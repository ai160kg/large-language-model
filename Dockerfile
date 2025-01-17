FROM python:3.12-slim

# Set environment variables for proper color support and Gradio
ENV TERM=xterm-256color \
    COLORTERM=truecolor \
    FORCE_COLOR=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry --version

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN pip install --no-cache-dir \
    together==1.3.11 \
    colorama \
    python-dotenv \
    requests \
    chromadb \
    sentence-transformers \
    gradio \
    pandas

# Create data directory for persistent memory
RUN mkdir -p /app/data/memory && \
    chmod -R 777 /app/data

# Copy the application code and public assets
COPY src /app/src
COPY public /app/public

# Install the package in development mode
RUN poetry install --no-interaction --no-ansi

# Expose port for Gradio
EXPOSE 7860

# Set the default command to run the UI
CMD ["python", "-m", "src.llm_swarm.ui.app"] 