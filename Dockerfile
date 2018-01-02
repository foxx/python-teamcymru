# Uses the official Docker Python 3 image based on Alpine Linux.
# See: https://hub.docker.com/_/python/
FROM python:3.6-alpine
LABEL authors="Walid ZIOUCHE <wziouche@gmail.com>"

# Some useful env variables, in one Docker layer
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Create and set /teamcymru as the working directory for this container
WORKDIR /teamcymru

# Copy source files
COPY . /teamcymru

# Install Python dependencies but first Make sure we have the latest pip version
RUN pip install --upgrade pip && pip install --no-cache-dir -r /teamcymru/dev-requirements.txt
