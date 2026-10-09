"""L3: synthesisable SystemVerilog for every CORDIC family, and its verification.

* :mod:`hw_dse.rtl.generator`  -- one generator for all four families;
* :mod:`hw_dse.rtl.sim`        -- drive generated (or reference, or gate-level)
  RTL with Icarus or Verilator and compare with the golden model;
* :mod:`hw_dse.rtl.formal`     -- SymbiYosys equivalence and latency checks.
"""
