"""Generate synthesisable SystemVerilog for any design in the family registry.

This is the L3 step of the fidelity ladder: a design point that the L1
explorer liked (an :class:`~hw_dse.families.ArchConfig`) becomes real RTL
that can be simulated against the golden model, formally checked and
synthesised. One generator covers all four families, because they are one
datapath scheduled four ways:

=============  ==============================  ===========================
family         micro-rotations per clock       registers
=============  ==============================  ===========================
iterative      1 (variable shift, FSM)          one x/y/z set, re-used
unrolled_k     k chained (variable shifts)      one x/y/z set, re-used
pipelined      1 per pipeline stage             one x/y/z set per rotation
pipelined_m    m chained per pipeline stage     one x/y/z set per m rotations
=============  ==============================  ===========================

so ``iterative`` is emitted as ``unrolled_k`` with k=1 and ``pipelined`` as
``pipelined_m`` with m=1. Every knob of the golden model is honoured: data
width W, iterations N, angle-path width A, fractional guard bits g on x/y,
and truncating vs round-half-up shifts.

How the generator is parametrised
---------------------------------
The *Python* function is the parametrised object; each call emits one
specialised module with every knob written out as a ``localparam`` at the
top of the file. That is deliberate: the arctangent table and the gain
constant depend on N and A through real-valued maths (``atan``, ``sqrt``),
which synthesis tools evaluate inconsistently (Yosys cannot evaluate
``$atan`` in a constant function at all). Emitting them from Python means:

* the atan LUT comes from :func:`hw_dse.models.cordic_bitexact.atan_lut` and
  the gain pre-compensation constant from
  :func:`hw_dse.models.cordic_bitexact.init_x`, **the same functions the
  golden model uses**, so the RTL and the model can never disagree about a
  constant;
* the emitted file is plain, readable SystemVerilog that Yosys, Vivado,
  Verilator and Icarus all accept.

Uniform ports
-------------
Every generated module has the same interface, so one testbench, one formal
wrapper and one synthesis script drive every family::

    input  logic                 clk
    input  logic                 rst        // synchronous, active high
    input  logic                 valid_in   // theta_in is valid this cycle
    output logic                 ready      // module accepts valid_in this cycle
    input  logic signed [W-1:0]  theta_in   // angle, full scale 2^(W-1) == pi
    output logic                 valid_out  // one-cycle pulse per result
    output logic signed [W-1:0]  cos_out    // Q1.(W-2)
    output logic signed [W-1:0]  sin_out

``ready`` is tied high for the pipelined families (a new angle every
cycle). The FSM families raise it only in their idle state; an angle offered
while ``ready`` is low is ignored, exactly like the reference's ``start``.

Latency (documented, and checked in simulation and formally)
------------------------------------------------------------
Latency L is counted in rising clock edges, from the edge that samples
``valid_in`` (inclusive) to the edge that raises ``valid_out`` (inclusive):

* ``iterative``:   L = N + 3 (accept, pre-rotate, N rotations, output);
  one result every N + 3 cycles.
* ``unrolled_k``:  L = ceil(N/k) + 3; one result every L cycles.
* ``pipelined``:   L = N + 2 (pre-rotation register, N stage registers,
  output register); one result per cycle.
* ``pipelined_m``: L = ceil(N/m) + 2; one result per cycle.

These are exactly :attr:`hw_dse.families.ArchConfig.latency_cycles`, the
numbers the cost model and the explorer already use.

The datapath, as hardware
-------------------------
Each micro-rotation is three add/subtracts. The direction ``pos`` (residual
angle z >= 0) selects add or subtract; the generator writes each as *one*
adder with an XOR-ed operand and a carry-in::

    x - s  ==  x + ~s + 1          x + s  ==  x + s + 0
    =>  x_next = x + (s ^ {WX{pos}}) + pos

Round-half-up shifts reuse that carry-in, which is why rounding is (almost)
free in hardware: ``(v + 2^(i-1)) >>> i`` equals ``(v >>> i) + v[i-1]``, the
bit just below the cut. Subtracting the rounded value needs carry-in
``~v[i-1]`` and adding it needs ``v[i-1]``, so the carry-in becomes
``pos ^ v[i-1]`` and the rounding costs one XOR. Fixed shifts (pipelined
families) are pure wiring: ``{i{s[MSB]}, s[MSB:i]}``. Variable shifts (FSM
families) are barrel shifters; in rounding mode the shifter is one bit wider
so its extra output bit *is* the rounding bit.

Output reduction drops the g guard bits: ``x[W+g-1:g]`` (truncate), or
``x[W+g-1:g] + x[g-1]`` (round half up), keeping the low W bits exactly as
:func:`hw_dse.models.cordic_bitexact.cordic_sincos` does.

Bit-identity with the reference
-------------------------------
For ``iterative`` and ``pipelined`` at W=16, N=14 (A=W, g=0, trunc) the
generated modules produce the same output codes as the vendored
``cordic_rotation_iterative.sv`` / ``cordic_rotation_pipelined.sv`` on all
65,536 angles (``tests/test_rtl_generator.py``). The generated pipelined
design differs from the reference in two output-neutral ways: datapath
registers have no reset (only the valid chain does, which is cheaper on an
FPGA), and there is no clock-enable port.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import HEADROOM_BITS, atan_lut, init_x

REPO_ROOT = Path(__file__).resolve().parents[3]
GOLDEN_DIR = REPO_ROOT / "rtl_golden"
DEFAULT_BUILD_DIR = REPO_ROOT / "build" / "rtl"


@dataclass(frozen=True)
class RtlDesign:
    """One generated module and the facts a harness needs about it."""

    arch: ArchConfig
    module: str
    text: str
    latency: int  # rising edges from sampling valid_in to raising valid_out
    initiation_interval: int  # cycles between accepted inputs at full rate
    data_width: int

    def write(self, directory: Path | str | None = None) -> Path:
        d = Path(directory) if directory else DEFAULT_BUILD_DIR
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{self.module}.sv"
        path.write_text(self.text)
        return path


def module_name(arch: ArchConfig) -> str:
    """Deterministic, readable module name encoding every knob."""
    n = arch.numerics
    sched = {"unrolled_k": f"_k{arch.k}", "pipelined_m": f"_m{arch.m}"}.get(arch.family, "")
    ag = n.A - n.data_width
    ag_s = f"p{ag}" if ag >= 0 else f"m{-ag}"
    return f"cordic_{arch.family}{sched}_w{n.data_width}_n{n.n_iter}_a{ag_s}_g{n.frac_guard}_{n.rounding}"


# ---------------------------------------------------------------------------
# Small SystemVerilog-emitting helpers
# ---------------------------------------------------------------------------

def _const(value: int, width: int) -> str:
    """A two's-complement constant as a sized hex literal (no signedness games)."""
    return f"{width}'h{value & ((1 << width) - 1):0{(width + 3) // 4}x}"


