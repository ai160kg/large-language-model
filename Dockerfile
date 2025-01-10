FROM python:3.12-slim

WORKDIR /app

# Copy the application files
COPY src/ /app/src/
COPY public/ /app/public/
COPY README.md /app/

# Install any needed packages
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    requests \
    together

# Set the default command to run the application
CMD ["python", "src/agents.py"] 