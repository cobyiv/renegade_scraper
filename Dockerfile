# Use the official Python image as the base image
FROM python:3.10.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#env
COPY .env /app

# # Install the required Python packages
RUN pip install -r requirements.txt

# Set the timezone to Seattle
RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
RUN echo "America/Los_Angeles" > /etc/timezone

# Start the Python app
CMD ["/bin/bash"]