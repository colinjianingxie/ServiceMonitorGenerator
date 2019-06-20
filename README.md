# ServiceMonitorGenerator
Python script that creates a service monitor YAML file for all the services in custom namespaces automatically.

# Requirements
- Python 3+ installed
- Minikube installed
- Working knowledge of Kubernetes
- Prometheus installed that Autodiscovers namespaces and service monitors

# Basic Setup
You will need to have some services deployed in a custom namespace and have Prometheus installed. Prometheus is a tool that helps scrape metrics. To set up Prometheus and have the services deployed, follow this [github tutorial](https://github.com/colinjianingxie/ServiceMonitoring#kubernetes). You will need to have the prometheus-operator deployed as well as prometheus. 

# How the Service Monitor is formatted
For every service that needs monitoring, there needs to be a **service monitor** uploaded within the namespace of the service.
A sample **ServiceMonitor.yaml** looks like the following:

```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example-service-test
  labels:
    team: whatever
  namespace: test
spec:
  selector:
    matchLabels:
      app: example-service-test
  endpoints:
  - port: web
```

The following tags need to be noted:
- name: (Name of the service monitor)
- namespace: (Namespace where service monitor is deployed in - same as the namespace of the service)
- app: (service name)
- port: (service end point, as listed in the custom service's YAML file)

