# Clip-2-Prompt
Tool for copying text to file without having to paste it

## Functions
- Copy mode - copy straight to file without pasting
- AI mode - Make hidden calls to chatgpt
- AI summary mode - Get ai summary of copied code
- AI translate mode - Translate copied text to desired language
- Hotkeys - Create custom hotkeys for the different modes
- Windows system tray menu - For easy access if you dont want to use hotkeys

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
Open config.py file and replace "OPENAI_KEY" with you key
```
api_key = os.getenv("OPENAI_KEY")
```
If you want you can change the output file for copy mode in config.py by changing "user_log_file": "sample.txt":
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
