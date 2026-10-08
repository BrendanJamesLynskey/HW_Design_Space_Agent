from __future__ import annotations

import pytest

from hw_dse import accuracy_table


@pytest.fixture(scope="session", autouse=True)
def _preload_accuracy() -> None:
    # Exact accuracy table (committed); keeps graph tests fast.
    accuracy_table.preload()
