FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY entrypoint.py /entrypoint.py

# Default command
ENTRYPOINT ["python", "/entrypoint.py"]
