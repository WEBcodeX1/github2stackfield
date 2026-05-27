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

# Link the x0 base stylesheets and fontawesome into the app subdir so that
# the x0 framework can find bootstrap.css, globalstyles.css and all.min.css
# at the {subdir}/ path it generates in the HTML <link> tags.
# globalstyles.css is copied (not symlinked) so that app-specific overrides
# for notification indicator styles (IndicatorSuccess, IndicatorWarning, ...)
# are included.
RUN ln -s /var/www/vhosts/x0/static/bootstrap.css /var/www/vhosts/x0/static/github2sf/bootstrap.css \
    && ln -s /var/www/vhosts/x0/static/fontawesome /var/www/vhosts/x0/static/github2sf/fontawesome

# Copy Python WSGI backend scripts into the x0 python directory
COPY python/ /var/www/vhosts/x0/python/github2sf/

# Install the supplementary Apache2 configuration snippet
COPY docker/apache2.conf /etc/apache2/conf-enabled/github2sf.conf
