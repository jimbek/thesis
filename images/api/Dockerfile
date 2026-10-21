# Set up a Python 3.14 environment.
FROM python:3.14-slim

# Define the working directory inside the container.
WORKDIR /app

# Copy the necessary application files.
COPY /crud/models /app/crud/models
COPY /crud/repos /app/crud/repos
COPY /crud/routes /app/crud/routes

COPY api.py /app/api.py

# Install requirements.
COPY images/api/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on.
EXPOSE 5000

# Run the application.
CMD ["python", "api.py"]