FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN pip install --upgrade pip

COPY requirements/dev-requirements.txt .

RUN pip install -r dev-requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
