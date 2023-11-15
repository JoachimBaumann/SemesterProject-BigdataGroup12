# Local deployment

## Development
To start the development server run:
```bash
bun run dev
```

Open http://localhost:3000/ with your browser to see the result.


# Apply image to kubernetes. 

### Step-by-Step Guide

#### 1. Create a Deployment Configuration
Create a file named `deployment.yaml` with the following content to define your Kubernetes deployment in the `frontend` namespace.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swegroup12-deployment
  namespace: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: swegroup12
  template:
    metadata:
      labels:
        app: swegroup12
    spec:
      containers:
      - name: swegroup12
        image: hansaskov/swegroup12:latest
        ports:
        - containerPort: 3000
```

#### 2. Apply the Deployment
Deploy your configuration to your Kubernetes cluster.

```
kubectl apply -f deployment.yaml -n frontend
```

#### 3. Create a Service
Create a file named `service.yaml` to expose your application. This service will also be in the `frontend` namespace.

```
apiVersion: v1
kind: Service
metadata:
  name: swegroup12-service
  namespace: frontend
spec:
  type: NodePort
  selector:
    app: swegroup12
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30000
```

#### 4. Apply the Service
Apply your service configuration to make it available.

```
kubectl apply -f service.yaml -n frontend
```

#### 5. Port Forward UI
To access the user interface via port forwarding, use the following command:

```
kubectl -n frontend port-forward svc/swegroup12-service 3000:3000
```

After executing this command, you can access the user interface by navigating to `http://localhost:3000` in your web browser.

