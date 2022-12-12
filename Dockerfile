FROM python:3.9-alpine

LABEL desc="Phototur v1"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /project
RUN mkdir /log
WORKDIR /project
COPY ./app /project/app
COPY ./utils /project/utils
COPY ./config.py /project/config.py
COPY ./main.py /project/main.py

EXPOSE 8563

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8563", "-w", "3", "main:app"]
