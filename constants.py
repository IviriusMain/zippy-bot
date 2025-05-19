import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENVIRONMENT") == "TESTING":
    TOKEN = os.environ["TOKEN_TEST"]
else:
    TOKEN = os.environ["TOKEN"]
