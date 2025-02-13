import os
import sys
import re
import uuid
import base64
from io import BytesIO, StringIO
from flask import Flask, render_template, request, send_file, redirect, url_for, after_this_request
from email import policy, message_from_file
from extract_msg import Message  # For .msg files
from weasyprint import HTML, CSS

app = Flask(__name__)

def sanitize_html(html_content):
    """Sanitize HTML content to ensure it fits within the PDF page."""
    css = """
    <style>
        body { 
            font-family: Arial, sans-serif; 
            font-size: 12px; 
            margin: 0; 
            padding: 10px; 
            width: 100%; 
            overflow: hidden; 
        }
        pre, p { 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            overflow-wrap: break-word; 
            max-width: 100%; 
        }
        img { 
            max-width: 100% !important; 
            height: auto !important; 
            display: block; 
            margin: 0 auto; 
        }
        table { 
            width: 100% !important; 
            max-width: 100% !important; 
            border-collapse: collapse; 
        }
        td, th { 
            border: 1px solid #ddd; 
            padding: 8px; 
            word-wrap: break-word; 
            max-width: 100%; 
        }
        .email-header { 
            margin-bottom: 20px; 
        }
        .email-header p { 
            margin: 5px 0; 
        }
        * { 
            box-sizing: border-box; 
            max-width: 100% !important; 
        }
    </style>
    """
    html_content = re.sub(r"<head>", f"<head>{css}", html_content, flags=re.IGNORECASE)
    return html_content

def msg_to_pdf(msg_file):
    """Convert .msg file to PDF."""
    msg = Message(msg_file)
    
    # Extract email headers
    headers = f"""
    <div class="email-header">
        <p><strong>From:</strong> {msg.sender}</p>
        <p><strong>To:</strong> {msg.to}</p>
        <p><strong>Subject:</strong> {msg.subject}</p>
    </div>
    """
    
    # Extract HTML content if available
    html_content = None
    if msg.htmlBody:
        html_content = msg.htmlBody
    else:
        # Fall back to plain text if no HTML content is found
        html_content = f"""
        <html>
            <head>
                <title>Email</title>
            </head>
            <body>
                {headers}
                <pre>{msg.body}</pre>
            </body>
        </html>
        """
    
    # Ensure html_content is a string (decode if it's bytes)
    if isinstance(html_content, bytes):
        html_content = html_content.decode("utf-8", errors="replace")
    
    # Inject headers into the HTML content
    if "<body>" in html_content:
        html_content = html_content.replace("<body>", f"<body>{headers}")
    
    # Handle embedded images
    for attachment in msg.attachments:
        if attachment.type == "image":
            # Encode the image as base64
            image_data = base64.b64encode(attachment.data).decode("utf-8")
            # Replace the cid reference in the HTML with the base64-encoded data
            cid = attachment.cid.strip("<>")
            if cid:
                html_content = html_content.replace(
                    f'cid:{cid}',
                    f'data:{attachment.mimetype};base64,{image_data}'
                )
    
    # Sanitize and generate PDF
    html_content = sanitize_html(html_content)
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(
        pdf_bytes,
        stylesheets=[CSS(string="@page { size: A3 landscape; margin: 1cm; }")]
    )
    pdf_bytes.seek(0)
    return pdf_bytes

def eml_to_pdf(eml_file):
    """Convert .eml file to PDF."""
    # Decode the bytes into a string
    eml_content = eml_file.read().decode("utf-8", errors="replace")
    # Use StringIO to simulate a file-like object for message_from_file
    eml_string_io = StringIO(eml_content)
    msg = message_from_file(eml_string_io, policy=policy.default)
    
    # Extract email headers
    headers = f"""
    <div class="email-header">
        <p><strong>From:</strong> {msg['From']}</p>
        <p><strong>To:</strong> {msg['To']}</p>
        <p><strong>Subject:</strong> {msg['Subject']}</p>
    </div>
    """
    
    # Extract HTML content from the email
    html_content = None
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                html_content = part.get_payload(decode=True).decode("utf-8", errors="replace")
                break
    else:
        if msg.get_content_type() == "text/html":
            html_content = msg.get_payload(decode=True).decode("utf-8", errors="replace")
    
    # If no HTML content is found, fall back to plain text
    if not html_content:
        plain_text = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        html_content = f"""
        <html>
            <head>
                <title>Email</title>
            </head>
            <body>
                {headers}
                <pre>{plain_text}</pre>
            </body>
        </html>
        """
    
    # Ensure html_content is a string (decode if it's bytes)
    if isinstance(html_content, bytes):
        html_content = html_content.decode("utf-8", errors="replace")
    
    # Inject headers into the HTML content
    if "<body>" in html_content:
        html_content = html_content.replace("<body>", f"<body>{headers}")
    
    # Handle inline images
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == "image":
                # Extract the image data
                image_data = part.get_payload(decode=True)
                # Encode the image as base64
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                # Replace the cid reference in the HTML with the base64-encoded data
                cid = part.get("Content-ID", "").strip("<>")
                if cid:
                    html_content = html_content.replace(
                        f'cid:{cid}',
                        f'data:{part.get_content_type()};base64,{image_base64}'
                    )
    
    # Sanitize and generate PDF
    html_content = sanitize_html(html_content)
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(
        pdf_bytes,
        stylesheets=[CSS(string="@page { size: A3 landscape; margin: 1cm; }")]
    )
    pdf_bytes.seek(0)
    return pdf_bytes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if file and (file.filename.endswith(".eml") or file.filename.endswith(".msg")):
            # Process the file in memory
            file_stream = BytesIO(file.read())
            if file.filename.endswith(".eml"):
                pdf_bytes = eml_to_pdf(file_stream)
            elif file.filename.endswith(".msg"):
                pdf_bytes = msg_to_pdf(file_stream)
            
            # Return the PDF as a downloadable file
            return send_file(
                pdf_bytes,
                as_attachment=True,
                download_name=f"{uuid.uuid4()}.pdf",
                mimetype="application/pdf"
            )
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
