# Use official Python image
FROM python:3.10-slim

# Install system dependencies, including Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "aadhaar_ocr_service:app"]
