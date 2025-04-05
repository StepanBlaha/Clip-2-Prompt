# Clip-2-Prompt :clipboard:
Easy to use tool for when you need a bit of help... :smirk:<br>
Make secret ai calls, translate and summarize copied text or just copy clipboard straight to a file.<br>

## Functions
- Copy mode - copy straight to file without pasting
- AI mode - Make hidden calls to chatgpt
- AI summary mode - Get ai summary of copied code :sparkles:
- AI translate mode - Translate copied text to desired language :speech_balloon:
- Hotkeys - Create custom hotkeys for the different modes
- Windows system tray menu - For easy access if you dont want to use hotkeys :pushpin:
 
## Requirements
- Open AI API key

## Instalation Guide
```
git clone https://github.com/StepanBlaha/Clip-2-Prompt/
cd Clip-2-Prompt
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Open config.py file and replace "OPENAI_KEY" with your key :key::
```
api_key = os.getenv("OPENAI_KEY")
```
If you want you can change the output file :file_folder: for copy mode in config.py by changing "user_log_file": "sample.txt":
```
app_state = {
    "copy_running": False,
    "user_log_file": "sample.txt",
    "ai_running": False,
    "summarize": False,
    "translate": False,
    "language": "en",
    "lang_running": False,
}
```
You can also create custom hotkeys in hotkeys.py:
```
 hotkeys = {
        '<ctrl>+<alt>+h': copy_on,
        '<ctrl>+<alt>+q': copy_off,
        '<ctrl>+<alt>+g': exit_script,
        '<ctrl>+<alt>+j': ai_on,
        '<ctrl>+<alt>+e': ai_off,
        '<ctrl>+<alt>+k': lambda: ai_on(summary=True),
        '<ctrl>+<alt>+l': lambda: ai_on(translate=True),
        '<ctrl>+<alt>+n': set_lang,
    }
```

## To run
```
python src/main.py
```

## Usage 
### Copy mode :clipboard:
- Copy text from clipboard to desired file
- To start run copy_on (Copy mode off hotkey or menu button)
- To end run copy_off (Copy mode off hotkey or menu button)

### AI mode :bulb:
- Send text from clipboard to Chatgpt and get the response back to clipboard
- To start run ai_on (AI mode on hotkey or menu button)
- To end run ai_off (AI mode off hotkey or menu button)

### Summary mode :bookmark_tabs:
- Send text from clipboard to Chatgpt and get the summary of it back to clipboard
- To start run ai_on in summary mode (Summary mode on hotkey or menu button)
- To end run ai_off (AI mode off hotkey or menu button)

### Translate mode :speech_balloon:
- Send text from clipboard to Chatgpt and get the translation of it back to clipboard
- To setup language run set_lang and copy a language you want to translate into (Set language hotkey or menu button)
- To start run ai_on in translate mode (Translate mode on hotkey or menu button)
- To end run ai_off (AI mode off hotkey or menu button)

### Script exit :x:
- To end the script either press the exit script hotkey or button
