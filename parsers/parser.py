from typing import List
from message import Message
from abc import ABC, abstractmethod

class Parser(ABC):
    """ Abstract base class for parsing a file into a list of messages """
    @abstractmethod
    def parse_file(self, filename: str) -> List[Message]:
        """ 
        Arguments:
            filename (str): The name of the file to parse 
        Returns:
            A list of messages 
        """
        raise NotImplementedError 
