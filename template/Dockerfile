# Use the Python version 3.8 base image
FROM python:3.8

# Indicate that Flask is listening on port 5000
EXPOSE 5000

# Set an environment variable
# This tells Flask to allow requests from outside the container
ENV FLASK_RUN_HOST="0.0.0.0"

# Run commands in the container from the /srv/template directory
WORKDIR /srv/template

# Copy all files in this directory on your machine to the
# srv/template directory in the container
COPY . .

# Mount a volume to persist database across builds
VOLUME /srv/template/db

# Install pipenv
RUN ["pip", "install", "pipenv"]

# Install dependencies with pipenv
RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]

# Run Flask when the container is run
CMD ["flask", "run"]
