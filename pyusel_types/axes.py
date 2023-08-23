from abc import ABC, abstractmethod
from typing import Any
import numpy as np

class DataAxis(ABC):
    @classmethod
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __len__(self, i:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self, i:int):
        raise NotImplementedError
    
    def __iter__(self):
        self.iter.i = 0
        return self
    
    def __next__(self):
        if self.iter.i >= self.N: raise StopIteration
        val = self[self.iter.i]
        self.iter.i += 1
        return val

class SampledDataAxis(DataAxis):
    def __init__(self, start, delta, N:int):
        self.start=start
        self.delta=delta
        self.N=N
    
    def __getitem__(self, value):
        if isinstance(value, int):
            if value < 0: value = (value + self.N) % self.N
            if (value < 0) or (value >= self.N): raise IndexError("i must be between 0 and N-1")
            return self.start + self.delta * value
        elif isinstance(value, str):
            if not hasattr(self, value): raise IndexError("key must be points or N")
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = int(0) if value.start is None else int(value.start)
            stop = self.N if value.stop is None else int(value.stop)
            if stop > self.N: raise IndexError
            step = int(1) if value.step is None else int(value.step)
            newstart = self[start]
            newN = (stop-start)//step
            newstep = step*self.delta
            return SampledDataAxis(newstart, newstep, newN)
        elif isinstance(value, tuple):
            return ArbitraryDataAxis([self[val] for val in value if isinstance(val, int)])
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
        
    def __len__(self):
        return self.N
    
class ArbitraryDataAxis(DataAxis):
    def __init__(self, points):
        self.points=points
        self.N=len(points)
    
    def __getitem__(self, value):
        if isinstance(value, int):
            if value < 0: value = (value + self.N) % self.N
            if (value < 0) or (value >= self.N): raise IndexError("i must be between 0 and N-1")
            return self.points[value]
        elif isinstance(value, str):
            if not hasattr(self, value): raise IndexError("when indexing with a string, key must be points or N")
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = int(0) if value.start is None else int(value.start)
            stop = len(self) if value.stop is None else int(value.stop)
            if stop > self.N: raise IndexError
            step = int(1) if value.step is None else int(value.step)
            
            return ArbitraryDataAxis([self[i] for i in range(start, stop, step)])
        elif isinstance(value, tuple):
            return ArbitraryDataAxis([self[val] for val in value])
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
        
    def __len__(self):
        return self.N
    
class DataAxisSet(ABC):
    def __init__(self, **kwargs):
        keys = []
        shape = []
        for key, item in kwargs.items():
            if not isinstance(item, DataAxis): raise ValueError("All inputs to DataAxisSet must be of type DataAxis")
            if (key in keys): raise KeyError("Each key must be unique")
            setattr(self, key, item)
            keys.append(key)
            shape.append(item['N'])

        self.keys = tuple(keys)
        self.shape = tuple(shape)
    
    def __len__(self):
        return len(self.keys)
    
    def __contains__(self, arg:str):
        return True if arg in self.keys else False

    def __getitem__(self, value):
        if isinstance(value, int):
            return self.__getattribute__(self.keys[value])
        elif isinstance(value, str):
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = int(0) if value.start is None else int(value.start)
            stop = len(self) if value.stop is None else int(value.stop)
            if stop > len(self): raise IndexError
            step = int(1) if value.step is None else int(value.step)

            datas = [self[i] for i in range(start, stop, step)]
            labels = [self.keys[i] for i in range(start, stop, step)]
            if len(datas) == 0: return None
            elif len(datas) == 1: return datas[0]
            else: return DataAxisSet(**dict(zip(labels, datas)))
        elif isinstance(value, tuple):
            datas = []
            labels = []
            for iv, val in enumerate(value):
                if isinstance(val, int):
                    datas.append(self.__getattribute__(self.keys[val]))
                    labels.append(self.keys[val])
                elif isinstance(val, str):
                    datas.append(self.__getattribute__(val))
                    labels.append(val)
                else:
                    raise IndexError
            return DataAxisSet(**dict(zip(labels, datas)))
        else:
            raise IndexError("Indexing variables must be an int, a slice, or sting")
        
    def __iter__(self):
        if hasattr(self, 'iter'): delattr(self, 'iter')
        self.iter = {}
        self.iter['N'] = len(self.shape)
        self.iter['i'] = 0
        return self
    
    def __next__(self):
        i = self.iter['i']
        N = self.iter['N']
        if i == N: raise StopIteration
        key = self.keys[i]
        ax = self.__getattribute__(self.keys[i])
        return key, ax

        
            