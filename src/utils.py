import time
import os

def exit_script(icon=None, item=None):
    """
    Exits script
    """
    print("Script closing...")
    if icon is not None:
        icon.stop()
        time.sleep(1)  
    os._exit(0)  