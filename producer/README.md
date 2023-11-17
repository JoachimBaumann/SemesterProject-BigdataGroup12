# Start producer code

Listed below are all the steps needed to start a interactive container to send data to kafka. 

## Setup Kubernetes Container

Small guide to start producer that sends data to kafka

### **Step 1**: Start interactive container

The following command will create a temporary pod within the python namespace using the image `hansaskov/producer`. And give you a command line to interface with
```
kubectl run producer -n python -i --rm --tty --image hansaskov/producer -- bash 
```

### **Step 2**: Start python program

The python program will download the dataset and begin sending the data to kafka in real time

    ``` bash
    python  main.py
    ```


