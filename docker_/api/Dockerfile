FROM python:3.8-slim

WORKDIR /

RUN echo deb http://httpredir.debian.org/debian/ buster main contrib non-free >> /etc/apt/sources.list \
    && echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections \
    && apt-get upgrade \
    && apt-get update \
    && apt-get install -y \
    apt-utils \
    ttf-mscorefonts-installer \
    libreoffice-writer \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/

COPY ./requirements.txt ./req.txt

COPY . .

RUN pip3 install -r req.txt

ENV PYTHONPATH "/"

WORKDIR /app

CMD ["python3", "api.py"]
