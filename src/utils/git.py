import datetime
# TODO spin-up custom 'git' module

def git_commit_with_timestamp():
    try:
        repo = git.Repo('.')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        repo.git.add(A=True)
        repo.git.commit(m=f"Auto-commit at {timestamp}")
        print(f"Changes committed with timestamp: {timestamp}")
    except git.exc.InvalidGitRepositoryError:
        print("Not a valid git repository. Initializing...")
        repo = git.Repo.init('.')
        repo.git.add(A=True)
        repo.git.commit(m="Initial commit")
        print("Git repository initialized and initial commit made.")
    except Exception as e:
        print(f"An error occurred while committing: {str(e)}")

def main():
    """invoked at-least once per runtime to perform git commit with timestamp
    this naturally includes CICD, pre-commit hooks, etc."""
    try:
        git_commit_with_timestamp()
    except Exception as e:
        print(f"An error occurred while committing: {str(e)}")
    finally:
        from cleanup import main as cleanup_main
        cleanup_main()
