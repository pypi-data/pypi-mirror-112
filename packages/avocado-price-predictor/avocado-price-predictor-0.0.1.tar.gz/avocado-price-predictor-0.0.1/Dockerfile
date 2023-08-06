# Python base image
FROM python:3.7

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

RUN mkdir /.cache && chmod g+w /.cache .

# --insecure for static files serving.
CMD ["python", "manage.py", "runserver", "--insecure", "0.0.0.0:8000"]