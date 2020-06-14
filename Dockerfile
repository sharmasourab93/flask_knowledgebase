FROM python:latest

WORKDIR /src/ 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


RUN pip install --upgrade pip
COPY app.py /src/.
COPY . . 
COPY wsgi.py /src/.
COPY load_configs.py /src/.
COPY requirements.txt /src/requirements.txt
COPY config.yaml /src/. 

RUN pip install -r requirements.txt 

CMD ["gunicorn", "--bind", "0.0.0.0:5000","wsgi", "-w", "1"]
