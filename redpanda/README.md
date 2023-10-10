
In this guide, we'll walk through the process of deploying Redpanda on Kubernetes using cert-manager and Helm. Let's break this down step-by-step.

### **Step 1: Check for Permissions**

Before you proceed, it's essential to ensure you have the necessary permissions to install custom resource definitions (CRDs) in your cluster.

Execute the following command:

```
kubectl auth can-i create CustomResourceDefinition --all-namespaces
```

The output should display `yes` if you have the correct permissions.

### **Step 2: Installing cert-manager**

Cert-manager helps manage certificate authorities in your Kubernetes cluster. Use Helm, a Kubernetes package manager, to install it:

1. Add the Jetstack repository:

```
helm repo add jetstack https://charts.jetstack.io
```

2. Update your Helm repository:

```
helm repo update
```

3. Install cert-manager:

```
helm install cert-manager jetstack/cert-manager --set installCRDs=true --namespace cert-manager --create-namespace
```

### **Step 3: Setting Up Redpanda Operator CRDs**

Now, install the Redpanda Operator custom resource definitions (CRDs):

```
kubectl kustomize https://github.com/redpanda-data/redpanda//src/go/k8s/config/crd | kubectl apply -f -
```

### **Step 4: Deploying the Redpanda Operator**

1. Add the Redpanda repository:

```
helm repo add redpanda https://charts.redpanda.com
```

2. Deploy the Redpanda Operator:

```
helm upgrade --install redpanda-controller redpanda/operator \
  --namespace redpanda \
  --set image.repository=docker.redpanda.com/redpandadata/redpanda-operator \
  --set image.tag=v23.2.10 \
  --create-namespace
```

### **Step 5: Verifying Deployment Rollout**

To ensure that the Redpanda Operator has been successfully deployed:

```
kubectl --namespace redpanda rollout status --watch deployment/redpanda-controller-operator
```

### **Step 6: Installing the Redpanda Custom Resource**

With the operator in place, you can now deploy a Redpanda custom resource. Here's a sample configuration with SASL enabled, saved as `redpanda-cluster.yaml`:

```
apiVersion: cluster.redpanda.com/v1alpha1
kind: Redpanda
metadata:
  name: redpanda
spec:
  chartRef: {}
  clusterSpec:
    external:
      domain: customredpandadomain.local
    statefulset:
      replicas: 3
      initContainers:
        setDataDirOwnership:
          enabled: true
```

To apply this configuration:

```
kubectl apply -f redpanda-cluster.yaml --namespace redpanda
```

### **Step 7: Verifying Redpanda Broker Scheduling**

Ensure that each Redpanda broker is scheduled on only one Kubernetes node with the following command:

```
kubectl get pod --namespace redpanda  \
  -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name -l \
  app.kubernetes.io/component=redpanda-statefulset
```

The expected output should resemble:

```
bds-g12-n2   redpanda-1
bds-g12-n0   redpanda-2
bds-g12-n1   redpanda-0
```

---

Congratulations! You've successfully deployed Redpanda on Kubernetes using cert-manager and Helm.
