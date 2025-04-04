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
}

def ai_message(message):
    """Call to chatgpt

    Args:
        message (string): Message to send to chatgpt

    Returns:
        sting: Chatgpt reply
    """
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Tell me only the answer without any go arounds. If i send code or ask for code send only the code"
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

def ai_on():
    """
    Starts the AI mode
    """
    app_dict["copy_running"] = False
    app_dict["ai_running"] = True
    threading.Thread(target=ai_run, daemon=True).start()
    print("Starting AI mode...")

def ai_off():
    """
    Stops the AI mode
    """
    app_dict["ai_running"] = False
    print('Exiting AI mode...')

def ai_run():
    """
    AI loop
    """
    print("AI running...")
    last_text = ""

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

        # Update last test
        last_text = copied_text

        # Get ai response
        ai_response = ai_message(copied_text)

        pyperclip.copy(ai_response)
        # Timeout
        time.sleep(1)

def copy_on():
    """
    Starts the copy mode
    """
    app_dict["ai_running"] = False
    app_dict["copy_running"] = True
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
        '<ctrl>+<alt>+h': copy_on,
        '<ctrl>+<alt>+q': copy_off,
        '<ctrl>+<alt>+g': exit_script,
        '<ctrl>+<alt>+j': ai_on,
        '<ctrl>+<alt>+e': ai_off,
    }
    with keyboard.GlobalHotKeys(hotkeys) as listener:
        listener.join()

if __name__ == "__main__":
    run()


