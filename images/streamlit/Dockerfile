# Set up a Python 3.14 environment
FROM python:3.14-slim

# Define the working directory inside the container
WORKDIR /app

# Copy the necessary application files
COPY /crud/library /app/crud/library
COPY /crud/models /app/crud/models
COPY /crud/pages /app/crud/pages
COPY /crud/repos /app/crud/repos
COPY /crud/services /app/crud/services

COPY admin.py /app/admin.py

# Install requirements
COPY images/streamlit/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN playwright install chromium
RUN playwright install msedge