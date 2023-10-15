# Use an official Python runtime as the parent image
FROM python:3.11

# Set the working directory in the docker
WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt


# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
EXPOSE 8000

# Define the startup command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

