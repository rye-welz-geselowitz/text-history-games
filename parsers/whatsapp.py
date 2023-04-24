from .parser import Parser 
from typing import List 
from message import Message
from  datetime import datetime
import re 

class WhatsappParser(Parser):
    def __init__(self, participant_names: List[str]):
        self.participant_names = participant_names

    def parse_file(self, filename: str) -> List[Message]:
        """ 
        Parses a chat history file exported from Whatsapp
        
        Arguments:
            filename (str): The name of the file to parse 
        Returns:
            A list of messages 
        """
        with open(filename, 'r') as f:
            return self._parse_text(f.read())

    def _parse_text(self, text: str) -> List[Message]:
        regex = self._get_regex()
        messages: List[Message] = []
        for match in re.finditer(regex, text):
            message = Message(
                when_created=self._parse_timestamp(match.group('timestamp')),
                sender=match.group('sender'),
                body=match.group('body'))
            messages.append(message)
        return messages

    def _parse_timestamp(self, timestamp: str) -> datetime:
        # 12/14/19, 1:28 AM
        return datetime.strptime(timestamp, '%m/%d/%y, %I:%M %p')

    def _get_regex(self) -> re.Pattern:
        joined_names = '|'.join(self.participant_names)
        sender_re = f'(?P<sender>({joined_names}))'
        date_re = '(?P<timestamp>\\d{1,2}\\/\\d{1,2}\\/\\d\\d\,\\s\\d{1,2}\:\\d{1,2}\\s(AM|PM))'
        body_re = '(?P<body>.*)'
        return re.compile(f'^{date_re}\s\-\s{sender_re}\:\s{body_re}', re.MULTILINE)
