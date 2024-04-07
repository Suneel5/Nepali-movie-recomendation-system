# Use the official Python image as the base image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /myapp

# Copy the application files into the working directory
COPY . /myapp

# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
CMD ["flask", "run", "--host=0.0.0.0"]