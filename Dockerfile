FROM python:3.9-slim

# Install Rust and dependencies (if necessary for your project)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libssl-dev \
    pkg-config \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set Rust and cargo home directories (if needed for your project)
ENV CARGO_HOME=/tmp/cargo
ENV CARGO_TARGET_DIR=/tmp/target

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app
WORKDIR /app

# Replace app.py with register.py here
CMD ["python", "register.py"]
