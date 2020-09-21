FROM python:3.8
EXPOSE 5000
ENV FLASK_APP app.py
COPY . /app
WORKDIR /app
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install", "--system", "--deploy", "--ignore-pipfile"]
RUN ["python", "create_db.py"]
CMD ["flask", "run", "--host", "0.0.0.0"]
