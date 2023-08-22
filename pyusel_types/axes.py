from abc import ABC, abstractmethod

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
            if not hasattr(self, value): raise IndexError("key must be points or N")
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = 0 if value.start is None else value.start
            stop = self.N if value.stop is None else value.stop
            step = 1 if value.step is None else value.step
            
            return [self[i] for i in range(value.start, value.stop, value.step)]
        elif isinstance(value, tuple):
            return [self[val] for val in value]
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

    def __getitem__(self, value):
        if isinstance(value, int):
            return self.__getattribute__(self.keys[value])
        elif isinstance(value, str):
            return self.__getattribute__(value)
        elif isinstance(value, slice):
            start = 0 if value.start is None else value.start
            stop = self.N if value.stop is None else value.stop
            step = 1 if value.step is None else value.step

            datas = [self[i] for i in range(start, stop, step)]
            labels = [self.keys[i] for i in range(start, stop, step)]
            if len(datas) == 0: return None
            elif len(datas) == 1: return datas[0]
            else: return DataAxisSet(**dict(zip(labels, datas)))
        elif isinstance(value, tuple):
            datas = []
            labels = []
            for val in value:
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
        
            