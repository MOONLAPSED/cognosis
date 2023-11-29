#! /bin/bash

micromamba create -f environment.yml
micromamba activate jupyterjax
docker pull joshxt/local-llm:cuda 
docker run -d --name local-llm -p 8091:8091 --gpus all joshxt/local-llm:cuda -e THREADS="10" -e GPU_LAYERS="0" -e MAIN_GPU="0" -e LOCAL_LLM_API_KEY=""
