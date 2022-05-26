FROM python:3

WORKDIR /moonseacodex_api
COPY . /moonseacodex_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python external libs, and web server packages
RUN apt update && apt install apache2 libapache2-mod-wsgi-py3 libpq-dev -y
# Update tooling and install required packages
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
# Enable site
RUN mv /moonseacodex_api/deploy/api.conf /etc/apache2/sites-available/api.conf && a2ensite api

CMD ["apachectl", "-D",  "FOREGROUND"]
