# Start producer code

Listed below are all the steps needed to start a interactive container to send data to kafka. 

## **Step 1**: Start interactive container

The following command will create a temporary pod within the python namespace using the image `hansaskov/producer`. And give you a command line to interface with
``` bash
kubectl run producer -n python -i --rm --tty --image hansaskov/producer -- bash 
```

## **Step 2**: Start python program
When the interactive container has been setup you can start the python program as follows.

```bash
python  main.py
```

 The program will download the dataset and begin sending the data to kafka in real time

