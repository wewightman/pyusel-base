from abc import ABC, abstractmethod

class TXType(ABC):
    @classmethod
    @abstractmethod
    def gentabs(self, points):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def c_gentabs(self, points, Np:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def cleartabs(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError
    
class RXType(ABC):
    @classmethod
    @abstractmethod
    def gentabs(self, points):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def c_gentabs(self, points, Np:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def cleartabs(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError