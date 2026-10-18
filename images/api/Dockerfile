# Set up a Python 3.14 environment.
FROM python:3.14-slim

# Define the working directory inside the container.
WORKDIR /app

# Copy the necessary application files.
COPY /crud/models /app/crud/models
COPY /crud/repos /app/crud/repos
COPY /crud/routes /app/crud/routes

COPY api.py /app/api.py

# Install Flask.
RUN pip install Flask==3.1.3

# Expose the port the app runs on.
EXPOSE 5000

# Run the application.
CMD ["python", "api.py"]