FROM python:alpine3.17
WORKDIR /app
COPY . /app
RUN pip install -r requirements/dev-requirements.txt
ENTRYPOINT ["python", "uvicorn main:app --host 0.0.0.0 --port 8000]
