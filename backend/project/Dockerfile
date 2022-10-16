FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update
RUN apt-get install nano

COPY . .

CMD ["gunicorn", "project.wsgi:application", "--bind", "0:8000" ]
