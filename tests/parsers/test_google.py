from unittest.mock import patch, mock_open
from parsers.google import GoogleParser
from datetime import datetime

READ_DATA = """{
    "messages": [
      {
        "creator": {
          "name": "Lou",
          "email": "lou@example.com",
          "user_type": "Human"
        },
        "created_date": "Tuesday, February 10, 2015 at 6:03:00 PM UTC",
        "text": "did you see the thing i sent u?"
      },
      {
        "creator": {
          "name": "Elektra",
          "email": "elektra@example.com",
          "user_type": "Human"
        },
        "created_date": "Tuesday, February 10, 2015 at 6:03:26 PM UTC",
        "text": "nope not yet why"
      }
    ]
}
"""

class TestParseFile:
    def test_parses_file(self):
        parser = GoogleParser()

        with patch("parsers.google.open", mock_open(read_data=READ_DATA)):
            messages = parser.parse_file('some_file.txt')

        assert len(messages) == 2

        message = messages[0]
        assert message.sender == 'Lou'
        assert message.body == 'did you see the thing i sent u?'
        assert message.when_created == datetime(2015, 2, 10, 18, 3)
        assert False
            