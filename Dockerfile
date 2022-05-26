FROM python:3.11-rc-slim

WORKDIR /moonseacodex_api
COPY . /moonseacodex_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python external libs, and web server packages
RUN apt update && apt install zlib1g libjpeg-dev apache2 -y
# Update tooling and install required packages
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]