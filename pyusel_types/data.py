from abc import ABC, abstractmethod
import numpy as np

from pyusel_types.axes import DataAxis, DataAxisSet

class Data(ABC):
    @classmethod
    @abstractmethod
    def get_ct(self, *args, **kargs):
        """Get data as ctype outputs"""
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def get_np(self, *args, **kargs):
        """Get data as numpy type outputs"""
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self, *args, **kargs):
        """Get data as numpy type outputs"""
        raise NotImplementedError

class NumpyData(Data):
    def __init__(self, data:np.ndarray, axes:DataAxisSet):
        self.data : np.ndarray = data
        self.axes : DataAxisSet = axes
        if len(axes) != len(data.shape): raise ValueError("Must be one DataAxis for each dimension of data")
        N = len(axes)

        for n in range(N):
            if self.data.shape[n] != axes[n].N: raise ValueError("Each data axis much have the same length as its corresponding DataAxis")

        self.shape = tuple(self.data.shape)

    def __getitem__(self, value):
        axes = []
        labels = []
        just_ints = True
        just_labels = True
        for val in value:
            if not isinstance(val, str): just_labels = False
            if not isinstance(val, int): just_ints = False

        # return a single datapoint
        if just_ints:
            return self.data[*value]

        # return the requested axes
        if just_labels:
            labels.extend([val for val in value])
            axes.extend([self.axes[val] for val in value])
        
        # return as many portions of axes as the slices in value
        elif (len(value) == len(self.shape)):
            labels.extend([self.axes.keys[iv][val] for iv, val in enumerate(value) if not isinstance(val, int)])
            axes.extend([self.axes[iv][val] for iv, val in enumerate(value) if not isinstance(val, int)])
        else: raise IndexError("Must specify specific axis labels or have one indexer for each dimension")

        return NumpyData(self.data[*value], DataAxisSet(**dict(zip(labels, axes))))

    def get_ct(self):
        raise NotImplementedError
    
    def get_np(self):
        return self.data

class CData(Data):
    def __init__(self, data, axes:DataAxisSet):
        raise NotImplementedError
    
    def get_ct(self, *args, **kargs):
        """Get data as ctype outputs"""
        raise NotImplementedError
    
    def get_np(self, *args, **kargs):
        """Get data as numpy type outputs"""
        raise NotImplementedError

class DataSet(ABC):
    @classmethod
    @abstractmethod
    def getaxes(self):
        """get list of Axes objects
        """
        raise NotImplementedError
    
    def setitreturn(self, *args):
        """Define which axes the iterable will return as a sub dataset"""
        if hasattr(self, 'iter'): delattr(self, 'iter')
        self.iter = {}
        axes : DataAxisSet = self.getaxes()
        axinc = {}
        for arg in args:
            if arg not in axes: raise AttributeError(f"Non-existent key in this dataset: {arg}")
            elif arg in axinc.keys(): raise AttributeError(f"Duplicate include key: {arg}")
            else: axinc[arg] = axes[arg]

        # convert to DataAxisSet
        axinc = DataAxisSet(**axinc)

        axexc = {}
        for arg in args: 
            if arg not in axinc: axexc[arg] = axes[arg]

        # convert to DataAxisSet
        axexc = DataAxisSet(**axexc)

        # get number of dimensions for excluded and included axes
        nexc = len(axexc)
        ninc = len(axinc)

        # calculate stides for each level
        N = 1
        for i in range(nexc): N *= axexc[i].N
        strides = [None] * nexc
        for i in range(nexc):
            strides[i] = 1
            for j in range(i+1, nexc):
                strides[i] *= axexc[j].N

        #copy variables to self
        self.iter['axexc'] = axexc
        self.iter['nexc'] = nexc
        self.iter['axinc'] = axinc
        self.iter['ninc'] = ninc

        # total number of iterable indices and current index
        self.iter['N'] = N
        self.iter['I'] = 0

        self.iter['strides'] = strides

    def __iter__(self):
        
        self.iter['slices'] = []
        axinc = self.iter['axinc']
        for label, ax in self.getaxes():
            if label in axinc:
                self.iter['slices'].append(slice(ax.N))
            else: 
                self.iter['slices'].append(0)

    def __next__(self):
        axes : DataAxisSet = self.getaxes()
        strides = self.iter['strides']
        slices = self.iter['slices']
        nexc = self.iter['nexc']
        I = self.iter['I']

        iax = 0
        iexc = 0
        delta = I
        curi = [0] * nexc
        for label in axes.keys():
            if label in self.iter['axexc']:
                for i in range(iexc):
                    delta -= curi[i] * strides[i]
                curi[iexc] = int(delta//strides[iexc])
                delta = I
                iexc += 1
                slices[iax] = curi[iexc]
            iax += 1

        return self.data[*slices]

class BasicNPDataSet(DataSet):
    def __init__(self, data:Data):
        self.data = data

    def getaxes(self):
        return self.data.axes
    
