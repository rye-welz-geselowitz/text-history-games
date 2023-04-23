from message import Message 
from typing import List, Callable, Optional, Set
from enum import Enum 
from dataclasses import dataclass 
import random 
from parsers import WhatsappParser, GoogleParser

class DisplayColor(Enum):
    """ Enum representing the color in which to display an element """
    STANDARD = 'STANDARD'
    EMPHASIZED_PRIMARY = 'EMPHASIZED_PRIMARY'
    EMPHASIZED_SECONDARY = 'EMPHASIZED_SECONDARY'

@dataclass 
class TextElement:
    """ Dataclass representing a text element to display """
    text: str 
    display_theme: DisplayColor = DisplayColor.STANDARD

LINE_BREAK = TextElement(text='')

@dataclass 
class MenuOption:
    """ Dataclass representing a menu option """
    text: str 
    get_next_state: Callable[[], 'State']
    # `accepted_values` expresses the list of values that trigger this
    # menu option to be chosen. If None, any input is sufficient to pass to
    # the next state. 
    # TODO: What I think I really want is a behavior where any keystroke causes 
    # the game to pass to the next state (rather than the current behavior, in which 
    # any combination of key strokes ending in the "return" button accomplishes that).
    # I would like to rethink this interface and also update the renderer to handle this 
    # new behavior.
    accepted_values: Optional[Set[str]] = None

    # TODO: Add a __post_init__ method validating that, if there is any menu option 
    # with accepted_values = None, then it is the only such menu option.

@dataclass
class State:
    """ Dataclass representing game state, i.e. the text and menu options 
    to render to the player """
    text_elements: List[TextElement]
    menu_options: List[MenuOption]

@dataclass
class IndexedMessage:
    """ Dataclass representing a message, together with its index in
    an ordered list of messages """
    message: Message
    idx: int

class FileInputConfig:
    """ Base class for representing configuration for a file from which 
    to parse messages """
    pass

@dataclass 
class WhatsappFileConfig(FileInputConfig):
    """ Configuration for a Whatsapp chat history file from which to parse 
    messages """
    participant1: str 
    participant2: str 
    filename: str 

@dataclass 
class GoogleFileConfig(FileInputConfig):
    """ Configuration for a Google chat history file from which to parse 
    messages """
    filename: str 

class GameEngine:
    """ Engine for a game in which players are asked to guess the datem, sender and 
    context of text messages from their chat history. """
    def __init__(self, file_input_configs: List[FileInputConfig]) -> None: 
        self._indexed_messages = GameEngine._get_indexed_messages_from_files(file_input_configs)
    
    def get_next_state(self) -> State:
        """ Returns the next state for the game """
        return self._get_choose_theme_state()

    @staticmethod
    def _get_indexed_messages_from_files(file_input_configs: List[FileInputConfig]) -> List[IndexedMessage]:
        """ 
        Arguments:
            file_input_configs (List[FileInputConfig]): A list of dataclasses representing 
                files from which to parse the messages on which this game is based 
        Returns:
            A list of datclasses (IndexedMessage) representing parsed messages    
        """
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
    
    def _get_choose_theme_state(self) -> State:
        """ Returns an instance of State prompting the player to choose a theme """
        formatted_message_count = '{:,}'.format(len(self._indexed_messages))
        return State(
            text_elements=[
                TextElement('Guess who sent which text, and when!', display_theme=DisplayColor.EMPHASIZED_PRIMARY),
                LINE_BREAK,
                TextElement(
                    f'This game includes {formatted_message_count} texts '
                    f'sent between {self._indexed_messages[0].message.when_created.date()} '
                    f'and {self._indexed_messages[-1].message.when_created.date()}!'
                ),
                LINE_BREAK,
                TextElement(text='Choose a theme!', display_theme=DisplayColor.EMPHASIZED_SECONDARY)
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
        """ Filters messages by the chosen theme and returns a state prompting the player 
        to guess the context of a text message """
        filtered_messages = [
            indexed_message for indexed_message
            in self._indexed_messages if filter_func(indexed_message.message)
        ]
        if len(filtered_messages) == 0:
            return State(
                # TODO: Ideally we wouldn't show an option at all in the first place 
                # if we already know there are no messages fitting that filter! 
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
        """ Returns a state prompting the player 
        to guess the context of a text message """
        # TODO: Currently a message can be selected multiple times, would be 
        # nice to update random choice logic so that a message appears at most 
        # once during a run of the game.
        random_message = random.choice(self._filtered_messages)
        return State(
            text_elements=[TextElement(
                random_message.message.body,
                display_theme=DisplayColor.EMPHASIZED_PRIMARY
            )],
            menu_options=[
                    MenuOption(
                    text='Reveal?',
                    get_next_state=lambda: self._get_revealed_message_state(random_message)
                )
            ]
        )
    
    def _get_revealed_message_state(self, selected_message: IndexedMessage) -> State:
        """ Returns a state revealing the context of a previously displayed message """
        min_bound = max(selected_message.idx - 2, 0)
        max_bound = min(selected_message.idx + 3, len(self._indexed_messages))
        text_elements = []
        for i in range(min_bound, max_bound):
            display_theme = DisplayColor.EMPHASIZED_PRIMARY if i == selected_message.idx else DisplayColor.STANDARD
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
            



        

    