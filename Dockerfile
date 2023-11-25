FROM ghcr.io/ai-dock/jupyter-pytorch:2.1.0-py3.9-cuda-12.1.0-cudnn8-devel-22.04

# Copying necessary files and setting up the environment
COPY .env.dev .
COPY requirements.txt .
COPY start.sh /start.sh
COPY app ./cognosis/app
COPY main ./cognosis/main
COPY src ./cognosis/src

RUN apt-get update && \
    apt-get install -y build-essential git curl wget && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install jupyter_contrib_nbextensions && \
        #1. Step 1 creates a new user with a specific UID. This is useful for running the application in a container with non-root privileges, which is considered a best practice for security reasons.
        #2. Step 2 changes the ownership of the  /app  directory (and all its contents) to the new user created in Step 1. This is necessary because the new user needs permission to access the application code and any other files in the  /app  directory.
        #3. Step 3 updates the permissions of the  /app  directory (and all its contents) to allow the new user to read, write, and execute files, and to allow everyone else to read and execute files. This is necessary to ensure that the new user has the appropriate permissions to run the application.
        #4. Step 4 sets the working directory to  /app . This is useful for ensuring that any subsequent commands in the Dockerfile are executed in the context of the  /app  directory.
        #5. Step 5 sets the default user for subsequent commands in the Dockerfile to the new user created in Step 1. This is necessary to ensure that any subsequent commands are executed with the appropriate user permissions.
        # Creating a non-root user and setting permissions
    
        ENV PATH="/opt/conda/bin:${PATH}"
        ENV PYTHONDONTWRITEBYTECODE=1 \
            PYTHONUNBUFFERED=1 \
            PATH="/home/appuser/.local/bin:${PATH}"
    
        WORKDIR /app
        USER appuser
    
        # Set the default command to start the application
        CMD ["/bin/bash", "/rollout.sh"]
    
        # Healthcheck to verify if the service is up
        HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1
    
        USER nonroot
    adduser --uid 5678 --disabled-password --gecos "" appuser  && \
    chown -R appuser /app && \
    chmod -R 755 /app && \
    chmod +x /start.sh
#1. Step 1 creates a new user with a specific UID. This is useful for running the application in a container with non-root privileges, which is considered a best practice for security reasons.
#2. Step 2 changes the ownership of the  /app  directory (and all its contents) to the new user created in Step 1. This is necessary because the new user needs permission to access the application code and any other files in the  /app  directory.
#3. Step 3 updates the permissions of the  /app  directory (and all its contents) to allow the new user to read, write, and execute files, and to allow everyone else to read and execute files. This is necessary to ensure that the new user has the appropriate permissions to run the application.
#4. Step 4 sets the working directory to  /app . This is useful for ensuring that any subsequent commands in the Dockerfile are executed in the context of the  /app  directory.
#5. Step 5 sets the default user for subsequent commands in the Dockerfile to the new user created in Step 1. This is necessary to ensure that any subsequent commands are executed with the appropriate user permissions.
# Creating a non-root user and setting permissions

ENV PATH="/opt/conda/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /app
USER appuser

# Set the default command to start the application
CMD ["/bin/bash", "/rollout.sh"]

# Healthcheck to verify if the service is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1

USER nonroot
    adduser --uid 5678 --disabled-password --gecos "" appuser  && \
    chown -R appuser /app && \
    chmod -R 755 /app && \
    chmod +x /start.sh
#1. Step 1 creates a new user with a specific UID. This is useful for running the application in a container with non-root privileges, which is considered a best practice for security reasons.
#2. Step 2 changes the ownership of the  /app  directory (and all its contents) to the new user created in Step 1. This is necessary because the new user needs permission to access the application code and any other files in the  /app  directory.
#3. Step 3 updates the permissions of the  /app  directory (and all its contents) to allow the new user to read, write, and execute files, and to allow everyone else to read and execute files. This is necessary to ensure that the new user has the appropriate permissions to run the application.
#4. Step 4 sets the working directory to  /app . This is useful for ensuring that any subsequent commands in the Dockerfile are executed in the context of the  /app  directory.
#5. Step 5 sets the default user for subsequent commands in the Dockerfile to the new user created in Step 1. This is necessary to ensure that any subsequent commands are executed with the appropriate user permissions.
# Creating a non-root user and setting permissions
