## Apply image to kubernetes. A Step-by-Step Guide 

#### 1. Apply the frontend
Apply your service configuration to make it available.

``` bash
kubectl apply -f frontend.yaml -n frontend
```

#### 2. Port Forward UI
To access the user interface via port forwarding, use the following command:

``` bash
kubectl -n frontend port-forward svc/swegroup12-service 3000:3000
```

After executing this command, you can access the user interface by navigating to `http://localhost:3000` in your web browser.

