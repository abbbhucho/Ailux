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

def main():
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
        user_input = input(" You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            bash_cmd = get_shell_command(user_input)
            print(f"Suggested Bash: {bash_cmd}")

            # Check for dangerous commands
            if is_dangerous(bash_cmd):
                print(" Warning: This command is flagged as potentially dangerous!")

            run = input(" Do you want to run this command? (y/n): ")
            if run.lower() == 'y':
                if SAFE_MODE and is_dangerous(bash_cmd):
                    print("The command is blocked by SAFE_MODE. Admin has disabled risky command execution.")
                    log_command(user_input, bash_cmd, "BLOCKED by SAFE_MODE")
                else:
                    subprocess.run(bash_cmd, shell=True)
                    log_command(user_input, bash_cmd, "EXECUTED")
            else:
                log_command(user_input, bash_cmd, "SKIPPED")
        except Exception as e:
            print(f"Error: {e}")
            log_command(user_input, "N/A", f"ERROR: {e}")
    # print("Welcome to AI Linux Shell Helper ")
    # print("Type your natural language command (or 'exit' to quit):\n")

    # while True:
    #     user_input = input(" You: ")
    #     if user_input.lower() in ["exit", "quit"]:
    #         break
    #     try:
    #         bash_cmd = get_shell_command(user_input)
    #         print(f" Suggested Bash: {bash_cmd}")
    #     except Exception as e:
    #         print(f" Could not parse input: {e}")

    # run = input(" Do you want to run this command? (y/n): ")
    # if run.lower() == 'y':
    #     SAFE_MODE = True
    #     if not SAFE_MODE:
    #         subprocess.run(bash_cmd, shell=True)

if __name__ == "__main__":
    main()