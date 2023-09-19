FROM python:3.10-slim

ENV Production=0

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY ./main.py /code/main.py
COPY ./__init__.py /code/__init__.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]