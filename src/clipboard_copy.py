import pyperclip
import threading
import time

from config import app_state

def get_new_clipboard(last_text):
    """Get new clipboard text

    Args:
        last_text (string): last text from clipboard
    """
    text = pyperclip.paste().strip()
    return text if text and text != last_text else None

def copy_on():
    """
    Starts the copy mode
    """
    # Set the flags for modes
    app_state["ai_running"] = False
    app_state["copy_running"] = True
    app_state["lang_running"] = False
    app_state["summarize"] = False
    app_state["translate"] = False
    threading.Thread(target=copy_run, daemon=True).start()
    print("Starting copy mode...")

def copy_off():
    """
    Stops the copy mode
    """
    app_state["copy_running"] = False
    print('Exiting copy mode...')

def copy_run():
    """
    Copy loop
    """ 
    last_text = ""

    while app_state["copy_running"]:
        copied_text = get_new_clipboard(last_text)
        # Make sure the clipboard isnt empty and same as the last one
        if not copied_text:
            time.sleep(1)
            continue

        # Update last test
        last_text = copied_text

        # Write into file
        with open(app_state["user_log_file"], "a") as f:
            f.write(copied_text + '\n')

        # Timeout
        time.sleep(1)
        
        