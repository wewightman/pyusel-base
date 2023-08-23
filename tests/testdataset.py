import pytest

@pytest.fixture
def makenp():
    import numpy as np
    from pyusel_types.data import NumpyData, BasicNPDataSet
    from pyusel_types.axes import SampledDataAxis, DataAxisSet

    data = np.arange(24).reshape((2, 3, 4))
    axes = DataAxisSet(
        ax0 = SampledDataAxis(5, 3, 2),
        ax1 = SampledDataAxis(1, 1, 3),
        ax2 = SampledDataAxis(4, 2, 4)
    )

    return BasicNPDataSet(NumpyData(data, axes))

def test_init_NumpyData(makenp):
    # define iterator parameters
    makenp.setitreturn("ax2")
    iterator = iter(makenp)