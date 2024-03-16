# cognosis - cognitive coherence coroutines - NLP + LLM + KB
## MIT license - MOONLAPSED@gmail.com + MOONLAPSED@github


\!#include: @`/docs/README.md`, @`src/app/README.md`, @`src/api/README.md`

\!#currently: @`/README.md`

```pseudocode
kb = "knowledge base":
    an abstract data class for logging disparate cognition into a lifelong artifact for learning and development.
```


### ::video instructions::
[youtube video link](https://www.youtube.com/watch?v=-rGRMM7jZhA)

## setup

+ micromamba - via environment.yaml (any hypervisor/os):
    ```
    - `cd {{app_dir}}`
    - conda activate {{env_name}}
    - conda env create -f environment.yml
    - `python -m {{app_name}}`
    ```
+ pipx, pdm - via pyproject.toml (wsl preferred):
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
        - python3 -m pip install --upgrade pip
        - python3 -m pip install --user pipx
        - pip install -e -r requirements.txt
        - Create a virtual environment: python -m venv test_env
        - Activate it: test_env\Scripts\activate
    ```



    ### WSL Python_App install:
    ```
    wsl # this is the ubuntu-22.04 vers.
    python3 -m pip install --user pipx  # source it in .bashrc to add path
    python3 -m pipx ensurepath
    source .bashrc

    ```

    see: @`docs/wsl_install.md` for a quick and dirty 0-69 wsl guide.




    ### Advanced - potential runtime configuration or **kwargs:

    ```
    [[loopback|local host]]::Ollama binds 127.0.0.1 port 11434 by default. Change the bind address with the OLLAMA_HOST environment variable.

    ```

