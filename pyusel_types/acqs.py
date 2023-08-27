from abc import ABC, abstractmethod

class TXType(ABC):
    @classmethod
    @abstractmethod
    def gen(self, points):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def c_gen(self, points, Np:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def clear(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError
    
class RXType(ABC):
    @classmethod
    @abstractmethod
    def gen(self, points):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def c_gen(self, points, Np:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def clear(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError
    
class Aperture(ABC):
    @classmethod
    @abstractmethod
    def gen(self, points):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def c_gen(self, points, Np:int):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def clear(self):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def __getitem__(self):
        raise NotImplementedError