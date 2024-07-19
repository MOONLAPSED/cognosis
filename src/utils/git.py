import datetime
import os
import subprocess


def git_commit_with_timestamp():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_message = f"Auto-commit at {timestamp}"

    try:
        # Stage all changes
        subprocess.run(["git", "add", "-A"], cwd=os.getcwd())

        # Commit the staged changes with the timestamp in the message
        subprocess.run(["git", "commit", "-m", f"{commit_message}"], cwd=os.getcwd())
        print(f"Changes committed with timestamp: {timestamp}")
    except Exception as e:
        print(f"An error occurred while committing: {str(e)}")


def main():
    try:
        git_commit_with_timestamp()
    except Exception as e:
        print(f"An error occurred while committing: {str(e)}")
    finally:
        from cleanup import main as cleanup_main

        cleanup_main()  # Call the cleanup function
