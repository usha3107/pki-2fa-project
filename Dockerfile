# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install cron + timezone data
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy app code and scripts and cron config
COPY app ./app
COPY scripts ./scripts
COPY cron ./cron

# Copy keys into container
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem

# Install cron file
RUN chmod 0644 /app/cron/2fa-cron && \
    crontab /app/cron/2fa-cron

# Create volume mount points
RUN mkdir -p /data /cron && \
    chmod 755 /data /cron

VOLUME ["/data", "/cron"]

EXPOSE 8080

# Start cron and FastAPI
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
