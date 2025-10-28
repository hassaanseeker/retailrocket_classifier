# Base image with Python
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# System deps (optional, usually enough as-is)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirement installation first (layer cache friendly)
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py /app/app.py
COPY model.py /app/model.py

# If you already have a trained model.pkl, copy it now:
# COPY model.pkl /app/model.pkl

# Healthcheck file (debug info)
RUN echo "container ready" > /app/healthcheck.txt

# Expose port 8080 because Vertex AI expects container on 8080 by default
EXPOSE 8080

# Start FastAPI with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
