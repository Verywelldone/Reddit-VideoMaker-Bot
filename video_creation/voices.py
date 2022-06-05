from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track
import pyttsx3
from pydub import AudioSegment
import re

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    print_step("Saving Text to MP3 files 🎶")
    length = 0

    oldpath = re.sub("[!@#$%^&*()[]{};:,. <>?\|'`~-=_+'/]", "", reddit_obj["thread_title"])
    path = ''.join(ch for ch in oldpath if ch.isalnum())


    # Create a folder for the mp3 files.
    Path("assets/{}/mp3".format(path)).mkdir(parents=True, exist_ok=True)


    engine.save_to_file(text= reddit_obj["thread_title"], filename="assets/{}/mp3/title.mp3".format(path))
    engine.runAndWait()
    # tts = gTTS(text=reddit_obj["thread_title"], lang="en", slow=False, tld="co.uk")
    # tts.save(f"assets/mp3/title.mp3")

    audio = AudioSegment.from_file("assets/{}/mp3/title.mp3".format(path))
    length += audio.duration_seconds

    for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 50 seconds. This can be longer, but this is just a good starting point
        if length > 40:
            break

        engine.save_to_file(comment["comment_body"],"assets/{}/mp3/{}.mp3".format(path,idx))
        engine.runAndWait()
        # tts = gTTS(text=comment["comment_body"], lang="en")
        # tts.save(f"assets/mp3/{idx}.mp3")
        audio = AudioSegment.from_file("assets/{}/mp3/{}.mp3".format(path,idx))
        length += audio.duration_seconds
        # length += MP3(f"assets/mp3/{idx}.mp3").info.length

    print_substep("Saved Text to MP3 files Successfully.", style="bold green")
    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
