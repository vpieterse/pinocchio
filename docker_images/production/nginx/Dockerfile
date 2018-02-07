# Use official alpine image as base
FROM alpine:3.7

# Install nginx
RUN apk add --no-cache nginx

# Create folder for logs
RUN mkdir -p /app/logs/

# Copy nginx config file
WORKDIR /etc/nginx/
ADD nginx.conf .
ADD uwsgi_params .

CMD ["nginx"]