def _sra(sig: str, width: int, sh: int) -> str:
    """Arithmetic right shift of a ``width``-bit signal by a constant: wiring."""
    if sh == 0:
        return sig
    if sh >= width:
        return f"{{{width}{{{sig}[{width - 1}]}}}}"
    return f"{{{{{sh}{{{sig}[{width - 1}]}}}}, {sig}[{width - 1}:{sh}]}}"


def _zext1(bit: str, width: int) -> str:
    """Zero-extend a 1-bit expression to ``width`` bits.

    Written as a concatenation on purpose: operands of ``{}`` are
    self-determined, so ``~pos`` stays one bit. A size cast ``18'(~pos)``
    would widen ``pos`` *before* inverting it and add 0x3fffe, not 0.
    """
    return f"{{{width - 1}'b0, {bit}}}"


def _round_bit(sig: str, width: int, sh: int) -> str:
    """Bit ``sh-1`` of the sign-extended signal: the round-half-up carry-in."""
    return f"{sig}[{min(sh - 1, width - 1)}]"


def _rotation(lines: list[str], ind: str, src: tuple[str, str, str], dst: tuple[str, str, str], i: int,
              wx: int, wz: int, atan: int, rnd: bool, y_is_zero: bool = False, need_z: bool = True,
              z_sign_only: bool = False) -> None:
    """Emit one constant-shift micro-rotation (pipelined families)."""
    x, y, z = src
    xn, yn, zn = dst
    pos = f"{dst[0]}_pos"
    lines.append(f"{ind}// micro-rotation {i}: shift {i}, atan(2^-{i}) = {atan} (angle LSBs)")
    lines.append(f"{ind}wire {pos} = ~{z}[{wz - 1}];  // residual angle z >= 0: rotate clockwise")
    if y_is_zero:
        # Rotation 0 of a pipeline sees y == 0 (gain pre-compensated x only):
        # x passes, y = +/- x. Synthesis would find this anyway; writing it
        # out keeps the generated code honest about what hardware remains.
        lines.append(f"{ind}wire signed [WX-1:0] {xn} = {x};")
        lines.append(f"{ind}wire signed [WX-1:0] {yn} = {pos} ? {x} : -{x};")
    else:
        sy, sx = _sra(y, wx, i), _sra(x, wx, i)
        cin_x = f"({pos} ^ {_round_bit(y, wx, i)})" if (rnd and i > 0) else pos
        cin_y = f"(~{pos} ^ {_round_bit(x, wx, i)})" if (rnd and i > 0) else f"~{pos}"
        lines.append(f"{ind}wire signed [WX-1:0] {xn} = {x} + ({sy} ^ {{{wx}{{{pos}}}}}) + {_zext1(cin_x, wx)};")
        lines.append(f"{ind}wire signed [WX-1:0] {yn} = {y} + ({sx} ^ {{{wx}{{~{pos}}}}}) + {_zext1(cin_y, wx)};")
    if need_z:  # the very last residual angle has no consumer
        decl = f"{ind}wire signed [WZ-1:0] {zn} = {z} + ({_const(atan, wz)} ^ {{{wz}{{{pos}}}}}) + {_zext1(pos, wz)};"
        if z_sign_only:  # only the next (final) rotation's direction reads it
            decl = f"{ind}/* verilator lint_off UNUSEDSIGNAL */\n{decl}\n{ind}/* verilator lint_on UNUSEDSIGNAL */"
        lines.append(decl)


