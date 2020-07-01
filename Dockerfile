FROM nginx:1.18.0

RUN apt-get install nginx 
RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/nginx.conf /etc/nginx/
COPY nginx/project.conf /etc/nginx/conf.d/
EXPOSE 80
# RUN nginx


WORKDIR /src/. 

RUN apt-get install python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN python -m pip install --upgrade pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY run.py /src/ 
COPY flask_kb /src/flask_kb

ENV PYTHONPATH "${PYTHONPATH}:/src/flask_kb/"

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run", "-w", "1"]
CMD ["gunicorn", "run", "-w","1"]
RUN nginx
