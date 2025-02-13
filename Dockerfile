# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi8 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install flask weasyprint extract_msg

# Copy the application files into the container
COPY app.py /app/app.py
COPY templates /app/templates

# Create upload and output directories
RUN mkdir -p /app/uploads /app/outputs

# Expose the Flask app port
EXPOSE 5000

# Set the entrypoint to run the Flask app
CMD ["python", "app.py"]
