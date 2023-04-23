from typing import List, Optional
from game_engine import GameEngine, WhatsappFileConfig, GoogleFileConfig, FileInputConfig, State
from renderer import GameRenderer

FILE_INPUT_CONFIGS = [
    WhatsappFileConfig(
        participant1='Lou',
        participant2='Elektra',
        filename='sample_data/whatsapp.txt'
    ),
    GoogleFileConfig(filename='sample_data/google.json')
]


def run(file_input_configs: List[FileInputConfig]) -> None:
    renderer = GameRenderer(
        standard_color='white',
        emphasized_primary_color='magenta',
        emphasized_secondary_color='cyan'
    )
    renderer.loading()

    engine = GameEngine(file_input_configs)

    state: Optional[State] = engine.get_next_state()
    while state:
        state = renderer.render_state_and_get_next(state)

if __name__ == "__main__":
    run(FILE_INPUT_CONFIGS)
