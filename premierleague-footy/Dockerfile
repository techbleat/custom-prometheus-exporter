FROM python:3.9
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
COPY exporter.py /usr/src/app/
CMD python3 exporter.py
