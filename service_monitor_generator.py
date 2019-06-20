import os
import yaml
from kubernetes import client, config


SERVICE_MONITOR_YAML_FILE_NAME = "test.yaml" #Change if needed

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


	
	for ns in kubernetes_client.list_namespace().items:
		temp_namespace = ns.metadata.name
		##################################################################################
		# Describe what string of the namespace you want to monitor,                     #
		# This specific namespace will have the word "test" inside it.                   #
		# We don't want to monitor the default namespaces, such as "kube-system", etc... #
		##################################################################################

		if "test" in temp_namespace:
			for svc in kubernetes_client.list_namespaced_service(temp_namespace).items:
				temp_service_name = svc.metadata.name #Returns the service name
				temp_service_port_type = svc.spec.ports[0].name #Returns the service port type

				#############################################
				# How the Service Monitor YAML is formatted #
				#############################################

				temp_service_monitor_yaml_data = {
					'apiVersion':'monitoring.coreos.com/v1',
					'kind':'ServiceMonitor',
					'metadata':{'name': temp_namespace + "-" + temp_service_name + '-monitor', 'labels':{'team':'whatever'},'namespace':temp_namespace},
					'spec':{'selector':{'matchLabels':{'app':temp_service_name}}, 'endpoints':[{'port':temp_service_port_type}] }
				}
	
				print(svc.metadata.name)
				print(svc.spec.ports[0].name)
				print()
				write(temp_service_monitor_yaml_data)
	print("Finished running program")
main()