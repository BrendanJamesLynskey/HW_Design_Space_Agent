"""L2: cycle-level and system-level simulation (milestone 3).

L1 scores a design with formulas: an estimated Fmax, a latency in cycles,
results per cycle. L2 asks what that design does *in a system*, with
requests arriving the way a real system sends them. It has two halves that
share one contract:

:mod:`hw_dse.l2.cycle`
    A cycle-accurate Python model of each family's interface: the
    ``ready`` / ``valid_in`` / ``valid_out`` behaviour, edge by edge, with the
    output codes from the golden model. It is checked against the generated
    RTL *cycle for cycle* on short bursty traces (:mod:`hw_dse.l2.validate`,
    using the L3 harness), so "the RTL and the model agree on every cycle" is
    a tested fact, not an assumption.
:mod:`hw_dse.l2.system`
    SimPy models of the CORDIC inside three systems (a DDS feeding a mixer,
    a control loop with a fixed tick, a bursty request stream). The CORDIC
    process in them accepts requests at its clock edges by the same contract
    (accept when ready; ready again ``ii`` cycles later; result ``latency``
    edges after the accepting edge, inclusive), and the system metrics
    (sustained throughput under back-pressure, queue depth, p50/p99 latency,
    utilisation) come out of the simulation.

Supporting modules:

:mod:`hw_dse.l2.fastsim`
    The same queue arithmetic vectorised over many designs at once, so the
    exhaustive ground truth (635,040 designs) can be simulated. A test
    checks it equals the SimPy models exactly.
:mod:`hw_dse.l2.bounds`
    Analytic L1 bounds of the system metrics (optimistic by construction),
    used to screen designs during exploration before L2 simulates the
    shortlist.
:mod:`hw_dse.l2.dds`
    SNR and SFDR of a DDS built from the golden model's exact outputs.
:mod:`hw_dse.l2.node`
    What the agent graph's ``l2_simulate`` node does with a run's front.

Provenance of every L2 number: ``simulated (<model>, <version>)``, naming
the scenario, the simulator and the clock it was run at (an *estimated*
Fmax unless measured data is supplied), so a simulated number is never
mistaken for a measurement.
"""

from __future__ import annotations

L2_VERSION = "l2-v1"
