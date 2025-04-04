import pyperclip
import threading
import time

from config import app_state

def set_lang():
    """
    Set the language for translation
    """
    # Set the flags for modes
    app_state["lang_running"] = True
    app_state["copy_running"] = False
    app_state["ai_running"] = False
    app_state["summarize"] = False
    
    pyperclip.copy("")
    threading.Thread(target=lang_run, daemon=True).start()
    print("Setting language...")
    
def lang_run():
    """
    Loop for setting language for translating
    """
    while app_state["lang_running"]:
        copied_text = pyperclip.paste().strip()
        # Make sure the clipboard isnt empty
        if not copied_text:
            time.sleep(1)
            continue
        # Set the language for translation
        app_state["language"] = copied_text
        print(f"Language set to {copied_text}")
        app_state["lang_running"] = False
        break
