# 🐳 Base DinD image
FROM docker:24-dind

# 📦 Install Python, pip, build tools, lib dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-wheel \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    make \
    bash \
    curl \
    git

# 🐍 Set up Python virtual environment
RUN python3 -m venv /opt/venv

# 🔧 Set PATH to use venv by default
ENV PATH="/opt/venv/bin:$PATH"

# ✅ Upgrade pip inside venv
RUN pip install --upgrade pip setuptools

# 🧪 Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG DJANGO_SETTINGS_MODULE=nocodi.settings

# 🏗️ Set work directory
WORKDIR /src

# 🧾 Copy requirements and install in venv
COPY requirements.txt /src/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --retries 10 -r requirements.txt

# 📁 Copy project files
COPY . /src/

# 🧼 Collect static files
RUN python manage.py collectstatic --noinput

# 📡 Expose port
EXPOSE 8000

# 🚀 Run Gunicorn using Python from venv
CMD ["gunicorn", "--workers", "1", "--timeout", "30", "--chdir", "/src", "--bind", "0.0.0.0:8000", "nocodi.wsgi:application"]
