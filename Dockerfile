# Dockerfile for GUI
# Swarmchestrate GUI web application

FROM python:3.13-slim-bookworm

LABEL maintainer="Swarmchestrate"
LABEL description="GUI for registering capacities and applications in Swarmchestrate"
LABEL version="1.0.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=gui.settings

ARG NODE_MAJOR=24

WORKDIR /gui

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get update && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json ./
RUN npm ci

COPY . .

RUN SECRET_KEY=build-only-secret \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    DATABASE_ENGINE=django.db.backends.sqlite3 \
    DATABASE_NAME=/tmp/gui-build.sqlite3 \
    API_URL=http://127.0.0.1 \
    USE_MOCK_API=True \
    python manage.py compilescss && \
    SECRET_KEY=build-only-secret \
    DEBUG=False \
    ALLOWED_HOSTS=localhost \
    DATABASE_ENGINE=django.db.backends.sqlite3 \
    DATABASE_NAME=/tmp/gui-build.sqlite3 \
    API_URL=http://127.0.0.1 \
    USE_MOCK_API=True \
    python manage.py collectstatic --noinput

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/')" || exit 1

CMD ["gunicorn", "gui.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
