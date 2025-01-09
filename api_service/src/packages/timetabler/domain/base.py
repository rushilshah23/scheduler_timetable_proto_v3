from dataclasses import dataclass
from abc import ABC, abstractmethod
@dataclass
class BaseDomain(ABC):

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()
    