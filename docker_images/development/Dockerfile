# Use official Python 3.6 image as base
FROM python:3.6.4-slim-stretch

# Copy pip's requirements.txt file to download Django on container build
#RUN mkdir /app
VOLUME ["/app"]
WORKDIR /app
COPY requirements.txt .

# Install project requirements
RUN pip install -r requirements.txt

# Disable python output buffering
ENV PYTHONUNBUFFERED 0

# Default command for container is to run the Django server
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
