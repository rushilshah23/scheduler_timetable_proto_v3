from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class DomainMapper():
    object:object


    @staticmethod
    @abstractmethod
    def serialzie_dbModel(self):
        pass

    @staticmethod
    @abstractmethod
    def deserialzie_dbModel(self):
        pass