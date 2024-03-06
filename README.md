# cognosis - cognitive coherence coroutines - NLP + LLM + KB
## MIT license - MOONLAPSED@gmail.com + MOONLAPSED@github

```pseudocode
kb = "knowledge base":
    an abstract data class for logging disparate cognition into a lifelong artifact for learning and development.
```

\#include "/docs/README.md"


\#<|currently@'/README.md'|>:

### ::__Instructions__::
    ```
    - `cd {{app_dir}}`
    - conda activate {{env_name}}
    - conda env create -f environment.yml
    - `python -m {{app_name}}`
    ```

    ```
    * clone to your local machine, set local $PATH manually in cfg.wsb and scoop.ps1.
    * run cfg.wsb to open container
    * inside container; try `boxy.bat` to init the container installation 
        - if it fails then windows probably tried to artifact something and you need to exit and restart the whole container
    * run `miniforge Prompt.lnk` to open a conda environment 
        - 'windows-key' + type 'terminal', select windows terminal
        - cd Desktop
        - .\"Miniforge Prompt.lnk"
        - conda create -n 3ten python=3.10
        - conda init
        - exit
        - cmd.exe (from inside windows terminal)
        - cd Desktop
        - .\"Miniforge Prompt.lnk"
        - conda activate 3ten
        - python.exe -m pip install --upgrade pip
        - pip install -r requirements.txt OR:
        - to test setup.py:
            Create a virtual environment: python -m venv test_env
            Activate it: test_env\Scripts\activate
            Install package locally: python setup.py install
            pip install -r requirements.txt
        - pip install open-interpreter
        - pip install litellm
        - pip install instructor
        - pip install lit-llm
        - pip install errbot
        - errbot --init
        - errbot
            + Command names also support unix-style globs and can optionally be restricted to a specific plugin by prefixing the command with the name of a plugin, separated by a colon. 
            + For example, Health:status will match the !status command of the Health plugin and Health:* will match all commands defined by the Health plugin.
            + The first command match found will be used so if you have overlapping patterns you must used an OrderedDict instead of a regular dict.
            + The !help command will list all commands and their descriptions.
    ```