# Use default alpine image as base. Python will be installed by apk adding uwsgi
FROM alpine:3.7

# Install uwsgi and tini
RUN apk add --no-cache uwsgi-python3 tini uwsgi-http uwsgi-logfile
ENTRYPOINT ["/sbin/tini", "-g", "--"]

# Copy pip's requirements.txt file to download Django on container build
WORKDIR /tmp
COPY requirements.txt .

# Install project requirements
RUN pip3 install -r requirements.txt

# Disable python output buffering
ENV PYTHONUNBUFFERED 0

# Start UWSGI server
# TODO (Raymond): Run uwsgi as regular user?
# TODO (Raymond): uwsgi config file?
# TODO (Raymond): Log to a file? --logger file:/app/logs/uwsgi.log
WORKDIR /app
CMD mkdir -p /app/logs && \
 uwsgi --plugin logfile,python3 --socket 0.0.0.0:8001 --module pinocchio.wsgi
