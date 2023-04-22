from typing import List
from engine.message import Message 
from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse_file(self, filename: str) -> List[Message]:
        raise NotImplementedError 
