# Start producer code

Listed below are all the steps needed to start a interactive container to send data to kafka.

## Start deployment
The recomended way to start the producer with a deployment. The deployment will automaticly download the needed dataset and begin sending it to kafka: 

```bash
kubectl apply -f deployment.yaml -n producer
```

## **Optional** Additional messages

If the producer already exists run the following:

```bash
kubectl -n producer exec -it producer -- bash
```

Then start sending messages by starting the main function

```bash
python  main.py
```
