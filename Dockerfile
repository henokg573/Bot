# Use an official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /Bot

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install pip and dependencies
RUN apt-get update && apt-get install -y python3-pip build-essential libssl-dev

# Install the Python dependencies
RUN pip3 install -U -r requirements.txt

# Run the register.py script
CMD ["python3", "register.py"]

