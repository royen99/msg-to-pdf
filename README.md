# Email to PDF Converter

This is a simple Flask-based web application that converts email files (`.eml` and `.msg`) into PDFs. The app runs inside a Docker container, and it allows users to upload their email files and get a downloadable PDF version.

## Features

- Converts `.eml` and `.msg` email files to PDFs.
- Inline images and email headers are properly included in the PDF.
- Runs in a Docker container, making it easy to deploy anywhere.
- Temporary file storage: uploaded files and generated PDFs are automatically deleted after download.

## Requirements

To run this project locally, you'll need:

- Python 3.x
- Docker (for containerized setup)

## How to Run Locally

1. Clone this repository:

    ```bash
    git clone https://github.com/royen99/msg-to-pdf.git
    cd msg-to-pdf
    ```

2. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

    This will start the application on `http://localhost:5000`.

## How to Use

1. Open the app in your browser at `http://localhost:5000`.
2. Upload a `.eml` or `.msg` file using the upload form.
3. The app will process the file and convert it to a PDF.
4. Download the PDF once it's ready.

## Docker Setup

The app is designed to be easily deployable using Docker. The `Dockerfile` and `docker-compose.yml` files are included in the repo for easy setup.

To start the app in Docker:

1. Build the Docker image:

    ```bash
    docker-compose build
    ```

2. Run the container:

    ```bash
    docker-compose up
    ```

The app will be accessible at `http://localhost:5000`.

## Files Handled

- `.eml` files: Standard email format used by many email clients (like Outlook).
- `.msg` files: Microsoft Outlook message format.
  
Both file types are processed and converted into well-formatted PDFs, including the email's content, headers, and any inline images.

## Technologies Used

- **Flask**: A lightweight Python web framework used for serving the app.
- **WeasyPrint**: A library for converting HTML to PDF, used for rendering email content.
- **extract-msg**: A Python library for reading `.msg` files (Microsoft Outlook emails).
- **Docker**: Used to containerize the app for easy deployment.

## License

This project is open-source and available under the Apache 2.0 License.

## Acknowledgments

- **Flask** for making web development simple.
- **WeasyPrint** for reliable HTML to PDF conversion.
- **extract-msg** for reading `.msg` files.
