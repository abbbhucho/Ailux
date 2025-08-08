from shell_nlp import get_shell_command
from safe_config import SAFE_MODE, is_dangerous
import subprocess
from datetime import datetime
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "command_log.log")

def log_command(nl_input, command, status):
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{datetime.now()}] Input: \"{nl_input}\"\n")
        log_file.write(f"  → Command: {command}\n")
        log_file.write(f"  → Status: {status}\n\n")

def ai_shell():
    print(
        """
         █████  ██ ██      ██    ██ ██   ██ 
        ██   ██ ██ ██      ██    ██  ██ ██  
        ███████ ██ ██      ██    ██   ███   
        ██   ██ ██ ██      ██    ██  ██ ██  
        ██   ██ ██ ███████  ██████  ██   ██ 
                                            

    """
    )
    print(f" SAFE_MODE is {'ON' if SAFE_MODE else 'OFF'} (set in .env)\n")
    while True:
        user_input = input(" ai-shell$ ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break

        try:
            bash_cmd = get_shell_command(user_input)
            print(f" Interpreted: {bash_cmd}")

            if is_dangerous(bash_cmd):
                print("  This command is flagged as dangerous!")

            run = input("  Run this? (y/n): ")
            if run.lower() == 'y':
                if SAFE_MODE and is_dangerous(bash_cmd):
                    print(" Blocked by SAFE_MODE")
                    log_command(user_input, bash_cmd, "BLOCKED by SAFE_MODE")
                else:
                    subprocess.run(bash_cmd, shell=True)
                    log_command(user_input, bash_cmd, "EXECUTED")
            else:
                log_command(user_input, bash_cmd, "SKIPPED")

        except Exception as e:
            print(f" Error: {e}")
            log_command(user_input, "N/A", f"ERROR: {e}")

def main():
    ai_shell()

if __name__ == "__main__":
    main()