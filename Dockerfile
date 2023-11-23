# Dockerfile

# Base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3=3.8.10-0ubuntu1~20.04 \
    python3-pip=20.0.2-5ubuntu1.6

# Set working directory
WORKDIR /app

# Copy files to working directory
COPY . /app
# Install required packages
RUN pip3 install --no-cache-dir -r requirements.txt==1.2.3
RUN pip3 install -r requirements.txt==1.2.3

# Set the CMD line to redirect output to a log file
CMD [ "/bin/bash", "-c", "source activate myenv && \
    jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root > debug.log 2>&1" ]
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1
USER nonroot
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl --fail http://localhost:8888/ || exit 1
USER nonroot
