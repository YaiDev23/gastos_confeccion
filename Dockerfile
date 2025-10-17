# Container image for the gastos_confeccion FastAPI app
FROM python:3.11-slim

# Do not write .pyc files and ensure stdout/stderr are not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal build deps (kept small); comment out if unnecessary
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (note the repository file is spelled 'requierements.txt')
COPY requierements.txt /app/requierements.txt

RUN pip install --no-cache-dir -r /app/requierements.txt

# Copy project
COPY . /app

# The FastAPI app module lives at app/main.py, so point Uvicorn to app.main:app
EXPOSE 10001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
