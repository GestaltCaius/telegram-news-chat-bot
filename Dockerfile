FROM python:3.9-alpine3.19

WORKDIR /app

# RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "scripts.run_bot"]