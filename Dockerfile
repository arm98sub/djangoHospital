FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY . /app/

WORKDIR /app/

RUN pip install pipenv
RUN pipenv install --system

RUN pip3 install --upgrade setuptools
RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 8080
