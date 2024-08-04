FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]
