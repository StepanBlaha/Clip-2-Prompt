import pystray
from PIL import Image

from ai_handler import ai_on, ai_off
from language import set_lang
from clipboard_copy import copy_on, copy_off
from utils import exit_script

def create_menu():
    """
    Creates a system tray menu
    """
    # Get all the items for the menu
    copy_on_item = pystray.MenuItem("Copy on", copy_on)
    copy_off_item = pystray.MenuItem("Copy off", copy_off)
    ai_on_item = pystray.MenuItem("AI on", lambda icon, item: ai_on())
    ai_off_item = pystray.MenuItem("AI off", ai_off)
    exit_script_item = pystray.MenuItem("Exit", exit_script)
    summary_item = pystray.MenuItem("AI summary mode", lambda icon, item: ai_on(summary=True))
    translate_item = pystray.MenuItem("AI Translate mode", lambda icon, item: ai_on(translate=True))
    set_language_item = pystray.MenuItem("Set language", set_lang)
    # Create the menu
    menu = (copy_on_item, copy_off_item, ai_on_item, ai_off_item, summary_item, translate_item, set_language_item, exit_script_item)
    try:
        image = Image.open('icon.png')
    except FileNotFoundError:
        print("Warning: icon.png not found. Using default.")
        image = Image.new("RGB", (64, 64), color="gray")
        
    icon = pystray.Icon("main", image, "Clip-2-Prompt", menu)
    icon.run()