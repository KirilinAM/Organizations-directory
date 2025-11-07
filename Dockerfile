FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \ 
    && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python пакеты
RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system --deploy

COPY ./ ./

ENV DB_HOST=host.docker.internal
ENV DB_PORT=5432
ENV DB_NAME=main

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]