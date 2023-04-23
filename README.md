# Text Explorer
A command-line game. Upload your texting history with a friend (supports WhatsApp and Google). The game will prompt you with an out-of-context text; guess the date, sender identity, and context.

![Screen recording of the game](https://github.com/rye-welz-geselowitz/text-history-games/blob/main/readme-screen-recording.gif?raw=true)

## Run the game!
Create virtual env:
```
python3 -m venv text-history-games-env
```

Activate virtual env:

```
source text-history-games-env/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```
Run game:
```
python3 -m game
```

## Dev notes 
For type checking:
```
mypy game.py
```

### TODOS
Unit tests! 