def _reduce(sig: str, w: int, g: int, rnd: bool) -> str:
    """Output reduction: drop g guard bits (truncate or round half up)."""
    if g == 0:
        return f"{sig}[{w - 1}:0]"
    if rnd:
        return f"{sig}[{w + g - 1}:{g}] + {_zext1(f'{sig}[{g - 1}]', w)}"
    return f"{sig}[{w + g - 1}:{g}]"


def _header(arch: ArchConfig, name: str, latency: int, ii: int) -> list[str]:
    n = arch.numerics
    w, a, g = n.data_width, n.A, n.frac_guard
    lut = atan_lut(n.n_iter, a)
    sched = {
        "iterative": "1 micro-rotation per cycle (FSM, barrel shifters)",
        "unrolled_k": f"{arch.k} chained micro-rotations per cycle (FSM, barrel shifters)",
        "pipelined": "one pipeline register per micro-rotation",
        "pipelined_m": f"a pipeline register every {arch.m} micro-rotations",
    }[arch.family]
    return [
        "// Generated by hw_dse.rtl.generator -- do not edit; regenerate instead.",
        f"// family {arch.family}: {sched}",
        f"// design key: {arch.key()}",
        f"// latency {latency} cycles (valid_in sampled -> valid_out), one result every {ii} cycle(s)",
        f"// atan LUT (hw_dse.models.cordic_bitexact.atan_lut(N={n.n_iter}, A={a})): {list(lut)}",
        f"// gain pre-compensation (init_x(N={n.n_iter}, frac_bits={w - 2 + g})): {init_x(n.n_iter, w - 2 + g)}",
        "`default_nettype none",
        f"module {name} (",
        "    input  wire                  clk,",
        "    input  wire                  rst,",
        "    input  wire                  valid_in,",
        "    output wire                  ready,",
        *(["    /* verilator lint_off UNUSEDSIGNAL */  // A < W: the low W-A angle bits are dropped"] if a < w else []),
        f"    input  wire signed [{w - 1}:0]   theta_in,",
        *(["    /* verilator lint_on UNUSEDSIGNAL */"] if a < w else []),
        "    output logic                 valid_out,",
        f"    output logic signed [{w - 1}:0]  cos_out,",
        f"    output logic signed [{w - 1}:0]  sin_out",
        ");",
        "    /* verilator lint_off UNUSEDPARAM */  // documentation: the knobs this module was built for",
        f"    localparam int W  = {w};   // data width: angle in, sin/cos out (Q1.{w - 2})",
        f"    localparam int N  = {n.n_iter};   // micro-rotations",
        f"    localparam int A  = {a};   // angle path width (angle_guard {a - w:+d})",
        f"    localparam int G  = {g};   // fractional guard bits on x/y",
        f"    localparam int WX = {n.xy_width};   // x/y register width = W + {HEADROOM_BITS} headroom + G",
        f"    localparam int WZ = {n.z_width};   // z register width = A + {HEADROOM_BITS} headroom",
        f"    localparam bit ROUND = 1'b{1 if n.rounding == 'round' else 0};  // {n.rounding}",
        f"    localparam int LATENCY = {latency};",
        "    /* verilator lint_on UNUSEDPARAM */",
        f"    localparam logic [WX-1:0] INIT_X = {_const(init_x(n.n_iter, w - 2 + g), n.xy_width)};  // K_N in Q1.{w - 2 + g}",
        f"    localparam logic [WZ-1:0] PI     = {_const(1 << (a - 1), n.z_width)};  // pi in angle units",
        "",
    ]


