FROM python:3.11 as builder

WORKDIR /app

RUN pip install --upgrade pip
RUN mkdir -p /secrets

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python3", "main.py"]