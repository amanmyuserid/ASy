# Base image: slim version
FROM python:3.11.6-slim

WORKDIR /app

# Set BLIS_ARCH environment variable (recommended syntax)
ENV BLIS_ARCH=generic

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    cmake \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Pre-install common build dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy==1.26.4 Cython==0.29.37

COPY requirements.txt .

# Use --prefer-binary to force pre-built wheels if available
RUN pip install --prefer-binary -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "ui.py"]