def _align_z(n_w: int, a: int, wz: int) -> str:
    """Input angle (W bits) -> z format (A+2 bits): left-align or drop LSBs."""
    if a >= n_w:
        pad = f", {a - n_w}'b0" if a > n_w else ""
        return f"{{{{2{{theta_in[{n_w - 1}]}}}}, theta_in{pad}}}"
    # The dropped input LSBs are intentionally unused (A < W).
    return f"{{{{2{{theta_in[{n_w - 1}]}}}}, theta_in[{n_w - 1}:{n_w - a}]}}"


# ---------------------------------------------------------------------------
# Pipelined families (pipelined, pipelined_m)
# ---------------------------------------------------------------------------

def _pipelined_body(arch: ArchConfig) -> list[str]:
    n = arch.numerics
    w, a, g, nn = n.data_width, n.A, n.frac_guard, n.n_iter
    wx, wz = n.xy_width, n.z_width
    rnd = n.rounding == "round"
    m = arch.rotations_per_step
    steps = arch.steps
    lut = atan_lut(nn, a)
    L: list[str] = []
    L.append("    assign ready = 1'b1;  // fully pipelined: a new angle every cycle")
    L.append("")
    L.append("    // ---- stage 0: register the input with the quadrant pre-rotation ----")
    L.append("    // Angles in (pi/2, pi) or (-pi, -pi/2) are rotated by -/+pi into the")
    L.append("    // CORDIC convergence range; that flips the sign of x0 (y0 is 0).")
    L.append(f"    wire [1:0] quadrant = theta_in[{w - 1}:{w - 2}];")
    L.append(f"    wire signed [WZ-1:0] z_in = {_align_z(w, a, wz)};")
    L.append(f"    logic signed [WX-1:0] x_s0;")
    L.append(f"    logic signed [WZ-1:0] z_s0;")
    L.append("    always_ff @(posedge clk) begin")
    L.append("        case (quadrant)")
    L.append("            2'b01:   begin x_s0 <= -INIT_X; z_s0 <= z_in - PI; end  // (pi/2, pi)")
    L.append("            2'b10:   begin x_s0 <= -INIT_X; z_s0 <= z_in + PI; end  // (-pi, -pi/2)")
    L.append("            default: begin x_s0 <=  INIT_X; z_s0 <= z_in;      end")
    L.append("        endcase")
    L.append("    end")
    L.append("")
    L.append(f"    // valid chain: {steps + 2} registers (stage 0, {steps} rotation stage(s), output)")
    L.append(f"    logic [{steps + 1}:0] valid_pipe;")
    L.append("    always_ff @(posedge clk) begin")
    L.append(f"        if (rst) valid_pipe <= '0;")
    L.append(f"        else     valid_pipe <= {{valid_pipe[{steps}:0], valid_in}};")
    L.append("    end")
    L.append(f"    assign valid_out = valid_pipe[{steps + 1}];")
    L.append("")
    prev = ("x_s0", None, "z_s0")  # y of stage 0 is the constant 0
    for r in range(1, steps + 1):
        rots = list(range((r - 1) * m, min(r * m, nn)))
        L.append(f"    // ---- stage {r}: micro-rotation(s) {rots[0]}..{rots[-1]}, then a register ----")
        cur = prev
        for i in rots:
            dst = (f"x_r{i}", f"y_r{i}", f"z_r{i}")
            src = (cur[0], cur[1] or "'0", cur[2])
            _rotation(L, "    ", src, dst, i, wx, wz, lut[i], rnd, y_is_zero=(cur[1] is None), need_z=(i < nn - 1),
                      z_sign_only=(i == nn - 2 and i != rots[-1]))
            cur = dst
        last = r == steps
        if last:  # only the low W+G bits feed the output; the headroom is dropped
            L.append("    /* verilator lint_off UNUSEDSIGNAL */")
        L.append(f"    logic signed [WX-1:0] x_s{r}, y_s{r};")
        if last:
            L.append("    /* verilator lint_on UNUSEDSIGNAL */")
        if r == steps - 1 and nn - (steps - 1) * m == 1:
            # The last stage only looks at this residual angle's sign.
            L.append(f"    /* verilator lint_off UNUSEDSIGNAL */ logic signed [WZ-1:0] z_s{r}; /* verilator lint_on UNUSEDSIGNAL */")
        elif not last:
            L.append(f"    logic signed [WZ-1:0] z_s{r};")
        L.append("    always_ff @(posedge clk) begin")
        L.append(f"        x_s{r} <= {cur[0]};")
        L.append(f"        y_s{r} <= {cur[1]};")
        if not last:  # the final residual angle has no consumer
            L.append(f"        z_s{r} <= {cur[2]};")
        L.append("    end")
        L.append("")
        prev = (f"x_s{r}", f"y_s{r}", f"z_s{r}")
    L.append("    // ---- output register: drop the guard bits ----")
    L.append("    always_ff @(posedge clk) begin")
    L.append(f"        cos_out <= {_reduce(prev[0], w, g, rnd)};")
    L.append(f"        sin_out <= {_reduce(prev[1], w, g, rnd)};")
    L.append("    end")
    return L


