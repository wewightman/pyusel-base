from abc import ABC, abstractmethod
import numpy as np
from pyusel_types.axes import DataAxisSet

class Data(ABC):
    @classmethod
    @abstractmethod
    def __extract__(self, slices):
        """extract portion of data specified by slices"""
        raise NotImplementedError
    
    def set_iter(self, *values):
        """Set iterator to go over the subselected axes defined by values
        Parameters:
        ----
        values: an iterable where each element is of the type [[str] | [slice | int]]
        """
        just_strings = True
        just_ints = True
        ints_n_slice = True

        if len(values) == 1 and isinstance(values[0], str):
            self.iter = {'axinc':{}}
            self.iter = {'axinc':{'vals':{values[0]:slice(None)}}}
            self.iter['axinc']['ninc'] = 1
            return
    
        
        for val in values:
            if not isinstance(val, str): just_strings = False
            if not isinstance(val, int): just_ints = False
            if not (isinstance(val, int) or isinstance(val, slice)): ints_n_slice = False

        # error out if not all dimensions are defined for the non-string cases
        if (just_ints or ints_n_slice) and (len(values) != len(self.axes)):
            raise IndexError("If elements of values are of type [[int] | [int | slice]]")

        # extract a scalar if the slicer set is just integers
        if just_ints:
            return self.__extract__(values)
        elif just_strings:
            self.iter = {'axinc':{'vals':dict(zip(values, [slice(None)]*len(values)))}}
            self.iter['axinc']['ninc'] = len(values)
        elif ints_n_slice:
            self.iter = {}
            self.iter['axinc'] = {'axinc':{'vals':{}}}
            for iv, value in enumerate(values):
                if isinstance(value, slice):
                    self.iter['axinc']['vals'][self.axes.keys[iv]] = value
            self.iter['axinc']['ninc'] = len(self.iter['axinc']['vals'].keys())
        else:
            raise ValueError("Unable to parse values as iterable with elements of type [[str] | [slice | int]]")
    
    def __iter__(self):
        if not hasattr(self, 'iter'):
            raise ValueError("Must call 'set_iter' before using Data as iterator")
        
        Niax = len(self.axes)
        Nexc = Niax - self.iter['axinc']['ninc']
        Ntotal = 1
        for key, ax in self.axes:
            if key not in self.iter['axinc']['vals'].keys():
                Ntotal *= ax['N']

        # generate the strides for arbitrary axes
        strides = []
        for key, ax in self.axes:
            if key not in self.iter['axinc']['vals'].keys():
                strides.append(ax['N'])

        self.iter['strides'] = strides
        self.iter['I'] = 0
        self.iter['Ntot'] = Ntotal
        self.iter['Nax'] = Niax
            
        return self 
    
    def __get_item_axes__(self, *value):
        just_strings = True
        just_ints = True
        ints_n_slice = True

        if len(value) == 1 and isinstance(value[0], str):
            return DataAxisSet(**{value[0]:self.axes[value[0]]})
        
        for val in value:
            if not isinstance(val, str): just_strings = False
            if not isinstance(val, int): just_ints = False
            if not (isinstance(val, int) or isinstance(val, slice)): ints_n_slice = False

        # Extract subset of axes selected by label only
        if just_strings:
            newaxes = {}
            for val in value:
                newaxes[val] = self.axes[val]
            return DataAxisSet(**newaxes)
        
        # return no axes if a scalar value is indexed
        elif just_ints:
            return None
        
        # only return axes indexed with slices, not ints
        elif ints_n_slice:
            newaxes = {}
            for iv, val in enumerate(value):
                if isinstance(val, slice): newaxes[self.axes.keys[iv]] = self.axes[iv][val]
            
            return DataAxisSet(**newaxes)
        else: raise IndexError(str(value))
    
    def __next__(self):
        if not hasattr(self, 'iter'):
            raise ValueError("Must call 'set_iter' and '__iter__' before using Data as iterator")
        if self.iter['I'] >= self.iter['Ntot']: raise StopIteration
        strides = self.iter['strides']
        I : int = self.iter['I']
        self.iter['I'] = I+1
        Nax : int = self.iter['Nax']
        axinc = self.iter['axinc']
        slicer = []

        # build slicer for N-dimensions not included in the iterable
        Nexc = Nax - axinc['ninc']
        if Nexc == 0: return self
        
        else: 
            iexc = 0
            for i, (key, ax) in enumerate(self.axes):
                if key in axinc['vals'].keys(): slicer.append(axinc['vals'][key])
                else: slicer.append(int((I//np.prod(strides[(iexc+1):]))%strides[iexc])); iexc += 1

        _data = self.__extract__(slicer)
        _axes = self.__get_item_axes__(*slicer)

        if isinstance(self, NumpyData): return NumpyData(_data, _axes)
        if isinstance(self, CData): return CData(_data, _axes)

class NumpyData(Data):
    def __init__(self, data:np.ndarray, axes:DataAxisSet):
        self.data = data
        self.axes = axes
        shape = []
        for id, dim in enumerate(data.shape):
            if len(axes[id]) != dim:
                raise ValueError("data and axes must have the same dimensions")
            shape.append(dim)
        self.shape = tuple(shape)

    def __extract__(self, slicer):
        if isinstance(slicer, int): return self.data[slicer]
        return self.data[*slicer]

class CData(Data):
    def __init__(self, data:np.ndarray, axes:DataAxisSet):
        raise NotImplementedError

    def __extract__(self, value):
        raise NotImplementedError

class DataSet(ABC):
    @classmethod
    @abstractmethod
    def transform(self, data):
        raise NotImplementedError