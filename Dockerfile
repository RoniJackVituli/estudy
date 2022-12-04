FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG 0
WORKDIR /Estudy_Project
ADD . /Estudy_Project
EXPOSE 8000

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/Estudy_Project/docker-entrypoint.sh"]
#CMD gunicorn Estudy_Project.wsgi:application --bind 0.0.0.0:$PORT
