from abc import ABC, abstractmethod
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
    
    @classmethod
    @abstractmethod
    def __copy__(self):
        raise NotImplementedError

class SampledDataAxis(DataAxis):
    def __init__(self, start, delta, N:int):
        if N == 1: return start
        if N <= 0: raise ValueError("Must have at least 1 point in set")
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
            start = 0 if value.start is None else value.start
            stop = self.N if value.stop is None else value.stop
            step = 1 if value.step is None else value.step
            if (start >= self.N) or (start < 0): raise IndexError("Indices must be in [0, N)")
            if stop > self.N: raise IndexError("Last index in slice must match the axis")
            if stop == 1: return self[start]
            
            return SampledDataAxis(self[start], step*self.delta, stop)
                
        elif isinstance(value, tuple):
            return [self[val] for val in value]
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
        
    def __len__(self):
        return self.N
    
    def __copy__(self):
        return SampledDataAxis(self.start, self.delta, self.N)
    
class ArbitraryDataAxis(DataAxis):
    def __init__(self, points):
        if np.ndim(points) == 0: return points
        elif np.ndim(points) > 1: raise ValueError("input points must be 1D")
        if len(points) == 1: return points[0]
        self.points=points
        self.N=len(points)
    
    def __getitem__(self, value):
        if isinstance(value, int):
            if value < 0: value = (value + self.N) % self.N
            if (value < 0) or (value >= self.N): raise IndexError("i must be between 0 and N-1")
            return self.points[value]
        elif isinstance(value, str):
            if not hasattr(self, value): raise IndexError("key must be points or N")
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = 0 if value.start is None else value.start
            stop = self.N if value.stop is None else value.stop
            step = 1 if value.step is None else value.step

            return ArbitraryDataAxis([self[i] for i in range(start, stop, step)])
        elif isinstance(value, tuple):
            return ArbitraryDataAxis([self[val] for val in value])
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
        
    def __len__(self):
        return self.N
    
    def __copy__(self):
        return ArbitraryDataAxis(np.array(self.points))
    
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

    def __getitem__(self, value):
        if isinstance(value, int):
            return self.__getattribute__(self.keys[value]).__copy__()
        elif isinstance(value, str):
            return self.__getattribute__(value).__copy__()
        elif isinstance(value, slice):
            start = 0 if value.start is None else value.start
            stop = len(self) if value.stop is None else value.stop
            step = 1 if value.step is None else value.step

            datas = [self[i].__copy__() for i in range(start, stop, step)]
            labels = [self.keys[i] for i in range(start, stop, step)]
            if len(datas) == 0: return None
            else: return DataAxisSet(**dict(zip(labels, datas)))
        elif isinstance(value, tuple):
            datas = []
            labels = []
            for val in value:
                if isinstance(val, int):
                    datas.append(self.__getattribute__(self.keys[val]).__copy__())
                    labels.append(self.keys[val])
                elif isinstance(val, str):
                    datas.append(self.__getattribute__(val).__copy__())
                    labels.append(val)
                else:
                    raise IndexError
            return DataAxisSet(**dict(zip(labels, datas)))
        else:
            raise IndexError("Indexing variables must be an int, a slice, or sting")
        
    def __copy__(self):
        copydict = {}
        for key in self.keys:
            copydict['key'] = self.__getattribute__(key).__copy__()
        return DataAxisSet(**copydict)
    
    def __iter__(self):
        self.iter = {}
        self.iter['i'] = 0
        return self

    def __next__(self):
        if self.iter['i'] >= len(self): raise StopIteration
        i = self.iter['i']
        self.iter['i'] = i+1
        return self.keys[i], self[i]