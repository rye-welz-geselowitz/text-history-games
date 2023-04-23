from message import Message 
from typing import List, Callable, Optional, Set
from enum import Enum 
from dataclasses import dataclass 
import random 
from parsers import WhatsappParser, GoogleParser

class Theme(Enum):
    ALL = 'ALL'
    LONG = 'LONG'

class DisplayTheme(Enum):
    STANDARD = 'STANDARD'
    EMPHASIZED_PRIMARY = 'EMPHASIZED_PRIMARY'
    EMPHASIZED_SECONDARY = 'EMPHASIZED_SECONDARY'

@dataclass 
class TextElement:
    text: str 
    display_theme: DisplayTheme = DisplayTheme.STANDARD

LINE_BREAK = TextElement(text='')

@dataclass 
class MenuOption:
    text: str 
    get_next_state: Callable[[], 'State']
    accepted_values: Optional[Set[str]] = None

@dataclass
class State:
    text_elements: List[TextElement]
    menu_options: List[MenuOption]

@dataclass
class IndexedMessage:
    message: Message
    idx: int

class FileInputConfig:
    pass

@dataclass 
class WhatsappFileConfig(FileInputConfig):
    participant1: str 
    participant2: str 
    filename: str 

@dataclass 
class GoogleFileConfig(FileInputConfig):
    filename: str 

class GameEngine:
    def __init__(self, file_input_configs: List[FileInputConfig]) -> None: 
        self._indexed_messages = GameEngine._get_indexed_messages_from_files(file_input_configs)
    
    @staticmethod
    def _get_indexed_messages_from_files(file_input_configs: List[FileInputConfig]) -> List[IndexedMessage]:
        all_messages = []

        google_parser = GoogleParser()

        for file_input_config in file_input_configs:
            if isinstance(file_input_config, WhatsappFileConfig):
                whatsapp_parser = WhatsappParser(
                    [file_input_config.participant1,
                    file_input_config.participant2]
                )
                all_messages += whatsapp_parser.parse_file(file_input_config.filename)
            elif isinstance(file_input_config, GoogleFileConfig):
                all_messages+= google_parser.parse_file(
                    file_input_config.filename) 

        sorted_messages = sorted(all_messages, key=lambda m: m.when_created)
        return [
            IndexedMessage(message=message, idx=idx)
            for idx, message in enumerate(sorted_messages)
        ]

    def get_next_state(self) -> State:
        return self._get_choose_theme_state()
    
    def _get_choose_theme_state(self) -> State:
        formatted_message_count = '{:,}'.format(len(self._indexed_messages))
        return State(
            text_elements=[
                TextElement('Guess who sent which text, and when!', display_theme=DisplayTheme.EMPHASIZED_PRIMARY),
                LINE_BREAK,
                TextElement(
                    f'This game includes {formatted_message_count} texts '
                    f'sent between {self._indexed_messages[0].message.when_created.date()} '
                    f'and {self._indexed_messages[-1].message.when_created.date()}!'
                ),
                LINE_BREAK,
                TextElement(text='Choose a theme!', display_theme=DisplayTheme.EMPHASIZED_SECONDARY)
            ],
            menu_options=[
                MenuOption(
                    text='A: All messages',
                    accepted_values={'a', 'A'},
                    get_next_state=lambda:  self._set_filter_and_get_next_state(filter_func=lambda message: True)
                ),
                MenuOption(
                    text='B: Long messages',
                    accepted_values={'b', 'B'},
                    get_next_state=lambda: self._set_filter_and_get_next_state(filter_func=lambda message: len(message.body) > 50)
                )
            ]
        )
    
    def _set_filter_and_get_next_state(self, filter_func: Callable[[Message], bool]) -> State:
        filtered_messages = [
            indexed_message for indexed_message
            in self._indexed_messages if filter_func(indexed_message.message)
        ]
        if len(filtered_messages) == 0:
            return State(
                text_elements=[TextElement('Oops, there are no messages fitting that filter!')],
                menu_options=[
                    MenuOption(
                        text='Try again?',
                        get_next_state=lambda: self._get_choose_theme_state()
                    )
                ]
            )
        self._filtered_messages = filtered_messages
        return self._get_obscured_message_state()

    def _get_obscured_message_state(self) -> State:
        random_message = random.choice(self._filtered_messages)
        return State(
            text_elements=[TextElement(
                random_message.message.body,
                display_theme=DisplayTheme.EMPHASIZED_PRIMARY
            )],
            menu_options=[
                    MenuOption(
                    text='Reveal?',
                    get_next_state=lambda: self._get_revealed_message_state(random_message)
                )
            ]
        )
    
    def _get_revealed_message_state(self, selected_message: IndexedMessage) -> State:
        min_bound = max(selected_message.idx - 2, 0)
        max_bound = min(selected_message.idx + 3, len(self._indexed_messages))
        text_elements = []
        for i in range(min_bound, max_bound):
            display_theme = DisplayTheme.EMPHASIZED_PRIMARY if i == selected_message.idx else DisplayTheme.STANDARD
            message = self._indexed_messages[i].message
            for message_display_part in [
                str(message.when_created),
                message.sender,
                message.body
            ]:
                text_elements.append(
                    TextElement(
                        text=message_display_part,
                        display_theme=display_theme
                    )
                )
            text_elements.append(LINE_BREAK)

        return State(
            text_elements=text_elements,
            menu_options=[
                MenuOption(
                    text='Continue?',
                    get_next_state=lambda: self._get_obscured_message_state()
                )
            ]        
        )
            



        

    