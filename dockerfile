FROM ghcr.io/ai-dock/jupyter-pytorch:2.1.0-py3.9-cuda-12.1.0-cudnn8-devel-22.04
# Set the working directory
WORKDIR /app
COPY .env.dev .
COPY app ./cognosis/app
COPY main ./cognosis/main
COPY src ./cognosis/src
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential git curl wget && \

    # Install Miniconda
    RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to the PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Expose the environment variables from the .env file
ENV GITHUB_USERNAME=my_github_user
ENV GITHUB_PASSWORD=my_secret_password

# Create a new conda environment
RUN conda create -n myenv python=<your-python-version> && \
    echo "conda activate myenv" >> ~/.bashrc

# Install required packages in the conda environment
RUN /bin/bash -c "source activate myenv && \
    conda install -y requirements.txt && \
    conda clean -afy"

# Set the default command to activate the environment and start Jupyter with Xonsh
CMD [ "/bin/bash", "-c", "source activate myenv && \
    xonsh -c 'jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root'" ]
# CMD ["python", "server.py", "--auto-devices", "--no-stream", "--load-in-8bit", "--listen"]
# docker run --rm -v "$(pwd)/.env:/root/.env" cognosis
