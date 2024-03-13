# cognosis - cognitive coherence coroutines - NLP + LLM + KB
## MIT license - MOONLAPSED@gmail.com + MOONLAPSED@github

```pseudocode
kb = "knowledge base":
    an abstract data class for logging disparate cognition into a lifelong artifact for learning and development.
```

\#include "/docs/README.md"


\#<|currently@'/README.md'|>:


### ::__Instructions__::
[youtube video link](https://www.youtube.com/watch?v=-rGRMM7jZhA)

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
        - if it fails try again and if nothing you need to exit and restart the whole container
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
        - pip install -e -r requirements.txt
        - python3 -m pip install --user pipx
        - to test setup.py:
            Create a virtual environment: python -m venv test_env
            Activate it: test_env\Scripts\activate
            Install package locally: python setup.py install
            pip install -r requirements.txt
        - pip install open-interpreter
        - pip install litellm
        - pip install instructor
        - pip install errbot
        - errbot --init
        - errbot
            + Command names also support unix-style globs and can optionally be restricted to a specific plugin by prefixing the command with the name of a plugin, separated by a colon. 
            + For example, Health:status will match the !status command of the Health plugin and Health:* will match all commands defined by the Health plugin.
            + The first command match found will be used so if you have overlapping patterns you must used an OrderedDict instead of a regular dict.
            + The !help command will list all commands and their descriptions.
    ```



```WSL_INSTALL:
wsl # this is the ubuntu-22.04 vers.
python3 -m pip install --user pipx  # source it in .bashrc to add path
python3 -m pipx ensurepath
source .bashrc

```










### Advanced - potential runtime configuration or **kwargs:

    ```
    [[loopback|local host]]::Ollama binds 127.0.0.1 port 11434 by default. Change the bind address with the OLLAMA_HOST environment variable.

    ```


### Extras - for empty cycles or downtime::[[rlhf]][[rlhf|kb]][[rlhf|kb->]][[rlhf|kb<-]]
> "->" is a "forward" or "outgoing" link, "<-" is a "backward" or "incoming" link.
    - outgoing links do not mutate the state other elements of kb (generally it will mean the creation of a new kb element but not necessarily (if one exists, if permissons aren't sufficient, etc))
    - incoming links are 'to-be-back-ported' to the kb -- involves the maintenence of a 'backport' queue due to asynchronous nature of the kb

> markdown is m

> numerous previous branches of this git repo, and all of my public repositories

> I keep a record of all work-files related to my projects including extensive chatbot-history (chat logs of code gneration and development)::[[2023dir]] (not public as of now)

