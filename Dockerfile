FROM python:3.12
WORKDIR /usr/local/app/DashApp

COPY requirements.txt ../requirements.txt
COPY DashApp/ ./
EXPOSE 8080

RUN pip install -r ../requirements.txt
#CMD ["gunicorn", "-b", ":8080", "wsgi:server"]
CMD ["python", "app.py"]