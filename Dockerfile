FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /django-tech-test
COPY . /django-tech-test/
RUN pip3 install -r requirements.txt
ENTRYPOINT python manage.py runserver 0.0.0.0:8000
