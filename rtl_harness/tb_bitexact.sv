`timescale 1ns / 1ps
/*
    tb_bitexact.sv -- bit-exactness harness for the reference CORDIC RTL.

    Drives a list of angle codes through ONE of the reference modules and
    dumps the raw output codes, one line per angle:

        <theta> <cos> <sin>        (signed decimal)

    tests/test_bitexact_rtl.py compares those lines, code for code, with
    hw_dse.models.cordic_bitexact.cordic_sincos().

    Select the device under test with a define:
        -DDUT_PIPELINED   cordic_rotation_pipelined (streams 1 angle/cycle)
        (default)         cordic_rotation_iterative (start/done handshake)

    Plusargs:
        +angles=<file>    one signed decimal angle code per line
        +out=<file>       output file

    The harness never checks correctness itself: it is a pure stimulus /
    capture shell so the comparison logic lives in one place (Python).
*/
module tb_bitexact;

localparam DATA_WIDTH     = 16;
localparam NUM_ITERATIONS = 14;
localparam MAX_ANGLES     = 1 << 16;

logic clk = 1'b0;
logic srst = 1'b1;
always #5 clk = ~clk;

int angles [0:MAX_ANGLES-1];
int n_angles = 0;
int fd_in, fd_out, rc, v;
string angles_file, out_file;

logic signed [DATA_WIDTH-1:0] theta = '0;
logic signed [DATA_WIDTH-1:0] cos_o, sin_o;

`ifdef DUT_PIPELINED
    logic valid_in = 1'b0, valid_out;
    cordic_rotation_pipelined #(DATA_WIDTH, NUM_ITERATIONS) dut (
        .SRST(srst), .CLK(clk), .CE(1'b1),
        .THETA_IN(theta), .DATA_VALID_IN(valid_in),
        .COS_OUT(cos_o), .SIN_OUT(sin_o), .DATA_VALID_OUT(valid_out));
`else
    logic start = 1'b0, done;
    cordic_rotation_iterative #(DATA_WIDTH, NUM_ITERATIONS) dut (
        .SRST(srst), .CLK(clk), .CE(1'b1),
        .THETA_IN(theta), .COS_OUT(cos_o), .SIN_OUT(sin_o),
        .start(start), .done(done));
`endif

initial begin
    if (!$value$plusargs("angles=%s", angles_file)) $fatal(1, "missing +angles=");
    if (!$value$plusargs("out=%s", out_file)) $fatal(1, "missing +out=");
    fd_in = $fopen(angles_file, "r");
    if (fd_in == 0) $fatal(1, "cannot open %s", angles_file);
    while (!$feof(fd_in) && n_angles < MAX_ANGLES) begin
        rc = $fscanf(fd_in, "%d\n", v);
        if (rc == 1) begin
            angles[n_angles] = v;
            n_angles++;
        end
    end
    $fclose(fd_in);
    fd_out = $fopen(out_file, "w");

    repeat (4) @(negedge clk);
    srst = 1'b0;
    repeat (2) @(negedge clk);

`ifdef DUT_PIPELINED
    // Stream one angle per cycle; a parallel capture process below logs
    // results in arrival order (the pipeline preserves order).
    for (int i = 0; i < n_angles; i++) begin
        theta = angles[i];
        valid_in = 1'b1;
        @(negedge clk);
    end
    valid_in = 1'b0;
    repeat (NUM_ITERATIONS + 8) @(negedge clk);
`else
    for (int i = 0; i < n_angles; i++) begin
        theta = angles[i];
        start = 1'b1;
        @(negedge clk);
        start = 1'b0;
        while (!done) @(negedge clk);
        $fdisplay(fd_out, "%0d %0d %0d", angles[i], cos_o, sin_o);
    end
`endif
    $fclose(fd_out);
    $finish;
end

`ifdef DUT_PIPELINED
int captured = 0;
always @(posedge clk) begin
    if (!srst && valid_out) begin
        $fdisplay(fd_out, "%0d %0d %0d", angles[captured], cos_o, sin_o);
        captured++;
    end
end
`endif

endmodule
