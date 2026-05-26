FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    requests \
    psycopg2-binary \
    pgdbpool

# Install python-micro-esb from source
RUN pip install --no-cache-dir \
    git+https://github.com/clauspruefer/python-micro-esb.git

# Install x0 framework Python modules
RUN pip install --no-cache-dir \
    git+https://github.com/WEBcodeX1/x0.git

WORKDIR /var/www/x0

# Apache configuration
COPY docker/apache2.conf /etc/apache2/sites-available/github2sf.conf
RUN a2ensite github2sf && a2dissite 000-default && a2enmod wsgi

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
