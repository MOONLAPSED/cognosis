import subprocess


class RateLimitExceededError(Exception):
    pass

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
