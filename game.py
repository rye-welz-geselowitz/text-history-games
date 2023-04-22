from typing import List, Optional
import random
import os
from time import sleep
from dataclasses import dataclass
from engine.message import Message
from termcolor import cprint
from engine.parsers import WhatsappParser, GoogleParser

@dataclass 
class WhatsappConfig:
    participant1: str 
    participant2: str 
    filename: str 

@dataclass 
class GoogleConfig:
    filename: str 

WHATSAPP_CONFIG = WhatsappConfig(
    participant1='Lou',
    participant2='Elektra',
    filename='sample_data/whatsapp.txt'
)

GOOGLE_CONFIG = GoogleConfig(filename='sample_data/google.json')


LONG_MESSAGE_MIN_WORDS = 50
LOVE_KEYWORDS = ['love you', 'in love with you', 'proud of you', 'care about you']

def has_keyword(message, keywords):
    for keyword in keywords:
        if keyword.lower() in message.body.lower():
            return True
    return False

THEMES_TO_FILTERS = {
    'love': lambda message: has_keyword(message, LOVE_KEYWORDS),
    'long': lambda message: len(message.body.split(' ')) >  LONG_MESSAGE_MIN_WORDS,
    'all': lambda message: message.body != '<Media omitted>',
}

@dataclass
class IndexedMessage:
    message: Message
    idx: int

def run(
    whatsapp_config: Optional[WhatsappConfig],
    google_config: Optional[GoogleConfig]
) -> None:
    os.system('color')
    os.system('clear')
    print('loading!')

    whatsapp_messages = WhatsappParser(
        [whatsapp_config.participant1, whatsapp_config.participant2]
    ).parse_file(whatsapp_config.filename) if whatsapp_config else []

    google_messages = GoogleParser().parse_file(
        google_config.filename) if google_config else []

    messages = sorted(whatsapp_messages + google_messages, key=lambda m: m.when_created)
    os.system('clear')


    formatted_count = '{:,}'.format(len(messages))
    cprint('Guess who sent which text, and when!', 'cyan')
    print(f'This game includes {formatted_count} texts '
        f'sent between {messages[0].when_created.date()} and {messages[-1].when_created.date()}!\n\n')

    filter_func = THEMES_TO_FILTERS['all']
    while True:
        theme = input(f'➡️    Choose a theme: {", ".join(THEMES_TO_FILTERS.keys())}, custom word search\n\n')
        if theme == 'custom word search':
            keywords = input('\n\nPlease enter keywords, separated by commas:\n\n')
            parsed_keywords = [keyword.strip() for keyword in keywords.split(',')]
            filter_func = lambda message: has_keyword(message, parsed_keywords)
            break
        if theme.lower() in THEMES_TO_FILTERS.keys():
            filter_func = THEMES_TO_FILTERS[theme.lower()]
            break
        else:
            print('That is not a valid theme!')

    filtered_messages = [IndexedMessage(message=message, idx=idx)
        for idx, message in enumerate(messages) if filter_func(message)]

    os.system('clear')
    print(f'\n\n{len(filtered_messages)} messages fit this theme. Here we go!!!')
    # TODO: handle case where no messages fit theme
    sleep(2)
    os.system('clear')

    # TODO: extract into engine
    while True:
        os.system('clear')
        random_message = random.choice(filtered_messages)
        print(f'\n\n{random_message.message.body}')
        _ = input('\n\nReveal?!')
        os.system('clear')
        min_bound = max(random_message.idx - 2, 0)
        max_bound = min(random_message.idx + 3, len(messages))

        for i in range(min_bound, max_bound):
            color = 'magenta' if i == random_message.idx else 'white'
            for output in [f'\n{messages[i].when_created}', messages[i].sender, messages[i].body]:
                cprint(output, color)

        _ = input('\n\nConinue?!')
        os.system('clear')

if __name__ == "__main__":
    run(WHATSAPP_CONFIG, GOOGLE_CONFIG)