# ---------------------------------------------------------------------------
# FSM families (iterative, unrolled_k)
# ---------------------------------------------------------------------------

def _fsm_body(arch: ArchConfig) -> list[str]:
    n = arch.numerics
    w, a, g, nn = n.data_width, n.A, n.frac_guard, n.n_iter
    wx, wz = n.xy_width, n.z_width
    rnd = n.rounding == "round"
    k = arch.rotations_per_step
    steps = arch.steps
    lut = atan_lut(nn, a)
    sw = max(1, math.ceil(math.log2(nn + k)))  # shift-amount width: up to N-1+k-1
    last_base = (steps - 1) * k
    L: list[str] = []
    L.append("    // FSM: IDLE (accept) -> PRE (quadrant pre-rotation) -> ITER x "
             f"{steps} -> OUT")
    L.append("    localparam logic [1:0] S_IDLE = 2'd0, S_PRE = 2'd1, S_ITER = 2'd2, S_OUT = 2'd3;")
    L.append("    logic [1:0] state;")
    L.append("    logic [1:0] quadrant;")
    L.append(f"    logic [{sw - 1}:0] base;  // shift amount of the first rotation this cycle (steps of {k})")
    L.append(f"    logic signed [WX-1:0] x, y;")
    L.append(f"    logic signed [WZ-1:0] z;")
    L.append("    assign ready = (state == S_IDLE);")
    L.append("")
    cur = ("x", "y", "z")
    for j in range(k):
        dst = (f"x_c{j}", f"y_c{j}", f"z_c{j}")
        xs, ys, zs = cur
        sh = f"sh{j}"
        L.append(f"    // ---- chained micro-rotation {j} of {k}: shift amount base+{j} ----")
        L.append(f"    wire [{sw - 1}:0] {sh} = base + {sw}'d{j};")
        # ROM: atan(2^-i) for the shift amounts this chain position can see.
        L.append(f"    logic [WZ-1:0] atan{j};")
        L.append("    always_comb begin")
        L.append(f"        case ({sh})")
        for i in range(j, nn, k):
            L.append(f"            {sw}'d{i}: atan{j} = {_const(lut[i], wz)};  // atan(2^-{i})")
        L.append(f"            default: atan{j} = '0;")
        L.append("        endcase")
        L.append("    end")
        pos = f"pos{j}"
        L.append(f"    wire {pos} = ~{zs}[{wz - 1}];")
        if rnd:
            # One-bit-wider barrel shifter: its LSB is bit (sh-1) of the
            # operand, i.e. the round-half-up carry-in (0 when sh == 0).
            L.append(f"    wire signed [WX:0] ysh{j}_w = $signed({{{ys}, 1'b0}}) >>> {sh};")
            L.append(f"    wire signed [WX:0] xsh{j}_w = $signed({{{xs}, 1'b0}}) >>> {sh};")
            L.append(f"    wire [WX-1:0] ysh{j} = ysh{j}_w[{wx}:1];")
            L.append(f"    wire [WX-1:0] xsh{j} = xsh{j}_w[{wx}:1];")
            cin_x, cin_y = f"({pos} ^ ysh{j}_w[0])", f"(~{pos} ^ xsh{j}_w[0])"
        else:
            L.append(f"    wire [WX-1:0] ysh{j} = {ys} >>> {sh};")
            L.append(f"    wire [WX-1:0] xsh{j} = {xs} >>> {sh};")
            cin_x, cin_y = pos, f"~{pos}"
        rx = f"{xs} + (ysh{j} ^ {{{wx}{{{pos}}}}}) + {_zext1(cin_x, wx)}"
        ry = f"{ys} + (xsh{j} ^ {{{wx}{{~{pos}}}}}) + {_zext1(cin_y, wx)}"
        rz = f"{zs} + (atan{j} ^ {{{wz}{{{pos}}}}}) + {_zext1(pos, wz)}"
        if nn % k and j >= nn % k:
            # In the final cycle this chain position runs past rotation N-1:
            # bypass it so exactly N rotations are applied.
            L.append(f"    wire act{j} = ({sh} < {sw}'d{nn});")
            rx, ry, rz = (f"act{j} ? ({e}) : {s}" for e, s in ((rx, xs), (ry, ys), (rz, zs)))
        L.append(f"    wire signed [WX-1:0] {dst[0]} = {rx};")
        L.append(f"    wire signed [WX-1:0] {dst[1]} = {ry};")
        L.append(f"    wire signed [WZ-1:0] {dst[2]} = {rz};")
        L.append("")
        cur = dst
    L.append("    always_ff @(posedge clk) begin")
    L.append("        if (rst) begin")
    L.append("            state     <= S_IDLE;")
    L.append("            valid_out <= 1'b0;")
    L.append("        end else begin")
    L.append("            valid_out <= 1'b0;")
    L.append("            case (state)")
    L.append("                S_IDLE: if (valid_in) begin")
    L.append(f"                    quadrant <= theta_in[{w - 1}:{w - 2}];")
    L.append("                    x        <= INIT_X;")
    L.append("                    y        <= '0;")
    L.append(f"                    z        <= {_align_z(w, a, wz)};")
    L.append("                    base     <= '0;")
    L.append("                    state    <= S_PRE;")
    L.append("                end")
    L.append("                S_PRE: begin  // rotate (pi/2, pi) by -pi and (-pi, -pi/2) by +pi")
    L.append("                    if (quadrant == 2'b01) begin x <= -x; z <= z - PI; end")
    L.append("                    if (quadrant == 2'b10) begin x <= -x; z <= z + PI; end")
    L.append("                    state <= S_ITER;")
    L.append("                end")
    L.append("                S_ITER: begin")
    L.append(f"                    x <= {cur[0]};")
    L.append(f"                    y <= {cur[1]};")
    L.append(f"                    z <= {cur[2]};")
    L.append(f"                    if (base == {sw}'d{last_base}) state <= S_OUT;")
    L.append(f"                    else base <= base + {sw}'d{k};")
    L.append("                end")
    L.append("                default: begin  // S_OUT: drop guard bits, present the result")
    L.append(f"                    cos_out   <= {_reduce('x', w, g, rnd)};")
    L.append(f"                    sin_out   <= {_reduce('y', w, g, rnd)};")
    L.append("                    valid_out <= 1'b1;")
    L.append("                    state     <= S_IDLE;")
    L.append("                end")
    L.append("            endcase")
    L.append("        end")
    L.append("    end")
    return L


