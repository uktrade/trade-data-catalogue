FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
  apt-get install -y curl && \
  curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
  apt-get install -y nodejs && \
  apt-get clean

COPY . /app/

RUN npm install --prefix /app

RUN cp /app/sample.env /app/.env

EXPOSE 8000

CMD ["python", "trade_data_catalogue/manage.py", "runserver", "0.0.0.0:8000"]
