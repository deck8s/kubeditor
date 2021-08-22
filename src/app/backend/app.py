import urllib3
import yaml, json, sys

from pprint import pprint
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class k8s_cluster():

    def __init__(self):
        # Define the bearer token we are going to use to authenticate.
        # See here to create the token:
        # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
        aToken = """eyJhbGciOiJSUzI1NiIsImtpZCI6IllQaGlKYk51UHZhS3hySG5jTlNKV05IU2dQRENkNzBYY1lNektDSTRYeEUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWVkaXRvciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXhkamdwIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI0OTA4MTQ1Zi00ZjkwLTQ1MDEtYjc2YS1iMDMwODZhMmY5ZjEiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1lZGl0b3I6YWRtaW4tdXNlciJ9.JRgZnQt5J94Yo6cM2ajXD41aYBhkueD_nI8DaAQckwvsTHTnNte-gukDasCxHjp0hwGdgWjLAwTIU9Ye7oFx04NLth7-NXKIZygIQbRhMxRfNHRz-iLiMv5fWSnQ_VumON9n_1XhnjqsGB_m7jPOOATKAH80oT04RMRGndxWH1I8GvY_qXDs4Am9qQ1WRLgKuZLKLIcE0C3P8R7VTYAbZYe3dBClr0fLRhlEPvv_nbZayVtMZWrFosWLrE-QopIquQatCa8t6mDUdU6GYmqIX5kySz76gKdOdKYLH_whCrxk2ELB8-BAMaHcHavU0IFu_5wbeiddPdnf3j5JrSBVYQ"""

        # Create a configuration object
        aConfiguration = client.Configuration()

        # Specify the endpoint of your Kube cluster
        aConfiguration.host = "https://172.16.85.134:6443"

        # Security part.
        # In this simple example we are not going to verify the SSL certificate of
        # the remote cluster (for simplicity reason)
        aConfiguration.verify_ssl = False
        # Nevertheless if you want to do it you can with these 2 parameters
        # configuration.verify_ssl=True
        # ssl_ca_cert is the filepath to the file that contains the certificate.
        # configuration.ssl_ca_cert="certificate"

        aConfiguration.api_key = {"authorization": "Bearer " + aToken}

        # Create a ApiClient with our config
        self.aApiClient = client.ApiClient(aConfiguration)

    def list_all_pods(self):
        # Do calls
        v1 = client.CoreV1Api(self.aApiClient)
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" %
                  (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def get_namespaced_object(self, kind, ns, name, pretty=True):
        api_instance = client.AppsV1Api(self.aApiClient)
        func = {
            "deployment": api_instance.read_namespaced_deployment,
            "statefullset": api_instance.read_namespaced_stateful_set,
            # "pod": api_instance.read_namespaced_pod,
            "replicaset": api_instance.read_namespaced_replica_set
        }
        try:
            api_response = func[kind](name, ns, pretty=pretty)
            yaml_response = yaml.dump(api_response.to_dict())
            pprint(yaml_response)
            stream = open('document.yaml', 'w')
            yaml.dump(api_response.to_dict(),stream)
        except ApiException as e:
            print("Exception when calling AppsV1Api->read_namespaced_deployment: %s\n" % e)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    k8s_c = k8s_cluster()

    k8s_c.get_namespaced_object("deployment", "kube-system", "coredns")