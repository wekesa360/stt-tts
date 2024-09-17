FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    libespeak1 \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    libmagic1 \
    libffi-dev \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --no-binary cffi cffi
RUN pip install --no-cache-dir -r requirements.txt

RUN export PORT=3000

COPY ./app .

CMD [ "sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}" ]
