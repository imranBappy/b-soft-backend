FROM python:3.9-slim

# Set environment variables to prevent Python from buffering stdout and to prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Clean up any existing sources and add the correct sources
RUN rm -f /etc/apt/sources.list.d/* && \
    echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Expose the port your app runs on
EXPOSE 8000

# Run migrations and start Gunicorn (adjust as needed)
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
