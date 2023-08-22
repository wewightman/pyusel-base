from abc import ABC, abstractmethod

class DataSet(ABC):
    @classmethod
    @abstractmethod
    def getaxes(self):
        """get list of Axes objects
        """
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def transform(self, *args, **kwargs):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self, *args, **kwargs):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def rawdata(self, *args, **kwargs):
        raise NotImplementedError
    