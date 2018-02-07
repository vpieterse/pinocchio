# Use default alpine image as base. Python will be installed by apk adding uwsgi
FROM alpine:3.7

# Copy pip's requirements.txt file to download Django on container build
VOLUME ["/app"]
WORKDIR /app
COPY requirements.txt .

# Install uwsgi and tini
RUN apk add --no-cache uwsgi-python3 tini uwsgi-http
ENTRYPOINT ["/sbin/tini", "-g", "--"]

# Install project requirements
RUN pip3 install -r requirements.txt

# Disable python output buffering
ENV PYTHONUNBUFFERED 0

# Start UWSGI server
# TODO (Raymond): Run uwsgi as regular user?
# TODO (Raymond): uwsgi config file?
# TODO (Raymond): collectstatic?
CMD uwsgi --plugin http,python3 --socket 0.0.0.0:8001 --module pinocchio.wsgi
