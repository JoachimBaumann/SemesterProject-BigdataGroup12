# Kubernetes Python Container Setup Guide

Follow this step-by-step guide to set up a Python environment in a Kubernetes container, upload the required data and code, install dependencies, and run Python scripts.


## Setup Kubernetes Container

### **Step 1**: Download Datasets

Navigate to the Kaggle pages and download the following datasets within the `datasets` folder:

- [**New York City Taxi Trips**](https://www.kaggle.com/datasets/dhruvildave/new-york-city-taxi-trips-2019)
- [**New York City Bus Data**](https://www.kaggle.com/datasets/stoney71/new-york-city-transport-statistics)

### **Step 2**: Rename Files

After downloading, rename the datasets for consistency:

- **Taxi Dataset**: `taxi_dataset.zip`
- **Bus Dataset**: `bus_dataset.zip`

### **Step 3**: Verify Folder Structure

Ensure your `datasets` folder aligns with the structure below:

```
datasets
├── bus_dataset.zip
└── taxi_dataset.zip
```

### **Step 4**: Create an Interactive Python Container

Initialize a namespace named `python` and launch an interactive Python container:

```
kubectl create namespace python
kubectl run python  -n python -i --tty --image python:3.11 -- bash 
```

### **Step 5**: Transfer Datasets to the Container

1. Generate a `datasets` directory in the container:

    ```
    kubectl exec -n python python -- mkdir datasets
    ```

2. Transfer and decompress the datasets:

    - **Bus Dataset**:

        ```
        kubectl cp datasets/bus_dataset.zip python:/datasets -n python
        kubectl exec -n python python -- unzip /datasets/bus_dataset.zip -d /datasets/bus_dataset/
        ```

    - **Taxi Dataset**:

        ```
        kubectl cp datasets/taxi_dataset.zip python:/datasets -n python
        kubectl exec -n python python -- unzip /datasets/taxi_dataset.zip -d /datasets/taxi_dataset/
        ```

_Note: Dataset transfer may take a while, so patience is key._

---

## Upload and Execute Python Code

### **Step 1**: Transfer Code to the Container

1. Eliminate any pre-existing `producer` folder.
2. Copy your local `producer` folder to the container root:

    ```
    kubectl exec -n python python -- rm -rf /producer
    kubectl cp producer python:/ -n python
    ```

### **Step 2**: Install Python Dependencies

Ensure a `requirements.txt` file is present in your `producer` folder and then install the dependencies:

```
kubectl exec -it python -n python -- pip install -r /producer/requirements.txt
```

### **Step 3**: Execute the Python Script

Run the main script located in the `producer` folder:

```
kubectl exec -it python -n python -- python /producer/main.py
```

### *Alternative One-Liner*

For a rapid setup to clean the `producer` folder, upload code, and execute the script:

```
kubectl exec -n python python -- rm -rf /producer && \
kubectl cp producer python:/ -n python && \
kubectl exec -it python -n python -- python /producer/main.py
```

---

Thank you for following this guide! Use the steps above to smoothly run your Python scripts within a Kubernetes container.
