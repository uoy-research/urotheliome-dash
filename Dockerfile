FROM python:3.12
WORKDIR /usr/local/app

COPY . .
EXPOSE 8080

RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", ":8080", "wsgi:server"]