# Dockerfile

# Base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Set working directory
WORKDIR /app

# Copy files to working directory
COPY . /app
# Install required packages
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

# Set the CMD line to redirect output to a log file
CMD [ "/bin/bash", "-c", "source activate myenv && \
    jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root > debug.log 2>&1" ]
