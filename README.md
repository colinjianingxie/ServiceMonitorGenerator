# Service Monitor YAML Generator
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

# Service Monitor Python Code Explanation (Code at bottom)

# Service Monitor Python Code

```python
import os
import yaml
from kubernetes import client, config

# Change if needed
SERVICE_MONITOR_YAML_FILE_NAME = "test.yaml"


########################################
# WRITING TO THE YAML FILE/UPDATING IT #
########################################
def write(new_yaml_data_dict):
  with open(SERVICE_MONITOR_YAML_FILE_NAME, "a") as fo:
    fo.write("---\n")
  sdump = yaml.dump(new_yaml_data_dict,indent=0)
  with open(SERVICE_MONITOR_YAML_FILE_NAME, "a") as fo:
    fo.write(sdump)
    
##############################################
# MAIN FUNCTION, WHERE WE GENERATE YAML FILE #
##############################################

def main():
	#################################################
	# DELETE THE YAML FILE (SO WE CAN OVERWRITE IT) #
	#################################################
	if os.path.exists(SERVICE_MONITOR_YAML_FILE_NAME):
		os.remove(SERVICE_MONITOR_YAML_FILE_NAME)

	##########################
	# CONNECTING TO MINIKUBE #
	##########################
	kube_config = os.getenv('KUBE_CONFIG')
	context = os.getenv('CONTEXT')

	proxy_url = os.getenv('HTTP_PROXY', None)
	config.load_kube_config(config_file=kube_config,
	                        context=context)
	if proxy_url:
	    logging.warning("Setting proxy: {}".format(proxy_url))
	    client.Configuration._default.proxy = proxy_url
  
	##########################
	# ACCESSING Minikube API #
	##########################
	kubernetes_client = client.CoreV1Api()
	v1 = client.CoreV1Api()

	###########################
	# GETTING THE NAMESPACES  #
	###########################
	for ns in kubernetes_client.list_namespace().items:
		temp_namespace = ns.metadata.name # Getting each specific namespace
    
    ##################################################################################
    # Describe what string of the namespace you want to monitor,                     #
    # This specific namespace will have the word "test" inside it.                   #
    # We don't want to monitor the default namespaces, such as "kube-system", etc... #
    ##################################################################################
		if "test" in temp_namespace:
			for svc in kubernetes_client.list_namespaced_service(temp_namespace).items:
				temp_service_name = svc.metadata.name # Returns the service name
				temp_service_port_type = svc.spec.ports[0].name # Returns the service port type
				
        #############################################
        # How the Service Monitor YAML is formatted #
        #############################################
				temp_service_monitor_yaml_data = {
					'apiVersion':'monitoring.coreos.com/v1',
					'kind':'ServiceMonitor',
					'metadata':{'name': temp_namespace + "-" + temp_service_name + '-monitor', 'labels':{'team':'whatever'},'namespace':temp_namespace},
					'spec':{'selector':{'matchLabels':{'app':temp_service_name}}, 'endpoints':[{'port':temp_service_port_type}] }
				}
	    
				print(svc.metadata.name) # Prints the service name
				print(svc.spec.ports[0].name) # Prints the service endpoint port
				print()
        
				write(temp_service_monitor_yaml_data) # Write to the YAML file
	print("Finished running program")
main()
```


