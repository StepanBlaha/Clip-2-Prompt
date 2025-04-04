from pynput import keyboard

from ai_handler import ai_on, ai_off
from language import set_lang
from clipboard_copy import copy_on, copy_off
from utils import exit_script

def create_hotkeys():
    # Set your custom hotkeys
    hotkeys = {
        '<ctrl>+<alt>+h': copy_on,  # Start copy mode
        '<ctrl>+<alt>+q': copy_off, # Stop copy mode
        '<ctrl>+<alt>+g': exit_script, # Exit script
        '<ctrl>+<alt>+j': ai_on, # Start ai mode
        '<ctrl>+<alt>+e': ai_off, # Stop ai mode
        '<ctrl>+<alt>+k': lambda: ai_on(summary=True), # Start ai with summary mode
        '<ctrl>+<alt>+l': lambda: ai_on(translate=True), # Start ai with translate mode
        '<ctrl>+<alt>+n': set_lang, # Sets the language for translation
    }
    # Start the hotkey listener
    with keyboard.GlobalHotKeys(hotkeys) as listener:
        listener.join()