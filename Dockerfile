# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# - wget, gnupg, ca-certificates: for adding Google's apt repository
# - jq: for parsing JSON to find the correct ChromeDriver version
# - unzip: for extracting ChromeDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates \
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
# We need a specific version of Chrome that is compatible with a known ChromeDriver
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install ChromeDriver
# This command finds the major version of the installed Google Chrome,
# then queries the official Chrome for Testing JSON endpoints to find the correct
# ChromeDriver download URL for that major version on Linux 64-bit.
# It then downloads, unzips, and moves ChromeDriver to a directory in the PATH.
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed 's/.* \([0-9]*\)\..*/\1/') \
    && echo "Detected Chrome major version: $CHROME_MAJOR_VERSION" \
    && CHROMEDRIVER_URL=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json | jq -r ".milestones[\"$CHROME_MAJOR_VERSION\"].downloads.chromedriver[] | select(.platform==\"linux64\") | .url") \
    && echo "Using ChromeDriver URL: $CHROMEDRIVER_URL" \
    && wget -q "$CHROMEDRIVER_URL" -O chromedriver.zip \
    && unzip chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && rm -rf /usr/local/bin/chromedriver-linux64 \
    && rm chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY instagram_login.py .

# Set environment variables for the script
# These should be passed in at runtime, but we can set placeholders
ENV INSTAGRAM_USERNAME=""
ENV INSTAGRAM_PASSWORD=""

# Command to run the Python script
# The "-u" flag ensures that prints send straight to stdout without being buffered
CMD ["python", "-u", "instagram_login.py"]