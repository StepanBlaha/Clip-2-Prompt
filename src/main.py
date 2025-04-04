import pyperclip
import time
import os
from pynput import mouse, keyboard
import time
import threading
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values


load_dotenv()
api_key = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=api_key,
)


app_dict = {
    "copy_running": False,
    "user_inp": "tt.txt",
    "ai_running": False,
    "summarize": False,
    "translate": False,
    "language": "en",
    "lang_running": False,
}
def set_lang():
    """
    Set the language for translation
    """
    # Set the flags for modes
    app_dict["lang_running"] = True
    app_dict["copy_running"] = False
    app_dict["ai_running"] = False
    app_dict["summarize"] = False
    
    pyperclip.copy("")
    threading.Thread(target=lang_run, daemon=True).start()
    print("Setting language...")
    
def lang_run():
    """
    Loop for setting language for translating
    """
    while app_dict["lang_running"]:
        copied_text = pyperclip.paste().strip()
        # Make sure the clipboard isnt empty
        if not copied_text:
            time.sleep(1)
            continue
        # Set the language for translation
        app_dict["language"] = copied_text
        print(f"Language set to {copied_text}")
        app_dict["lang_running"] = False
        break

def ai_message(message):
    """Call to chatgpt

    Args:
        message (string): Message to send to chatgpt
        sumary (bool, optional): If True, it will summarize the message. Defaults to False.

    Returns:
        string: Chatgpt reply
    """
    if app_dict["summarize"]:
        role_message = "Summarize the text i send you into easy to understan article" 
    elif app_dict["translate"]:
        role_message = f"Translate the text i send you to {app_dict['language']} language"
    else:
        role_message = "Tell me only the answer without any go arounds. If i send code or ask for code send only the code"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": role_message
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content

def exit_script():
    """
    Exits script
    """
    print("Script closing...")
    exit()

def ai_on(summary=False, translate=False):
    """
    Starts the AI mode
    
    Args:
        summary (bool, optional): If True, it will summarize the message. Defaults to False.
    """
    if app_dict["ai_running"]:
        print("AI mode is already running")
        return
    # Set flags for all the modes
    app_dict["copy_running"] = False
    app_dict["ai_running"] = True
    app_dict["summarize"] = summary
    app_dict["translate"] = translate
    app_dict["lang_running"] = False
    # Clear clipboard
    pyperclip.copy("")
    # Run AI in a separate thread
    threading.Thread(target=ai_run, daemon=True).start()
    
    # Debug
    if app_dict["summarize"]:
        print("Summary mode starting...")
    elif app_dict["translate"]:
        print(f"Translate mode starting... {app_dict['language']}")
    else:
        print("AI mode starting...")

def ai_off():
    """
    Stops the AI mode
    """
    # Stop summary mode
    app_dict["summarize"] = False
    # Stop AI mode
    app_dict["ai_running"] = False
    print('Exiting AI mode...')

def ai_run():
    """
    AI loop
    """
    print("AI running...")
    last_text = ""
    ai_response = ""
    while app_dict["ai_running"]:
        copied_text = pyperclip.paste().strip()
        # Make sure the clipboard isnt empty
        if not copied_text:
            time.sleep(1)
            continue
        # Make sure the clipboard content isnt the same
        if copied_text == last_text:
            time.sleep(1)
            continue
        # Make sure to not send ai reply back to ai
        if copied_text == ai_response:
            time.sleep(1)
            continue

        # Update last test
        last_text = copied_text

        # Get ai response
        ai_response = ai_message(copied_text)

        pyperclip.copy(ai_response)
        
        # Debug
        print(f"[Clipboard IN]: {copied_text[:40]}")
        print(f"[AI OUT]: {ai_response[:40]}")
        # Timeout
        time.sleep(1)

def copy_on():
    """
    Starts the copy mode
    """
    # Set the flags for modes
    app_dict["ai_running"] = False
    app_dict["copy_running"] = True
    app_dict["lang_running"] = False
    app_dict["summarize"] = False
    app_dict["translate"] = False
    threading.Thread(target=copy_run, daemon=True).start()
    print("Starting copy mode...")

def copy_off():
    """
    Stops the copy mode
    """
    app_dict["copy_running"] = False
    print('Exiting copy mode...')

def copy_run():
    """
    Copy loop
    """ 
    last_text = ""

    while app_dict["copy_running"]:
        copied_text = pyperclip.paste().strip()
        # Make sure the clipboard isnt empty
        if not copied_text:
            time.sleep(1)
            continue
        # Make sure the clipboard content isnt the same
        if copied_text == last_text:
            time.sleep(1)
            continue

        # Update last test
        last_text = copied_text

        # Write into file
        with open(app_dict["user_inp"], "a") as f:
            f.write(copied_text + '\n')

        # Timeout
        time.sleep(1)


def run():
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
    with keyboard.GlobalHotKeys(hotkeys) as listener:
        listener.join()

if __name__ == "__main__":
    run()


