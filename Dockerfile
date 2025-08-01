# Use Python 3.10
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy code to container
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
