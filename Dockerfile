FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn_config.py .
COPY app.py . 

CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]