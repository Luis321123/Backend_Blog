FROM python:3.12
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./.env /app/.env

RUN useradd -rm -d /code -s /bin/bash -g root -G sudo -u 1001 ubuntu

COPY ./startup.sh /app/startup.sh

RUN chmod +x /app/startup.sh

# copy requirements file
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install --no-cache-dir setuptools

USER ubuntu

EXPOSE 8000

COPY ./app /app/app/

COPY ./alembic.ini /app/alembic.ini

COPY ./alembic /app/alembic

ENV PYTHONPATH=/app
    
USER root

RUN chown -R ubuntu /app/alembic/versions/

CMD bash -c 'uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload'