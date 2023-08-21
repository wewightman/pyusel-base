import pytest
from pyusel_types.axes import SampledDataAxis, DataAxis, ArbitraryDataAxis
import numpy as np

@pytest.fixture
def makeaxes():
    ax1 = SampledDataAxis(5, 3, 35)
    ax2 = ArbitraryDataAxis(np.logspace(-5, 5, 11, endpoint=True, base=2))
    return ax1, ax2

def test_axis_types(makeaxes):
    ax1 = makeaxes[0]
    ax2 = makeaxes[1]

    # test ax1
    assert isinstance(ax1, DataAxis)
    assert isinstance(ax1, SampledDataAxis)
    assert not isinstance(ax1, ArbitraryDataAxis)

    # test ax2
    assert isinstance(ax2, DataAxis)
    assert not isinstance(ax2, SampledDataAxis)
    assert isinstance(ax2, ArbitraryDataAxis)

def test_attributes(makeaxes):
    ax1 = makeaxes[0]
    ax2 = makeaxes[1]
    
    for key in ['start', 'delta', 'N']:
        assert hasattr(ax1, key)
    assert not hasattr(ax1, 'points')

    for key in ['points', 'N']:
        assert hasattr(ax2, key)
    for key in ['start', 'delta']:
        assert not hasattr(ax2, key)

def test_indexing_valid(makeaxes):
    ax1 = makeaxes[0]
    ax2 = makeaxes[1]
    
    assert ax1[0] == 5
    assert ax1['N'] == 35

    assert ax2[0] == 2**(-5)
    assert ax2['N'] == 11
