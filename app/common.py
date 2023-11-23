def common_setup():
    """
    Run the setup job and handle rate limit exceeded errors.

    Returns:
        str: The stdout output of the setup job.

    Raises:
        RateLimitExceededError: If the rate limit for the setup job is exceeded.
    """
    result = subprocess.run(['./setup.sh'], capture_output=True, text=True)
    if 'Error: Setup job has been run too many times. Please wait and try again.' in result.stderr:
        raise RateLimitExceededError('Rate limit exceeded for setup job')
    return result.stdout

class RateLimitExceededError(Exception):
    pass

def validate_input(command):
    Validate the input command to ensure it is safe for execution.

    Args:
        command (list): The command to be executed.

    Raises:
        ValueError: If the command contains untrusted input.
    """
    # Add validation logic here, such as checking for untrusted characters or patterns in the command
    if any(re.search(pattern, arg) for pattern in ['<untrusted_pattern_1>', '<untrusted_pattern_2>']):
        raise ValueError('Untrusted input detected in command')
import re


def validate_input(command):
    """
    Validate the input command to ensure it is safe for execution.

    Args:
    Raises:
        ValueError: If the command contains untrusted input.
    """
    # Add validation logic here, such as checking for untrusted characters or patterns in the command
    if any(re.search(pattern, arg) for pattern in ['<untrusted_pattern_1>', '<untrusted_pattern_2>']):
        raise ValueError('Untrusted input detected in command')
import re


def validate_input(command):
    """
    Validate the input command to ensure it is safe for execution.

    Args:
