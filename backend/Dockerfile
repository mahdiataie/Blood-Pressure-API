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

