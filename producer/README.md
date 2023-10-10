## Create interactive pyton container
``` bash
kubectl create namespace python
kubectl run python  -n python -i --tty --image python:3.11 -- bash 
```

## Upload folder
```bash
kubectl exec -n python python -- rm -rf /producer
kubectl cp producer python:/ -n python
```

## Install dependencies
```bash
kubectl exec -it python -n python -- pip install -r /producer/requirements.txt
```

## Run python 
```bash
kubectl exec -it python -n python -- python /producer/main.py
```

