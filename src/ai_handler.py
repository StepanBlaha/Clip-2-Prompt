from openai import OpenAI
import pyperclip
import threading
import time


from config import api_key, app_state
from clipboard_copy import get_new_clipboard

client = OpenAI(api_key=api_key,)

def ai_message(message):
    """Call to chatgpt

    Args:
        message (string): Message to send to chatgpt
        sumary (bool, optional): If True, it will summarize the message. Defaults to False.

    Returns:
        string: Chatgpt reply
    """
    if app_state["summarize"]:
        role_message = "Summarize the text i send you into easy to understan article" 
    elif app_state["translate"]:
        role_message = f"Translate the text i send you to {app_state['language']} language"
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

def ai_on(summary=False, translate=False):
    """
    Starts the AI mode
    
    Args:
        summary (bool, optional): If True, it will summarize the message. Defaults to False.
    """
    if app_state["ai_running"]:
        print("AI mode is already running")
        ai_off()
    # Set flags for all the modes
    app_state["copy_running"] = False
    app_state["ai_running"] = True
    app_state["summarize"] = summary
    app_state["translate"] = translate
    app_state["lang_running"] = False
    # Clear clipboard
    pyperclip.copy("")
    # Run AI in a separate thread
    threading.Thread(target=ai_run, daemon=True).start()
    
    # Debug
    if app_state["summarize"] == True:
        print("Summary mode starting...")
    if app_state["translate"]:
        print(f"Translate mode starting... {app_state['language']}")
    else:
        print("AI mode starting...")

def ai_off():
    """
    Stops the AI mode
    """
    # Stop summary mode
    app_state["summarize"] = False
    app_state["translate"] = False
    # Stop AI mode
    app_state["ai_running"] = False
    print('Exiting AI mode...')

def ai_run():
    """
    AI loop
    """
    print("AI running...")
    last_text = ""
    ai_response = ""
    while app_state["ai_running"]:
        copied_text = get_new_clipboard(last_text)
        # Make sure to not send ai reply back to ai nd that copied text is not empty
        if not copied_text or copied_text == ai_response:
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
