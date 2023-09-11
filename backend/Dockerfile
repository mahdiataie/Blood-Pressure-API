# Use an official Python runtime as a parent image
FROM python:3.8


RUN pip install --upgrade pip
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "deinhaus.asgi:application"]


# Use an official Python runtime as a parent image
# FROM python:3.8-slim

# # Set environment variables for Python
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application code into the container
# COPY . /app/

# # Expose the port that the application will run on
# EXPOSE 8000

# # Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
