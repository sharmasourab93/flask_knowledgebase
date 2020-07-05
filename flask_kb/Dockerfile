FROM python:latest

WORKDIR /src/. 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt 

COPY run.py /src/
COPY ./configs /src/flask_kb/configs/
COPY ./routes.py /src/flask_kb/
COPY ./__init__.py /src/flask_kb/
COPY ./models /src/flask_kb/models/
COPY ./log /src/flask_kb/log/
# COPY ./entrypoint.sh /src/

ENV PYTHONPATH "${PYTHONPATH}:/src/flask_kb/"
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "run", "&"]
# ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
