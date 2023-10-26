# How to Monitor Redpanda Clusters with the Prometheus Operator

_This guide has taken inspiration from [Grafana Blog](https://grafana.com/blog/2023/01/19/how-to-monitor-kubernetes-clusters-with-the-prometheus-operator/) and [Redpanda Docs](https://docs.redpanda.com/current/manage/kubernetes/monitor/#generate-grafana-dashboard)._

To make this quick, I will go over this as fast as possible. This is a guide to set up monitoring of Redpanda using Prometheus and Grafana. It is assumed that you have followed and set up the Redpanda cluster using the guide found at the [redpanda readme](../README.md)

## Step 1: Prometheus Operator

You're going to deploy Prometheus Operator in your cluster, then configure permissions for the deployed operator to scrape targets in your cluster.

You can deploy by applying the `bundle.yaml` file from the Prometheus Operator GitHub repository:

```bash
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml
```

If you run into the error "The CustomResourceDefinition 'prometheuses.monitoring.coreos.com' is invalid: metadata.annotations: Too long: must have at most 262144 bytes," then run the following command:

```bash
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml --force-conflicts=true --server-side=true
```

This command allows you to deploy Prometheus Operator CRD without Kubernetes altering the deployment when it encounters any conflicts while installing the operator in your cluster. In this scenario, your cluster complains of a long metadata annotation that is beyond the limit provided by Kubernetes. However, `--force-conflicts=true` allows the installation to continue without the warning stopping it. Additionally, `--force-conflicts` only works with `--server-side`.

Once you've entered the command, you should get an output similar to this:

```bash
customresourcedefinition.apiextensions.k8s.io/alertmanagerconfigs.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/alertmanagers.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/podmonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/probes.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheuses.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/prometheusrules.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/servicemonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io/thanosrulers.monitoring.coreos.com created
clusterrolebinding.rbac.authorization.k8s.io/prometheus-operator created
clusterrole.rbac.authorization.k8s.io/prometheus-operator created
deployment.apps/prometheus-operator created
serviceaccount/prometheus-operator created
service/prometheus-operator created
```

When you run `kubectl get deployments`, you can see that the Prometheus Operator is deployed:

```bash
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
prometheus-operator   1/1     1            1           6m1s
```

Next, you'll install role-based access control (RBAC) permissions to allow the Prometheus server to access the Kubernetes API to scrape targets and gain access to the Alertmanager cluster. To achieve this, you'll deploy a ServiceAccount.

Apply the file to your cluster:

```bash
kubectl apply -f redpanda/monitoring/prometheus_rbac.yaml
```

You should get the following response:

```bash
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus created
clusterrolebinding.rbac.authorization.k8s.io/prometheus created
```

Now that you have deployed the Prometheus Operator into your cluster, you're going to create a Prometheus instance using a Prometheus CRD defined in a YAML file.

Then, run the following to apply the instance:

```bash
kubectl apply -f redpanda/monitoring/prometheus_instance.yaml
```

Now, access the server by forwarding a local port to the Prometheus service:

```bash
kubectl port-forward svc/prometheus-operated 9090:9090
```

Visit `localhost:9090` in your browser, and you will see the Prometheus UI.

## Part 2: Deploying Grafana

Next, let’s review how to deploy Grafana in Kubernetes. Grafana allows you to query, visualize, alert on, and understand your metrics no matter where they are stored.

In your terminal, run the following command:

```bash
kubectl create deployment grafana --image=docker.io/grafana/grafana:latest 
```

You can run `kubectl get deployments` to confirm that Grafana has been deployed:

```bash
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
grafana               1/1     1            1           7m27s
```

Next, you’ll create a service for the Grafana deployment:

```bash
kubectl expose deployment grafana --port 3000
```

Forward the port 3000 to the service by running the command below:

```bash
kubectl port-forward svc/grafana 3000:3000
```

Open http://localhost:3000 in your browser to access your Grafana dashboard. Log in with admin as the username and password. This redirects you to a page where you’ll be asked to change your password; afterward, you’ll see the Grafana homepage:

![Grafana overview](https://grafana.com/static/assets/img/blog/prometheus-operator-2.png)

Click Data Sources, then select Prometheus and fill in your configuration details, such as your Prometheus Server URL, access, auth type, and scrape intervals.

You can’t use http://localhost:9090 as your HTTP URL because Grafana won’t have access to it. You must expose Prometheus using a NodePort or LoadBalancer.

Expose Prometheus:

```bash
kubectl apply -f redpanda/monitoring/expose_prometheus.yaml
```

Grafana will be able to pull the metrics from `http://<node_ip>:30900`. To view the `<node_ip>`, run:

```bash
kubectl get nodes -o wide
```

Enter `http://<node_ip>:30900` in the URL box, then click Save & Test:

![Grafana add Prometheus](https://grafana.com/static/assets/img/blog/prometheus-operator-3.png)
