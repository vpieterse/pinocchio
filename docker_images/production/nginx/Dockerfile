# Use official alpine image as base
FROM alpine:3.7

RUN apk add --no-cache nginx

# Copy nginx config file
WORKDIR /etc/nginx/
ADD nginx.conf .
ADD uwsgi_params .

CMD ["nginx"]