def generate(arch: ArchConfig, module: str | None = None) -> RtlDesign:
    """Emit the SystemVerilog module for ``arch``."""
    name = module or module_name(arch)
    lat = arch.latency_cycles
    ii = 1 if arch.is_pipelined else lat
    body = _pipelined_body(arch) if arch.is_pipelined else _fsm_body(arch)
    text = "\n".join(_header(arch, name, lat, ii) + body + ["endmodule", "`default_nettype wire", ""])
    return RtlDesign(arch=arch, module=name, text=text, latency=lat, initiation_interval=ii,
                     data_width=arch.numerics.data_width)


# ---------------------------------------------------------------------------
# Committed golden examples (one per family)
# ---------------------------------------------------------------------------

GOLDEN_EXAMPLES: dict[str, ArchConfig] = {
    "iterative": ArchConfig.from_params("iterative", {"data_width": 16, "n_iter": 14}),
    "unrolled_k": ArchConfig.from_params("unrolled_k", {"data_width": 12, "n_iter": 11, "angle_guard": 1,
                                                        "frac_guard": 2, "rounding": "round", "k": 4}),
    "pipelined": ArchConfig.from_params("pipelined", {"data_width": 16, "n_iter": 14}),
    "pipelined_m": ArchConfig.from_params("pipelined_m", {"data_width": 12, "n_iter": 13, "angle_guard": -1,
                                                          "frac_guard": 1, "rounding": "round", "m": 3}),
}
"""The examples ``rtl_golden/`` holds. ``iterative``/``pipelined`` are the
reference configuration; the other two exercise every non-default knob
(angle guard of both signs, guard bits, rounding, N not a multiple of k/m)."""


def write_golden(directory: Path | None = None) -> list[Path]:
    """(Re)write the committed golden examples. ``tests/`` diffs against them."""
    d = directory or GOLDEN_DIR
    return [generate(a, module=f"cordic_golden_{fam}").write(d) for fam, a in GOLDEN_EXAMPLES.items()]


if __name__ == "__main__":  # pragma: no cover
    for p in write_golden():
        print("wrote", p)
