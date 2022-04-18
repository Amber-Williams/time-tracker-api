FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install repo dependencies
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-root --no-dev

COPY ./app /app/

CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]

