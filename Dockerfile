# Use an official Miniconda runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/requirements.txt

# Create a Conda environment and activate it
RUN conda create --name DamageDetection python=3.8
SHELL ["conda", "run", "-n", "DamageDetection", "/bin/bash", "-c"]

# Install the required packages using pip
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Specify the command to run on container start
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
