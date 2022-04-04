FROM python:3.6-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN set -eux; \
        apt-get update; \
        apt-get install -y --no-install-recommends gcc; \
	apt-get install -y  python3-dev; \
	apt-get install -y libevent-dev; \
        apt-get -y  autoremove gcc; \
        rm -rf /var/lib/apt/lists/*

COPY ./ /usr/src/app

CMD ["python","/usr/src/app/code.py"]