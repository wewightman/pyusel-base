import pytest

@pytest.fixture
def makenp():
    import numpy as np
    from pyusel_types.data import NumpyData
    from pyusel_types.axes import SampledDataAxis, DataAxisSet

    data = np.arange(24).reshape((2, 3, 4))
    axes = DataAxisSet(
        ax0 = SampledDataAxis(5, 3, 2),
        ax1 = SampledDataAxis(1, 1, 3),
        ax2 = SampledDataAxis(4, 2, 4)
    )

    return NumpyData(data, axes)

def test_init_NumpyData(makenp):
    makenp

def test_getitem_NumpyData(makenp):
    res = makenp[0,:,:]
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            assert res[i,j] == i*res.shape[1]+j