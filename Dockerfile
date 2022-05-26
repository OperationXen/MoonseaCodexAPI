FROM python:3-alpine

WORKDIR /moonseacodex_api
COPY . /moonseacodex_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python external libs, and web server packages
RUN apk update && apk add --no-cache apache2 apache2-ctl apache2-mod-wsgi postgresql-dev build-base
# Update tooling and install required packages
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
RUN mv /moonseacodex_api/deploy/apache-wsgi.conf /etc/apache2/sites-available/ && a2enmod wsgi && a2ensite apache-wsgi

CMD apachectl -D foreground
