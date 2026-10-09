"""L4 synthesis (measured) and L5 back-annotation.

* :mod:`hw_dse.synth.flow`         -- Yosys + nextpnr-xilinx on xc7a35tcpg236-1;
* :mod:`hw_dse.synth.sweep`        -- the measured design points;
* :mod:`hw_dse.synth.measured`     -- the measured-points CSV schema (any tool);
* :mod:`hw_dse.synth.gatesim`      -- gate-level simulation of the mapped netlist;
* :mod:`hw_dse.synth.recalibrate`  -- refit the cost model per tool (L5).
"""
