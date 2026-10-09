"""SNR and SFDR of a DDS built from the golden model's exact outputs.

A direct digital synthesiser is a phase accumulator (here 32 bits) whose top
W bits address a phase-to-amplitude converter, in our case the CORDIC. Its
spectral purity is what a radio engineer specifies, so L2 reports it for
every simulated design:

1. Pick a tone that is *coherent* with the FFT: frequency word
   ``FTW = bin * 2^32 / N_FFT`` with an odd ``bin`` (so the tone visits
   ``N_FFT`` distinct phases and lands exactly on one FFT bin; no window
   is needed and no leakage blurs the spurs).
2. Truncate each accumulator value to the top W bits (the CORDIC's signed
   angle code; full scale 2^(W-1) == pi) and run
   :func:`~hw_dse.models.cordic_bitexact.cordic_sincos`: the exact codes
   the RTL would output.
3. FFT the complex output ``cos + j sin`` scaled to full scale.
   **SFDR** = carrier power / largest other bin (DC counts as a spur),
   **SNR** = carrier power / everything else.

With ``N_FFT = 2^14`` the accumulator's low 18 bits stay zero, so for
W <= 14 the phase truncation is part of what is measured and for W > 14 the
spectrum shows the CORDIC's own arithmetic error. Numbers depend only on
the numeric knobs, never on the family or the clock. Provenance:
``simulated (hw_dse.l2.dds ...)``.
"""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

from hw_dse.l2 import L2_VERSION
from hw_dse.models.cordic_bitexact import CordicNumerics, cordic_sincos

N_FFT = 1 << 14
TONE_BIN = 1297  # odd (coprime with N_FFT), roughly fs/12.6
ACC_BITS = 32

PROVENANCE = (f"simulated (hw_dse.l2.dds {L2_VERSION}: golden-model DDS, {ACC_BITS}-bit phase accumulator, "
              f"coherent {N_FFT}-point FFT, tone bin {TONE_BIN})")


def phase_codes(data_width: int, n: int = N_FFT, tone_bin: int = TONE_BIN) -> np.ndarray:
    """Top-W-bit signed angle codes of a coherent 32-bit phase accumulator."""
    ftw = tone_bin * (1 << ACC_BITS) // n
    acc = (np.arange(n, dtype=np.uint64) * np.uint64(ftw)) & np.uint64((1 << ACC_BITS) - 1)
    code = (acc >> np.uint64(ACC_BITS - data_width)).astype(np.int64)
    return np.where(code >= (1 << (data_width - 1)), code - (1 << data_width), code)


@lru_cache(maxsize=65536)
def dds_spectrum(cfg: CordicNumerics) -> tuple[float, float]:
    """(SFDR dBc, SNR dB) of the DDS tone for one numeric configuration."""
    th = phase_codes(cfg.data_width)
    c, s = cordic_sincos(th, cfg)
    scale = float(1 << (cfg.data_width - 2))
    spec = np.abs(np.fft.fft((c + 1j * s) / scale)) ** 2
    carrier = spec[TONE_BIN]
    rest = np.delete(spec, TONE_BIN)
    worst = float(rest.max())
    noise = float(rest.sum())
    sfdr = 10 * math.log10(carrier / worst) if worst > 0 else float("inf")
    snr = 10 * math.log10(carrier / noise) if noise > 0 else float("inf")
    return sfdr, snr
