from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    when_created: datetime
    sender: str
    body: str
