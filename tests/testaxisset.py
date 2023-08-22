import pytest
from pyusel_types.axes import SampledDataAxis, ArbitraryDataAxis, DataAxisSet, DataAxis
import numpy as np

@pytest.fixture
def makeaxes():
    ax1 = SampledDataAxis(5, 3, 35)
    ax2 = ArbitraryDataAxis(np.logspace(-5, 5, 11, endpoint=True, base=2))
    ax3 = SampledDataAxis(2, 3, 35)
    ax4 = ArbitraryDataAxis(np.logspace(-2, 2, 5, endpoint=True, base=2))
    return ax1, ax2, ax3, ax4

@pytest.fixture
def makeaxset(makeaxes):
    dset = DataAxisSet(
        ax1=makeaxes[0],
        ax2=makeaxes[1],
        ax3=makeaxes[2],
        ax4=makeaxes[3]
        )
    return dset

def test_make_dataxisset(makeaxset):
    dset = makeaxset

def test_get_subset(makeaxset):
    dset = makeaxset
    assert len(dset) == 4
    assert isinstance(dset[0], DataAxis)
    assert isinstance(dset['ax1'], DataAxis)
    assert isinstance(dset[0:2], DataAxisSet)
    assert isinstance(dset[(0, 'ax2', 3)], DataAxisSet)
    assert dset[10::] is None
    