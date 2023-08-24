import pytest

@pytest.fixture
def dset():
    import numpy as np
    from pyusel_types.data import NumpyData
    from pyusel_types.axes import SampledDataAxis, ArbitraryDataAxis, DataAxisSet

    plane = np.ones((2, 3, 1))
    extender = np.arange(4).reshape((1,1,-1))
    data = plane*extender

    axes = DataAxisSet(
        ax0 = ArbitraryDataAxis(np.array([0, 3])),
        ax1 = ArbitraryDataAxis(np.array([0, 0.3, 0.5])),
        ax2 = SampledDataAxis(0.5, 0.7, 4)
    )

    return NumpyData(data, axes)

def test_constructor(dset):
    assert True

def test_set_iter_vec(dset):
    from pyusel_types.data import NumpyData, Data

    dset.set_iter("ax0")
    _iter = iter(dset)
    assert 2 == _iter.iter['Nax'] - _iter.iter['axinc']['ninc']
    assert tuple(_iter.iter['strides']) == (4, 1)
    for i in range(3):
        out1 = next(_iter)
        for i in range(out1.shape[0]): 
            assert out1.__extract__(i) == 0
    assert _iter.iter['axinc']['ninc'] == 1
    assert list(_iter.iter['axinc']['vals'].keys())[0] == "ax0"
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 1
    assert _iter.iter['I'] == 3+1

    for i in range(3): 
        out1 = next(_iter)
        assert tuple(_iter.iter['strides']) == (4, 1)
        for i in range(out1.shape[0]): 
            assert out1.__extract__(i) == 1
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 1
    assert _iter.iter['I'] == 6+1

    for i in range(3): 
        out1 = next(_iter)
        assert tuple(_iter.iter['strides']) == (4, 1)
        for i in range(out1.shape[0]): 
            assert out1.__extract__(i) == 2
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 1
    assert _iter.iter['I'] == 9+1
    
    for i in range(3): 
        out1 = next(_iter)
        assert tuple(_iter.iter['strides']) == (4, 1)
        for i in range(out1.shape[0]): 
            assert out1.__extract__(i) == 3
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 1
    assert _iter.iter['I'] == 12+1

    try:
        next(_iter)
        assert False
    except StopIteration as si:
        assert True

def test_set_iter_mat(dset):
    from pyusel_types.data import NumpyData, Data

    dset.set_iter("ax0", "ax1")
    _iter = iter(dset)
    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 3)
    assert _iter.iter['I'] == 1
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == 0
    assert tuple(_iter.iter['strides']) == (1,)

    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 3)
    assert _iter.iter['I'] == 2
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == 1
    assert tuple(_iter.iter['strides']) == (1,)

    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 3)
    assert _iter.iter['I'] == 3
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == 2
    assert tuple(_iter.iter['strides']) == (1,)

    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 3)
    assert _iter.iter['I'] == 4
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == 3
    assert tuple(_iter.iter['strides']) == (1,)

    assert _iter.iter['Ntot'] == 4

    try:
        next(_iter)
        assert False
    except StopIteration as si:
        assert True

    dset.set_iter("ax0", "ax2")
    _iter = iter(dset)
    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 4)
    assert _iter.iter['I'] == 1
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == j
    assert tuple(_iter.iter['strides']) == (1,)

    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 4)
    assert _iter.iter['I'] == 2
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == j
    assert tuple(_iter.iter['strides']) == (1,)

    out1 = next(_iter)
    assert isinstance(out1, Data)
    assert isinstance(out1, NumpyData)
    assert len(out1.shape) == 2
    assert out1.shape == (2, 4)
    assert _iter.iter['I'] == 3
    for i in range(out1.shape[0]):
        for j in range(out1.shape[1]):
            assert out1.__extract__((i, j)) == j
    assert tuple(_iter.iter['strides']) == (1,)

    assert _iter.iter['Ntot'] == 3

    try:
        next(_iter)
        assert False
    except StopIteration as si:
        assert True
    


