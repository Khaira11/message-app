# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create directory for message file and set permissions
RUN mkdir -p /data && chmod 755 /data

# Create a non-root user to run the app
RUN useradd -m -u 1000 webuser && chown -R webuser:webuser /app /data
USER webuser

# Expose port
EXPOSE 5000

# Environment variables
ENV MESSAGE_FILE_PATH=/data/message.txt
ENV PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
