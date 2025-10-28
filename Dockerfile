# ---- sanity-check Dockerfile ----
    FROM python:3.11-slim

    # Set working directory
    WORKDIR /app
    
    # Minimal dependencies
    RUN pip install --no-cache-dir pandas numpy google-cloud-storage
    
    # Copy everything (optional)
    COPY . .
    
    # Simple sanity script
    RUN echo "✅ Docker image built successfully" > /app/healthcheck.txt
    
    # Command to verify environment
    CMD ["python3", "-c", "\
    import os, sys, pandas as pd; \
    print('✅ Sanity check OK'); \
    print('Python version:', sys.version); \
    print('Files:', os.listdir('/app')); \
    print('pandas version:', pd.__version__); \
    "]
    