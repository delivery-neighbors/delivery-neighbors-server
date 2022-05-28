FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim  # 도커 안에서 vi 설치 안해도 됨.

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --settings=BACKEND.settings.deploy --no-input"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
