FROM ghcr.io/ai-dock/jupyter-pytorch:2.1.0-py3.9-cuda-12.1.0-cudnn8-devel-22.04

ADD cognosis /project/cognosis
COPY .env.example .env
COPY requirements.txt .
COPY cognosis ./cognosis/
SHELL ["/bin/bash", "-c"]
WORKDIR /project
COPY requirements.txt /temp/
RUN apt-get update && \
    apt-get install -y python3-pip && \
    python -m pip install --upgrade pip==23.3.1 && \
    pip install --no-cache-dir -r /temp/requirements.txt && \
    pip install jupyter_contrib_nbextensions && \
    conda install -y -c pytorch pytorch torchvision cudatoolkit=12.1.0 cudnn=8.1.0 && \
    conda clean -afy

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"
#1.  ENV  is a Dockerfile keyword that sets environment variables in the Docker image. 
#2.  PYTHONDONTWRITEBYTECODE=1  sets the  PYTHONDONTWRITEBYTECODE  environment variable to 1, which tells Python not to write bytecode files (.pyc) to disk. This can improve performance and reduce disk usage in some cases, but may affect debugging and import behavior.  
#3.  PYTHONUNBUFFERED=1  sets the  PYTHONUNBUFFERED  environment variable to 1, which tells Python to run in unbuffered mode. This can improve the responsiveness of Python applications running in Docker, by reducing the amount of data that is buffered in memory before being output. 
#4.  PATH="/home/appuser/.local/bin:${PATH}"  adds  /home/appuser/.local/bin  to the beginning of the system  PATH  variable, which allows executables installed by  pip  to be found without specifying the full path.
# Create a non-root user with an explicit UID and add permission to access the /app folder
RUN adduser --uid 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser /app \
    && chmod -R 755 /app
# Switch user to non-root user
USER appuser
# Define the command to run the application
CMD ["faststream", "run", "--workers", "1", "cognosis.application:app"]
# CMD ["python", "test_application.py"]

# docker build -t my_image:tag .
# This will build a Docker image with the tag "my_image:tag" using the current directory as the build context (denoted by the dot at the end).
# docker run --gpus all -it my_image:tag
# The docker run command is used to configure the runtime behavior of the container, while the Dockerfile is used to define the image configuration and setup.

# Healthcheck to verify if the service is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1
USER nonroot
