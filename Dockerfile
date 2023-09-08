FROM python:3.10
LABEL authors="Dhaval.Mayatra"

WORKDIR /var/ey

COPY requirements.txt           requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY config config
COPY script.py script.py

RUN mkdir "data"

CMD python script.py