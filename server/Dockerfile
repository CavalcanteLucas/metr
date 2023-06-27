FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install "setuptools<58.0.0"
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000
