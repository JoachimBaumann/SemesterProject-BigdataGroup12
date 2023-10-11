## Create interactive pyton container
``` bash
kubectl create namespace python
kubectl run python  -n python -i --tty --image python:3.11 -- bash 
```

## Upload code to folder
```bash
kubectl exec -n python python -- rm -rf /producer
kubectl cp producer python:/ -n python
```

## Upload dataset
```bash
kubectl exec -n python python -- mkdir datasets
kubectl cp datasets/bus_dataset.zip python:/datasets -n python
kubectl exec -n python python -- unzip /datasets/bus_dataset.zip -d /datasets/bus_dataset/

```

## Install dependencies
```bash
kubectl exec -it python -n python -- pip install -r /producer/requirements.txt
```

## Run python 
```bash
kubectl exec -it python -n python -- python /producer/main.py
```


## Run python 2.0
```bash
kubectl exec -n python python -- rm -rf /producer && \
kubectl cp producer python:/ -n python && \
kubectl exec -it python -n python -- python /producer/main.py
```