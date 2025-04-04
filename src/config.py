import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_KEY")

app_state = {
    "copy_running": False,
    "user_log_file": "sample.txt",
    "ai_running": False,
    "summarize": False,
    "translate": False,
    "language": "en",
    "lang_running": False,
}
