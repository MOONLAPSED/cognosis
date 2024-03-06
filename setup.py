import setuptools
import pip
import logging
import sys
import subprocess
import os
import venv
try:  # Configure setup logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file_handler': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log')),
                'maxBytes': 10 * 1024 * 1024,  # 10MB
                'backupCount': 5,
                'formatter': 'standard'
            },
        },
        'formatters': {
            'standard': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'root': {
            'level': logging.INFO,
            'handlers': ['file_handler']
        },
    }
    logging.config.dictConfig(logging_config)
    logging.info("Setup-logging configuration initiated.")
except Exception as e:
    # Basic logging setup for setup.py in case of configuration error
    log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs', 'setup.log'))
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    logging.error(f"Error setting up logging configuration: {e}")
    raise SystemExit(1)  # Indicate installation failure (no logging)
finally:
    logging.info("Setup-logging initiated.")

def read_requirements():
    with open('requirements.txt') as req:
        requirements = req.read().splitlines()
    return requirements

def __starter():  # windows starter
    nt="copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE"
    subprocess.run(nt, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for req in read_requirements():
        try:
            pip.main(['install', req])
        except Exception as e:
            logging.error(f"Error installing requirement {req}: {e}")
            return False
    return True

def __path():
    project_root = os.path.abspath(os.path.dirname(__file__))
    os.environ['PROJECT_ROOT'] = project_root
    os.environ['VIRTUAL_ENV'] = os.path.abspath(os.path.join(project_root, 'venv'))
    os.environ['PATH'] = os.environ['VIRTUAL_ENV'] + os.pathsep + os.environ['PATH']
    return True

def __venv():  # requires __path() to be called first
    try:
        venv_path = os.environ['VIRTUAL_ENV']
        if os.path.exists(venv_path) is False or None:
            logging.info("Creating virtual environment...")
            venv.create(venv_path, with_pip=True)
        return venv_path
    except Exception as e:
        logging.error(f"Error creating virtual environment: {e}")
        return False
    
def __appget():  # 'runs' __path() and __starter()
    app = __starter()
    if app is False:
        return False
    else:
        pass
    try:
        __path()
    except Exception as e:
        logging.error(f"Error setting up $PATH: {e}")
        return False
    finally:
        logging.info("$PATH set up.")
    return True

def __main():
    try:
        logging.info("Starting setup...")
        if __venv() and __path() and __starter():
            logging.info("Setup complete or cognosis already installed.")
            return True
        else:
            logging.info("No cognosis hidden methods present in $PATH, adding...")
        launcher=__appget()
        if launcher is False or None:
            logging.info("Setup failed.")
            return False
        else:
            pass
        try:
            launcher=__appget()
            venv_path=__venv()
            if venv_path is False or None:
                logging.info("Setup failed.")
                return False
            else:
                pass
            subprocess.run(f'python -m venv {venv_path}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            logging.error(f"Error during setup: {e}")
            return False
        finally:
            logging.info("Setup complete.")
            # if all routines PASS or are True, then return True after doing anything written-here
        return True
    except Exception as e:
        logging.error(f"Error during setup: {e}")
        raise

    
if __name__ == "__main__":
    try:
        if __main() is True:
            logging.info("Setup complete.")
            sys.exit(0)
        else:  # else __main() is false
            logging.info("__main__ runtime achieved, but __main() is false.")
            pass
    except Exception as e:
        logging.error(f"Error during setup: {e}")
        sys.exit(1)
    finally:
        if os.environ.get('VIRTUAL_ENV') is not None:
            activate_script = os.path.join(os.environ.get('VIRTUAL_ENV'), 'Scripts', 'activate')
            subprocess.run(f'cmd /k "{activate_script}"', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            pass
        if os.environ.get('PROJECT_ROOT') is not str.lower(os.path.abspath(os.path.dirname(__file__))):
            os.environ['PROJECT_ROOT'] = os.path.abspath(os.path.dirname(__file__))
        else:
            pass
        if os.environ.get('PATH') is not os.environ['VIRTUAL_ENV'] + os.pathsep + os.environ['PATH']:
            os.environ['PATH'] = os.environ['VIRTUAL_ENV'] + os.pathsep + os.environ['PATH']
        else:
            pass

        # assemble all objects to pass to /src/app.py for creation of pydantic BaseModel
        