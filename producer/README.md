# Kubernetes Python Container Setup Guide

Follow this step-by-step guide to set up a Python environment in a Kubernetes container, upload the required data and code, install dependencies, and run Python scripts.

## 1. Create an Interactive Python Container

Set up a namespace named `python` and launch an interactive Python container within it:

```bash
kubectl create namespace python
kubectl run python  -n python -i --tty --image python:3.11 -- bash 
```

## 2. Upload Code to the Container

First, clean any existing `producer` folder, and then copy your local `producer` folder to the root of the container:

```bash
kubectl exec -n python python -- rm -rf /producer
kubectl cp producer python:/ -n python
```

## 3. Upload Dataset to the Container

a. Create a `datasets` directory inside the container:

```bash
kubectl exec -n python python -- mkdir datasets
```

b. Copy the `bus_dataset.zip` file to the `datasets` directory and unzip it:

```bash
kubectl cp datasets/bus_dataset.zip python:/datasets -n python
kubectl exec -n python python -- unzip /datasets/bus_dataset.zip -d /datasets/bus_dataset/
```

## 4. Install Python Dependencies

Make sure you have a `requirements.txt` file in your `producer` folder, then install the dependencies:

```bash
kubectl exec -it python -n python -- pip install -r /producer/requirements.txt
```

## 5. Run the Python Script

Execute the main script from the `producer` folder:

```bash
kubectl exec -it python -n python -- python /producer/main.py
```

## 6. Alternative Method: One-Liner to Setup and Run Python Script

If you'd like to quickly clean the `producer` folder, upload code, and run the script in one command, use the following:

```bash
kubectl exec -n python python -- rm -rf /producer && \
kubectl cp producer python:/ -n python && \
kubectl exec -it python -n python -- python /producer/main.py
```

That's all! Follow the steps above to seamlessly run your Python code within a Kubernetes container.
