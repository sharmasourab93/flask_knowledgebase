FROM python:latest

WORKDIR /src/ 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY run.py /src/.
COPY flask_kb/. /src/flask_kb/.
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/src/flask_kb/"

CMD ["gunicorn", "--bind", "0.0.0.0:5000","run", "-w", "1"]
