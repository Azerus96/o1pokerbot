FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libevent-dev \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --no-binary :all: gevent

COPY . .

EXPOSE 10000

CMD ["python", "web_server.py"]
