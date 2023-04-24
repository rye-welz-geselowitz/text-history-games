from unittest.mock import patch, mock_open
from parsers.whatsapp import WhatsappParser
from datetime import datetime

READ_DATA = """12/13/18, 5:27 AM - Banana Fred: Totally up for that!
12/13/18, 5:28 AM - Pineapple: would you go home after, or... ?
12/13/18, 5:28 AM - Banana Fred: Probably? Not sure"""

class TestParseFile:
    def test_parses_file(self):
        parser = WhatsappParser(['Banana Fred', 'Pineapple'])

        with patch("parsers.whatsapp.open", mock_open(read_data=READ_DATA)):
            messages = parser.parse_file('some_file.txt')

        assert len(messages) == 3 

        message = messages[0]
        assert message.sender == 'Banana Fred'
        assert message.body == 'Totally up for that!'
        assert message.when_created == datetime(2018, 12, 13, 5, 27)
            