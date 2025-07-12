import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Get SAFE_MODE from .env
SAFE_MODE = os.getenv("SAFE_MODE", "True").lower() == "true"

# Define basic safe/dangerous patterns
SAFE_COMMANDS = [
    "ls", "cat", "echo", "find", "ps", "du", "pwd", "whoami", "date"
]

DANGEROUS_KEYWORDS = [
    "rm", "kill", "pkill", "reboot", "shutdown", "chmod", "chown", "dd", "mv", "rmdir", "wipefs"
]

def is_dangerous(cmd: str) -> bool:
    cmd = cmd.lower()
    return any(danger in cmd for danger in DANGEROUS_KEYWORDS)