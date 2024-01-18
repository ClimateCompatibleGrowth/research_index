# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install packages for the memgraph client
RUN sudo apt install python3-dev cmake make gcc g++ libssl-dev

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]