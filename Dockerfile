# 1. Use an official Python base image
FROM python:3.10-slim

# 2. Install LibreOffice and required fonts
# We need libreoffice to convert .docx to .pdf
# We also clean up the cache to keep the image small
RUN apt-get update && apt-get install -y \
    libreoffice \
    fonts-liberation \
    libxml2 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy your local files into the container
# This includes main.py, requirements.txt, and your template
COPY . .

# 5. Install the Python libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose the port Koyeb will use
EXPOSE 8080

# 7. Start the application using Gunicorn (production-ready)
# main:app means: in main.py, find the Flask object named 'app'
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app", "--timeout", "90"]
