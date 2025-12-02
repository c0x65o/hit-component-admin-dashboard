FROM python:3.11-slim

WORKDIR /app

# Install uv for fast package management
RUN pip install --no-cache-dir uv

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies
RUN uv pip install --system .

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8200

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8200"]

