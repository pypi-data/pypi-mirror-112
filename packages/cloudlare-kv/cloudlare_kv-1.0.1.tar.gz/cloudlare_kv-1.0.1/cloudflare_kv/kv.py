import requests
import json

class KV:
    def __init__(self, email, access_key, account_id, namespace=None):
        self.email      = email
        self.access_key = access_key
        self.account_id = account_id
        self.namespace  = namespace
        self.base_url   = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}"
        self.headers    = {
                            'X-Auth-Email' : self.email,
                            'X-Auth-Key'   : self.access_key,
                            'Content-Type' : 'application/json'
        }
        
    def set_namespace(self, namespace):
        if(namespace != None):
            self.namespace = namespace
        
    def create_namespace(self, namespace=None):
        """Create Cloudflare KV namespace

        Args:
            namespace (str, optional): Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: Unable to create namespace

        Returns:
            bool: The Namespace created successfully
        """
        self.set_namespace(namespace)
        url = f"{self.base_url}/storage/kv/namespaces"
        payload = json.dumps({
            "title": self.namespace
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Unable to create namespace: {str(response.txt)}")
        
    def get_namespace_id(self, namespace=None):
        """Get the ID of the Namespace

        Args:
            namespace (str, optional): Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: The Namespace is not available in the Cloudflare KV

        Returns:
            str: The Namespace ID
        """
        self.set_namespace(namespace)
        response = [x for x in self.list_namespaces() if x['title'] == self.namespace]
        if(len(response)>0):
            return response[0]['id']
        else:
            raise Exception(f"{self.namespace} namespace is not available in the Cloudflare KV")
        
    def list_namespaces(self):
        """List Namespaces

        Returns:
            list: Cloudflare KV Namespaces
        """
        page = 1
        namespaces = []
        while(page<10):
            url = f"{self.base_url}/storage/kv/namespaces?page={page}&per_page=50"
            payload = {}
            response = json.loads(requests.request("GET", url, headers=self.headers, data=payload).text)
            if(len(response['result'])>0):
                namespaces += response['result']
            else:
                break
            page += 1
        return namespaces
          
    def create_kv_pair(self, key_name, key_value, namespace=None, expiration=None, expiration_ttl=None):
        """Create or Update key-value pair

        Args:
            key_name (str): The key to associate with the value. A key cannot be empty, . or ... 
                            All other keys are valid.
            key_value (str, list): The value to store.
            namespace (str, optional):  Name of the Cloudflare KV Namespace. Defaults to None.
            expiration (str, optional): Set its "expiration", using an absolute time specified 
                                        in a number of seconds since the UNIX epoch. For example, 
                                        if you wanted a key to expire at 12:00AM UTC on April 1, 2019, 
                                        you would set the key’s expiration to 1554076800. 
                                        Defaults to None.
            expiration_ttl (str, optional): The number of seconds for which the key should be visible 
                                            before it expires. At least 60. Defaults to None.
        
        To Note: You can choose one of two ways to specify when a key should expire: 
                 expiration or expiration_ttl

        Raises:
            Exception: Unable to create key-value pair

        Returns:
            bool: The key-value pair creation is successful
        """
        self.set_namespace(namespace)
        id = self.get_namespace_id(self.namespace)
        if expiration or expiration_ttl:
            url = f"{self.base_url}/storage/kv/namespaces/{id}/values/{key_name}?expiration={expiration}&expiration_ttl={expiration_ttl}"
        else:
            url = f"{self.base_url}/storage/kv/namespaces/{id}/values/{key_name}"
        
        if type(key_value) is not str:
            key_value = json.dumps(key_value)
        response = requests.request("PUT", url, headers=self.headers, data=key_value)
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Unable to create key-value pair: {str(response.text)}")
        
    def read_kv_pair(self,  key_name, namespace=None):
        """Read key-value pair

        Args:
            key_name (str): The key to associate with the value. A key cannot be empty, . or ... 
                            All other keys are valid.
            namespace (str, optional):  Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: Unable to get key-value pair

        Returns:
            str: The value of the Key 
        """
        self.set_namespace(namespace)
        id = self.get_namespace_id(self.namespace)
        url = f"{self.base_url}/storage/kv/namespaces/{id}/values/{key_name}"
        response = requests.request("GET", url, headers=self.headers, data={})
        if(response.status_code == 200):
            return response.text
        else:
            raise Exception(f"Unable to get key-value pair: {str(response.txt)}")

    def list_keys(self, prefix,  namespace=None):
        """List Namespace's Keys

        Args:
            prefix (str): A string prefix used to filter down which keys will be returned. 
                          Exact matches and any key names that begin with 
                          the prefix will be returned.
            namespace (str, optional):  Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: Unable to get Namespace's Keys

        Returns:
            list: Namespace's Keys
        """
        self.set_namespace(namespace)
        id =  self.get_namespace_id(self.namespace)
        url = f"{self.base_url}/storage/kv/namespaces/{id}/keys?prefix={prefix}"
        payload={}
        response = requests.request("GET", url, headers=self.headers, data=payload)
        if(response.status_code == 200):
            return json.loads(response.text)['result']
        else:
            raise Exception(f"Unable to get Namespace's Keys: {str(response.txt)}")
        
    def delete_kv_pair(self, key_name, namespace=None):
        """Delete key-value pair

        Args:
            key_name (str): The key to associate with the value. A key cannot be empty, . or ... 
                            All other keys are valid.
            namespace (str, optional):  Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: Unable to delete key-value pair

        Returns:
            bool: The key-value pair deletion is successful
        """
        self.set_namespace(namespace)
        id =  self.get_namespace_id(self.namespace)
        url = f"{self.base_url}/storage/kv/namespaces/{id}/values/{key_name}"
        payload = {}
        response = requests.request("DELETE", url, headers=self.headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Unable to delete key-value pair: {str(response.text)}")

    def delete_namespace(self, namespace=None):
        """Delete a namespace

        Args:
            namespace (str, optional):  Name of the Cloudflare KV Namespace. Defaults to None.

        Raises:
            Exception: Unable to delete KV Namespace

        Returns:
            bool: The namespace deleted successfully
        """
        self.set_namespace(namespace)
        id = self.get_namespace_id(self.namespace)
        url = f"{self.base_url}/storage/kv/namespaces/{id}"
        payload = {}
        response = requests.request("DELETE", url, headers=self.headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Unable to delete KV Namespace: {str(response.text)}")
  