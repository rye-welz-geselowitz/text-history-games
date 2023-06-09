from game_engine import State, DisplayColor
import os
from termcolor import cprint # type: ignore
from typing import Optional 


# TODO: The os functions here (e.g. `os.clear`) are tested only on my own terminal set-up;
# I believe other terminals require different commands. Ideally I would write a base class with 
# abstract methods like `clear` and child classes for different environments, implementing those 
# methods as appropriate. Since this is mostly a project for personal use I've deprioritized this! 
class GameRenderer:
    """ Renders an instance of a game """
    def __init__(
        self,
        standard_color: str, 
        emphasized_primary_color: str,
        emphasized_secondary_color: str
    ):
        self.standard_color = standard_color
        self.emphasized_primary_color = emphasized_primary_color 
        self.emphasized_secondary_color = emphasized_secondary_color

    
    def loading(self) -> None:
        """ Displays a loading image """
        os.system('color')
        os.system('clear')
        print('Loading!')
    
    def _get_color_for_display_theme(self, display_theme: DisplayColor) -> str:
        return {
            DisplayColor.STANDARD: self.standard_color,
            DisplayColor.EMPHASIZED_PRIMARY: self.emphasized_primary_color,
            DisplayColor.EMPHASIZED_SECONDARY: self.emphasized_secondary_color
        }.get(display_theme, self.standard_color)

    def render_state_and_get_next(self, state: State) -> Optional[State]:
        """ Renders game state and returns the next state based on user input """
        os.system('clear')
        for text_element in state.text_elements:
            color = self._get_color_for_display_theme(text_element.display_theme)
            cprint(text_element.text, color)
        
        if not state.menu_options:
            return None 

        print()
        for menu_option in state.menu_options:
            cprint(menu_option.text)

        while True:
            print()
            user_input = input('>>> ')
            for menu_option in state.menu_options:
                if menu_option.accepted_values is None:
                    return menu_option.get_next_state()
                elif user_input.strip() in menu_option.accepted_values:
                    return menu_option.get_next_state()
            print(f'{user_input} is not a valid choice. Please try again: ')




        