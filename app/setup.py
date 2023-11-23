import subprocess

class RateLimitExceededError(Exception):
    pass

def run_setup():
    result = subprocess.run(['./setup.sh'], capture_output=True, text=True)
    if 'Error: Setup job has been run too many times. Please wait and try again.' in result.stderr:
        raise RateLimitExceededError('Rate limit exceeded for setup job')
    return result.stdout
import retry

@retry
def run_setup():
    result = subprocess.run(['./setup.sh'], capture_output=True, text=True)
    if 'Error: Setup job has been run too many times. Please wait and try again.' in result.stderr:
        raise RateLimitExceededError('Rate limit exceeded for setup job')
    return result.stdout
import retry

@retry
def run_setup():
    result = subprocess.run(['./setup.sh'], capture_output=True, text=True)
    if 'Error: Setup job has been run too many times. Please wait and try again.' in result.stderr:
        raise RateLimitExceededError('Rate limit exceeded for setup job')
    return result.stdout
import retry

@retry
def run_setup():
    result = subprocess.run(['./setup.sh'], capture_output=True, text=True)
    if 'Error: Setup job has been run too many times. Please wait and try again.' in result.stderr:
        raise RateLimitExceededError('Rate limit exceeded for setup job')
    return result.stdout
from common import common_setup
from common import common_setup
from common import common_setup
