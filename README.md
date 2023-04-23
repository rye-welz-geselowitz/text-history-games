# Text Message Explorer
I created this **simple command line game as a way of exploring my own vast archive of personal text messages.** (Fun fact: Between 2015 and 2023, my partner and I exchanged more than 235,489 text messages!).

The premise is simple:
* Export your text messages (from a service such as WhatsApp or Google Chat - see instructions below)
* The game will prompt you with a random text message from your archive.
* Guess the sender, date, and context of the text message. 
    * _(This is an especially meaningful activity to share with the friend or loved one with whom the text messages were exchanged - discuss, reminisce, or get competitive in your guessing!)_
* When you're ready, the game will reveal the text message in context.

Here's a screen recording with some sample data:
![Screen recording of the game](https://github.com/rye-welz-geselowitz/text-history-games/blob/main/readme-screen-recording.gif?raw=true)


## Run the game!
⚠️ This project has been developed and tested to run in iTerm on Mac; it has not been tested against other terminals.

Export your own text messages history:
* From [WhatsApp](https://faq.whatsapp.com/1180414079177245/?cms_platform=android)
* From [Google Chat](https://support.google.com/chat/answer/10126829?hl=en)

Update the `game.py` script to include configuration for your own files (i.e. specify file name and other necessary metadata)

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
* Unit tests! 
* Organize files a bit more thoughtfully?