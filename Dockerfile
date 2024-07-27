FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY .env /app/.env

RUN pip install -r /app/requirements.txt

COPY . /app/

CMD alembic revision --autogenerate -m "Create Table" \
	&& alembic upgrade heads \
	&& uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000