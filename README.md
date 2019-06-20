# ServiceMonitorGenerator
Python script that creates a service monitor YAML file for all the services in custom namespaces automatically.

# Requirements
- Python 3+ installed
- Minikube installed
- Working knowledge of Kubernetes
- Prometheus installed that Autodiscovers namespaces and service monitors

# How the Service Monitor is formatted
For every service that needs monitoring, there needs to be a **service monitor** uploaded within the namespace of the service.
A sample service monitor looks like the following:
'''
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
'''
The following tags need to be noted:
1. name: (Name of the service monitor)
2. namespace: (Namespace the service monitor will be deployed in - should be same as the namespace of the service)
3. app: (service name)
4. port: (service end point, as listed in the custom service's YAML file)
