# Instagram Cookie Exporter

This project provides a Dockerized Python script to log into Instagram using Selenium, handle 2-Factor Authentication (2FA), and export the session cookies to a JSON file. These cookies can then be used for other automation tasks that require an authenticated Instagram session.

## Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed on your system.

## How to Use

### 1. Build the Docker Image

First, build the Docker image using the provided `Dockerfile`. Open a terminal in the project directory and run:

```bash
docker build -t instagram-cookie-exporter .
```

### 2. Run the Docker Container

To run the script, you need to provide your Instagram credentials as environment variables. You also need to mount a local directory to the container to be able to access the exported cookies file.

Execute the following command, replacing `<your_username>`, `<your_password>`, and `<path_to_local_directory>` with your actual credentials and a local path.

-   **For Linux/macOS:**
    ```bash
    docker run -it \
      -e INSTAGRAM_USERNAME="<your_username>" \
      -e INSTAGRAM_PASSWORD="<your_password>" \
      -v "$(pwd)/output:/app/output" \
      instagram-cookie-exporter
    ```
-   **For Windows (Command Prompt):**
    ```bash
    docker run -it ^
      -e INSTAGRAM_USERNAME="<your_username>" ^
      -e INSTAGRAM_PASSWORD="<your_password>" ^
      -v "%cd%\\output:/app/output" ^
      instagram-cookie-exporter
    ```
-   **For Windows (PowerShell):**
    ```bash
    docker run -it `
      -e INSTAGRAM_USERNAME="<your_username>" `
      -e INSTAGRAM_PASSWORD="<your_password>" `
      -v "${PWD}\\output:/app/output" `
      instagram-cookie-exporter
    ```

**Note:** The `-it` flag is important as it runs the container in interactive mode, which is necessary for you to enter the 2FA code when prompted.

### 3. Enter 2FA Code

After you run the container, the script will navigate to the Instagram login page and enter your credentials. If your account has 2FA enabled, the script will pause and prompt you to enter the 6-digit verification code sent to your device:

```
Enter the 2FA code:
```

Type the code into the terminal and press `Enter`.

### 4. Retrieve the Cookies

If the login is successful, the script will create a file named `instagram_cookies.json` inside the container. Because we mounted the `output` directory, this file will appear in the `output` folder on your local machine.

The contents of `instagram_cookies.json` will look something like this:

```json
[
    {
        "domain": ".instagram.com",
        "expirationDate": 1730123456,
        "hostOnly": false,
        "httpOnly": true,
        "name": "sessionid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": true,
        "session": false,
        "storeId": "0",
        "value": "..."
    },
    ...
]
```

You can now use this JSON file in other scripts or tools that need to make authenticated requests to Instagram.

## How it Works

-   **`Dockerfile`**: Sets up a container with Python, Google Chrome, and the correct version of ChromeDriver. It also installs the necessary Python libraries from `requirements.txt`.
-   **`instagram_login.py`**: A Python script that uses Selenium to automate the browser. It navigates to Instagram, fills in the login form, waits for a 2FA prompt, and saves the cookies upon successful login.
-   **`requirements.txt`**: Specifies the Python dependencies (`selenium`).