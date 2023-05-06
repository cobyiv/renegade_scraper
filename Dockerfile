# Use the official Python image as the base image
FROM python:3.10.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#env
COPY .env /app

# Install Cron
RUN apt-get update && apt-get install -y cron
RUN touch /var/log/cron.log

# Establish the Cron Job
RUN echo "55 23 * * 5 root cd /app && /usr/local/bin/python /app/run.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron

# # Install the required Python packages
RUN pip install -r requirements.txt

# Set the timezone to Seattle
RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
RUN echo "America/Los_Angeles" > /etc/timezone

# Start the Python app
CMD cron && tail -f /var/log/cron.log