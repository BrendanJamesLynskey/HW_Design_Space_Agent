`timescale 1ns / 1ps
/*
    tb_generated.sv -- one stimulus/capture harness for every generated CORDIC.

    Every module from hw_dse.rtl.generator (and every gate-level netlist
    synthesised from one) has the same ports, so this single harness drives
    all four families in both Icarus and Verilator (--binary --timing):

        clk, rst, valid_in, ready, theta_in, valid_out, cos_out, sin_out

    It offers angle i on valid_in until the DUT accepts it (valid_in && ready
    at a rising edge), then offers angle i+1. Pipelined DUTs accept one per
    cycle; FSM DUTs accept one whenever they are idle. Each result is logged
    in arrival order with its measured latency:

        <theta> <cos> <sin> <latency>      (signed decimal; latency in cycles)

    where latency = rising edges from the edge that accepted the angle to the
    edge that raised valid_out, both inclusive. hw_dse.rtl.sim compares the
    codes with the golden model and the latency with the documented one.
    Like tb_bitexact.sv, the harness never judges correctness itself.

    Defines (set by hw_dse.rtl.sim):
        HW_DUT     module name of the device under test
        HW_W       data width W
        HW_MAXN    capacity of the angle buffer
    Plusargs:
        +angles=<file>  one signed decimal angle per line, first line = count
        +out=<file>     output file
*/
`ifndef HW_MAXN
`define HW_MAXN 262144
`endif

module tb_generated;

localparam int W    = `HW_W;
localparam int MAXN = `HW_MAXN;

logic clk = 1'b0;
logic rst = 1'b1;
always #5 clk = ~clk;

logic                valid_in = 1'b0;
logic signed [W-1:0] theta    = '0;
wire                 ready, valid_out;
wire  signed [W-1:0] cos_o, sin_o;

`HW_DUT dut (
    .clk(clk), .rst(rst),
    .valid_in(valid_in), .ready(ready), .theta_in(theta),
    .valid_out(valid_out), .cos_out(cos_o), .sin_out(sin_o)
);

int angles   [0:MAXN-1];
int accepted [0:MAXN-1];  // cycle number at which angle i was accepted
int n_angles = 0, n_acc = 0, n_res = 0, cyc = 0;
int fd, rc, v;
string angles_file, out_file;

initial begin
    if (!$value$plusargs("angles=%s", angles_file)) $fatal(1, "missing +angles=");
    if (!$value$plusargs("out=%s", out_file)) $fatal(1, "missing +out=");
    fd = $fopen(angles_file, "r");
    if (fd == 0) $fatal(1, "cannot open angles file");
    rc = $fscanf(fd, "%d\n", n_angles);
    if (rc != 1 || n_angles > MAXN) $fatal(1, "bad angle count");
    for (int i = 0; i < n_angles; i++) begin
        rc = $fscanf(fd, "%d\n", v);
        angles[i] = v;
    end
    $fclose(fd);
    fd = $fopen(out_file, "w");
    repeat (4) @(negedge clk);
    rst = 1'b0;
end

// Drive on the falling edge, so inputs are stable at the rising edge.
always @(negedge clk) begin
    if (!rst && n_acc < n_angles) begin
        valid_in <= 1'b1;
        theta    <= angles[n_acc];
    end else begin
        valid_in <= 1'b0;
    end
end

// Observe on the rising edge: these are the values from *before* the edge,
// i.e. what the DUT's registers sample now, and what its outputs presented
// since the previous edge.
always @(posedge clk) begin
    cyc = cyc + 1;
    if (!rst) begin
        if (valid_out === 1'b1) begin
            // valid_out was raised by the previous edge (cyc - 1).
            $fdisplay(fd, "%0d %0d %0d %0d", angles[n_res], cos_o, sin_o, (cyc - 1) - accepted[n_res] + 1);
            n_res = n_res + 1;
            if (n_res == n_angles) begin
                $fclose(fd);
                $finish;
            end
        end else if (valid_out !== 1'b0) begin
            $fatal(1, "valid_out is X/Z at cycle %0d", cyc);
        end
        if (valid_in && ready === 1'b1) begin
            accepted[n_acc] = cyc;
            n_acc = n_acc + 1;
        end
        if (cyc > 64 * (n_angles + 16) + 1000) $fatal(1, "timeout: %0d of %0d results", n_res, n_angles);
    end
end

endmodule
