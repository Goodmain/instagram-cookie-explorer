# Start from the official Selenium image which includes Chrome and the correct driver
FROM selenium/standalone-chrome:latest

# Switch to the root user to install Python
USER root

# Install Python and Pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory for our app
WORKDIR /app

# Copy our Python requirements and script into the container
COPY requirements.txt .
COPY instagram_login.py .

# Install the Python libraries
RUN pip3 install --no-cache-dir -r requirements.txt

# Change ownership of the app directory to the container's default user
RUN chown -R seluser:seluser /app

# Switch back to the non-root user for security
USER seluser

# Set the command to run our Python script when the container starts
CMD ["python3", "-u", "instagram_login.py"]