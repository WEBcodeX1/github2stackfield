FROM ghcr.io/webcodex1/x0-app

# Install github2stackfield Python backend dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages \
    requests \
    psycopg2-binary \
    pgdbpool \
    git+https://github.com/clauspruefer/python-micro-esb.git
