FROM ghcr.io/ai-dock/jupyter-pytorch:2.1.0-py3.9-cuda-12.1.0-cudnn8-devel-22.04

ADD cognosis /project/cognosis
COPY pyproject.toml /project/
COPY env.config .env
COPY requirements.txt .
# COPY start.sh /start.sh
COPY cognosis ./cognosis/
# COPY main ./cognosis/main
# COPY src ./cognosis/src
SHELL ["/bin/bash", "-c"]
WORKDIR /project
COPY requirements.txt /temp/
RUN apt-get update && \
    apt-get install -y python3-pip && \
    python -m pip install --upgrade pip==23.3.1
#1.  RUN  is a Dockerfile keyword that executes a command in a new layer of the Docker image. 
#2.  apt-get update  updates the list of available packages and their versions from the Debian/Ubuntu package repositories. 
#3.  &&  is a shell operator that allows you to execute multiple commands on the same line. 
#4.  apt-get install -y python3-pip  installs the  python3-pip  package, which provides the  pip3  command-line tool for installing Python packages. 
#5.  &&  is used again to execute the next command on the same line. 
#6.  pip3 install --no-cache-dir -r requirements.txt  uses  pip3  to install the Python packages listed in the  requirements.txt  file. The  --no-cache-dir  option tells  pip3  not to cache downloaded package files, which can save disk space. 

# Set environment variables to optimize Python runtime in Docker
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
#1. Step 1 creates a new user with a specific UID. This is useful for running the application in a container with non-root privileges, which is considered a best practice for security reasons. 
#2. Step 2 changes the ownership of the  /app  directory (and all its contents) to the new user created in Step 1. This is necessary because the new user needs permission to access the application code and any other files in the  /app  directory. 
#3. Step 3 updates the permissions of the  /app  directory (and all its contents) to allow the new user to read, write, and execute files, and to allow everyone else to read and execute files. This is necessary to ensure that the new user has the appropriate permissions to run the application. 
#4. Step 4 sets the working directory to  /app . This is useful for ensuring that any subsequent commands in the Dockerfile are executed in the context of the  /app  directory. 
#5. Step 5 sets the default user for subsequent commands in the Dockerfile to the new user created in Step 1. This is necessary to ensure that any subsequent commands are executed with the appropriate user permissions. 
# Set environment variable for OpenAI API key

# RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/' >> ~/.bashrc
# Define the command to run the application

# CMD ["faststream", "run", "--workers", "1", "cognosis.application:app"]
CMD ["python", "main.py"]

# Build the Docker image from your Dockerfile (assuming your Dockerfile is in the current directory):
# docker build -t my_image:tag .
# This will build a Docker image with the tag "my_image:tag" using the current directory as the build context (denoted by the dot at the end).
# docker run --gpus all -it my_image:tag
# The docker run command is used to configure the runtime behavior of the container, while the Dockerfile is used to define the image configuration and setup.

# Healthcheck to verify if the service is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1
USER nonroot
