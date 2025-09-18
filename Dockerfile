# 🔬 Compensation Research System - Production Container
FROM python:3.11-slim-bullseye

# Metadata
LABEL maintainer="Compensation Research Team <research@compensation.ai>"
LABEL description="Automated compensation research system with 5WHY methodology"
LABEL version="1.0.0"

# Environment Variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV DEBIAN_FRONTEND=noninteractive

# System Dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create Application User
RUN groupadd --gid 1000 research && \
    useradd --uid 1000 --gid research --shell /bin/bash --create-home research

# Working Directory
WORKDIR /app

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Code
COPY --chown=research:research . .

# Create Required Directories
RUN mkdir -p \
    /app/logs \
    /app/cache \
    /app/backups \
    /app/Compensation-Research-Vault \
    && chown -R research:research /app

# Switch to Non-Root User
USER research

# Health Check
HEALTHCHECK --interval=5m --timeout=30s --start-period=1m --retries=3 \
    CMD python scripts/health_check.py || exit 1

# Volume Mounts
VOLUME ["/app/Compensation-Research-Vault", "/app/logs", "/app/cache", "/app/backups"]

# Expose Ports (for monitoring)
EXPOSE 8080

# Default Command
CMD ["python", "compensation_research_system.py", "--mode=production"]

# Multi-stage build optimization
FROM python:3.11-slim-bullseye as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim-bullseye as runtime

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH=/home/research/.local/bin:$PATH

RUN groupadd --gid 1000 research && \
    useradd --uid 1000 --gid research --shell /bin/bash --create-home research

COPY --from=builder /root/.local /home/research/.local
COPY --chown=research:research . /app

WORKDIR /app
USER research

CMD ["python", "compensation_research_system.py"]