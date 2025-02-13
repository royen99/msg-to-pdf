# 📧 EML/MSG to PDF Converter 🚀

A Flask-based web application to convert `.eml` and `.msg` email files to PDF, including attachments like `.docx`, `.pptx`, and `.xlsx`. Built with ❤️ using Python, Docker, and modern libraries.

---

## 🌟 Features

- **Email Conversion**:
  - Convert `.eml` and `.msg` files to PDF. ✅
  - Preserve email headers (From, To, Subject). 📄
  - Handle HTML and plain text email content. ✉️

- **Attachment Support**:
  - Include attachments in the final PDF. 📎
  - Convert attachments to PDF:
    - Word documents (`.docx`) → PDF. 📑
    - PowerPoint presentations (`.pptx`) → PDF. 📊
    - Excel spreadsheets (`.xlsx`) → PDF. 📈
  - Directly include PDF attachments. 📄

- **Modern Web Interface**:
  - Drag-and-drop file upload. 🖱️
  - Sleek and responsive design. 🎨
  - Dark mode support. 🌙

- **Dockerized**:
  - Easy to deploy using Docker. 🐳
  - No external dependencies required. 🚫

---

## 🛠️ Technologies Used

- **Python Libraries**:
  - `Flask`: Web framework. 🌐
  - `WeasyPrint`: HTML to PDF conversion. 🖨️
  - `extract_msg`: Extract content from `.msg` files. 📩
  - `pypandoc`: Convert `.docx` files to PDF. 📑
  - `python-pptx`: Extract content from `.pptx` files. 📊
  - `openpyxl`: Extract content from `.xlsx` files. 📈
  - `PyPDF2`: Merge PDFs. 🔗

- **System Dependencies**:
  - `Pandoc`: Document conversion. 🔄
  - `TeX Live`: PDF engine for `pandoc`. 📜

---

## 🚀 Getting Started

### Prerequisites

- Docker installed on your system. 🐳
  - [Install Docker](https://docs.docker.com/get-docker/)

### Steps to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/royen99/msg-to-pdf.git
   cd msg-to-pdf

2. **Build the Docker Image**:
    ```bash
    docker build -t eml-to-pdf-converter .

3. **Run the Docker Container**:
    ```bash
    docker run -p 5000:5000 eml-to-pdf-converter

4. **Access the Web Interface**:
Open your browser and navigate to: `http://localhost:5000`.

5. **Upload and Convert**:
    * Drag and drop your .eml or .msg file.
    * Download the converted PDF with attachments. 📥

## 📂 Project Structure
    eml-to-pdf-converter/
    ├── app.py                # Flask application
    ├── Dockerfile            # Docker configuration
    ├── README.md             # Project documentation
    ├── requirements.txt      # Python dependencies
    └── templates/
        └── index.html        # Web interface

## 🤝 Contributing
Contributions are welcome! 🎉 If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.
- Fork the repository. 🍴
- Create a new branch. 🌿
- Make your changes. ✏️
- Submit a pull request. 🚀

## 📜 License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
