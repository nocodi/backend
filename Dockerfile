FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG DJANGO_SETTINGS_MODULE=nocodi.settings

WORKDIR /src

COPY requirements.txt /src/

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --retries 10 -r requirements.txt

COPY . /src/

EXPOSE 8000

# Command to run the application using Gunicorn
CMD ["gunicorn", "--timeout", "30", "--chdir", "/src", "--bind", "0.0.0.0:8000", "nocodi.wsgi:application"]
