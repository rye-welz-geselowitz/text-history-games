from .parser import Parser 
from typing import List
from message import Message
import re 
from datetime import datetime
import json 

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

class GoogleParser(Parser):
    def parse_file(self, filename: str) -> List[Message]:
        with open(filename, 'r') as f:
            data = json.load(f)
        messages = []
        for message_obj in data['messages']:
            if 'text' in message_obj:
                sender = message_obj['creator']['name']
                when_created = self._parse_timestamp(message_obj['created_date'])
                message = Message(sender=sender, body=message_obj['text'], when_created=when_created)
                messages.append(message)
        return messages

    def _parse_timestamp(self, timestamp: str) -> datetime:
        pattern = r'(?P<month>\w+)\s(?P<date>\d{1,2}),\s(?P<year>\d{4})\sat\s(?P<time>\d{1,2}:\d{2}:\d{2}\s(?:AM|PM))'
        match = re.search(pattern, timestamp)
        if match is None:
            raise ValueError('File does not match expected input')
        month_number = MONTHS.index(match.group('month').lower()) + 1
        date = int(match.group('date'))
        year = int(match.group('year'))
        time = datetime.strptime(match.group('time'), '%I:%M:%S %p')
        return datetime(
            year=year, month=month_number, day=date,
            hour=time.hour, minute=time.minute, second=time.second)
