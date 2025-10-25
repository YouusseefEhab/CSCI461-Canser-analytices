# Dockerfile
FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app/pipeline/

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into container
COPY . /app/pipeline/

# Install all Python packages (including openpyxl!)
RUN python -m pip install --upgrade pip && \
    pip install pandas numpy matplotlib seaborn scikit-learn scipy requests openpyxl

# Create results directory
RUN mkdir -p /app/pipeline/results

# Default working directory
WORKDIR /app/pipeline/

# Default command
CMD ["/bin/bash"]
