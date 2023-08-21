from abc import ABC, abstractmethod

class DataAxis(ABC):
    @classmethod
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self, i:int):
        raise NotImplementedError

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
            if value.start is None: value.start = 0
            if value.stop is None: value.stop = self.N
            if value.step is None: value.step = 1
            return [self[i] for i in range(value.start, value.stop, value.step)]
        elif isinstance(value, tuple):
            return [self[val] for val in value]
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
    
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
            if not hasattr(self, value): raise IndexError("key must be points or N")
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            if value.start is None: value.start = 0
            if value.stop is None: value.stop = self.N
            if value.step is None: value.step = 1
            return [self[i] for i in range(value.start, value.stop, value.step)]
        elif isinstance(value, tuple):
            return [self[val] for val in value]
        else:
            raise IndexError(f"Unable to parse argument: {str(value)}")
    
class DataAxisSet(ABC):
    def __init__(self, **kwargs):
        dict.__init__(self)
        keys = []
        shape = []
        for key, item in kwargs:
            if not issubclass(DataAxis): raise ValueError("All inputs to DataAxisSet must be of type DataAxis")
            if (key in self.keys()): raise KeyError("Each key must be unique")
            setattr(self, key, item)
            keys.append(key)
            shape.append(item['N'])

        self.keys = tuple(keys)
        self.shape = tuple(shape)

    def __getitem__(self, value):
        if isinstance(value, int):
            return self.__getattribute__(self.labels[value])
        elif isinstance(value, str):
            return self['value']
        elif isinstance(value, slice):
            if value.start is None: value.start = 0
            if value.stop is None: value.stop = self.N
            if value.step is None: value.step = 1
            return [self[i] for i in range(value.start, value.stop, value.step)]
        elif isinstance(value, tuple):
            return [self[val] for val in value]
        else:
            raise IndexError("Indexing variables must be an int, a slice, or sting")
        
            