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

# Copy static x0 config files into the web-server document root
COPY static/ /var/www/vhosts/x0/static/github2sf/

# Copy Python WSGI backend scripts into the x0 python directory
COPY python/ /var/www/vhosts/x0/python/github2sf/

# Install the supplementary Apache2 configuration snippet
COPY docker/apache2.conf /etc/apache2/conf-enabled/github2sf.conf
