# Instagram Cookie Exporter

This project provides a simple, containerized solution for logging into Instagram and exporting your session cookies. It uses Selenium with Chrome and is designed to handle 2-Factor Authentication (2FA) by prompting for the code in your terminal.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Goodmain/instagram-cookie-exporter.git
    cd instagram-cookie-exporter
    ```

2.  **Create an environment file:**

    Create a file named `.env` in the root of the project and add your Instagram credentials. **Note:** The script uses `IG_USERNAME` and `IG_PASSWORD`.

    ```env
    IG_USERNAME="your_instagram_username"
    IG_PASSWORD="your_instagram_password"
    ```

    Replace `"your_instagram_username"` and `"your_instagram_password"` with your actual credentials.

## Usage

1.  **Build the Docker image:**

    Use Docker Compose to build the image. This command reads the `docker-compose.yml` file and builds the `insta-exporter` service.
    ```bash
    docker-compose build
    ```

2.  **Run the container:**

    Execute the following command to run the container. The script will start, and you will be prompted for your 2FA code in the terminal. The `--rm` flag ensures the container is removed after the script finishes.
    ```bash
    docker-compose run --rm insta-exporter
    ```

3.  **Enter your 2FA code:**

    The script will log you into Instagram and may pause for you to enter your 2FA code. Check your terminal and input the code when prompted.

## Output

Once the login is successful, the script will save your session cookies to a file named `instagram_cookies.txt` inside the `output/` directory. The cookies are saved in the **Netscape cookie file format**, which is compatible with tools like `yt-dlp` and other scripts.