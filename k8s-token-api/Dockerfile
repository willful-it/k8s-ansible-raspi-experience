FROM python:3.7

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN pip install uvicorn

EXPOSE 80

COPY ./app /app

ENV PYTHONPATH "/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
