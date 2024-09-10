FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:./src/zenmlplayground"
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

#RUN pip install -e .
