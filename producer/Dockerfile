FROM python:3.9-slim

# Install unzip utility
RUN apt-get update && apt-get install -y unzip

WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the datasets into the container and unzip them
COPY bus_dataset.zip /datasets/
COPY taxi_dataset.zip /datasets/
RUN unzip /datasets/bus_dataset.zip -d /datasets/bus_dataset/ && \
    unzip /datasets/taxi_dataset.zip -d /datasets/taxi_dataset/

CMD ["python", "main.py"]
