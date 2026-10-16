# Set up a Python 3.14 environment
FROM python:3.14-slim

# Define the working directory inside the container
WORKDIR /app

# Copy the necessary application files
COPY /crud/models /app/crud/models
COPY /crud/pages /app/crud/pages
COPY /crud/repos /app/crud/repos

COPY admin.py /app/admin.py

# Install streamlit
RUN pip install streamlit==1.65.0