# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
from pathlib import Path

import pytest

from eelbrain import load


def test_read_cnd():
    data_root = Path('~/Data/CND').expanduser()
    if not data_root.exists():
        pytest.skip(f"Data not available at {data_root}")

