# Built-in modules
import threading
# Modules from the project
from hotkeys import create_hotkeys
from menu import create_menu

def run():
    # Create a thread for the menu to avoid blocking the main thread
    threading.Thread(target=create_menu, daemon=True).start()
    # Start the hotkey listener
    create_hotkeys()

if __name__ == "__main__":
    run()
