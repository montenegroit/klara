# Set base image
FROM python:3.8.6-slim

# Set the working directory
WORKDIR /bot

# Copying the dependencies file
COPY req.txt .

# Installing dependencies
RUN pip install -r req.txt

# Copying files into working directory
COPY . /bot

