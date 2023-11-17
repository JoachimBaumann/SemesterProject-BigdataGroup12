FROM python:3.11

# Install unzip utility
RUN apt-get update && apt-get install -y unzip && apt-get install -y jq

WORKDIR /app

# Copy the project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#CMD ["python", "main.py"]
