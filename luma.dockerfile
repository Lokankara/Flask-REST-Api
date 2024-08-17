FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /tests

RUN apt-get update && apt-get install -y \
    curl \
    software-properties-common \
    python3-launchpadlib \
    fonts-liberation \
    jq \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    unzip \
    openjdk-17-jre \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json' \
    | jq -r '.channels.Stable.downloads|.chrome,.chromedriver|.[]|select(.platform=="linux64").url|"curl -LO \(.)"' \
    | bash \
    && unzip -d /usr/local/share 'chrome-linux64.zip' \
    && ln -s /usr/local/share/chrome-linux64/chrome /usr/bin/chrome \
    && unzip -d /usr/local/share 'chromedriver-linux64.zip' \
    && ln -s /usr/local/share/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && rm 'chrome-linux64.zip' && rm 'chromedriver-linux64.zip'

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY pytest.ini /tests/pytest.ini
COPY conftest.py /tests/conftest.py
COPY ./data /tests/data
COPY ./pages /tests/pages
COPY ./tests /tests/tests

ENV CI_RUN=true
CMD ["pytest", "-n2", "-s", "-v", "--reruns=5"]
