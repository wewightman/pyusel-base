from abc import ABC, abstractmethod

class RawData(ABC):
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
    def getdata(self, *args, **kwargs):
        raise NotImplementedError
    
class RawDataSet(ABC):
    @classmethod
    @abstractmethod
    def __init__(self):
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
    def data(self, *args, **kwargs):
        raise NotImplementedError
    