FROM python:3.9.6

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ADD . /app/
WORKDIR /app/

CMD [ "python", "main.py" ]