import base64
import paramiko
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name

class OpenDJPlugin(BasePlugin):
	def query(self, **kwargs):
		#variables
		hostName = #host running openDJ
		userName = #user name to ssh with
		userPassword = #password of user
		key = paramiko.RSAKey(data=base64.b64decode(b'AAA...')) #base64 RSA host key for verification
		
		# Find Dynatrace pgi_id from oneAgent monitoring of OpenDJ
		pgi = self.find_single_process_group(pgi_name('<CHANGE TO OpenDJ PROCESSS>'))
		pgi_id = pgi.group_instance_id
		
		
		#connect to host
		client = paramiko.SSHClient()
		client.get_host_keys().add(hostName, 'ssh-rsa', key)
		client.connect(hostName, username=userName, password=userPassword)
		
		#run command to switch to correct directory
		client.exec_command('cd /path/to/ldapsearch')
		
		#run ldapsearch command and pipe all data to stdin, stdout, & stderr
		stdin, stdout, stderr = client.exec_command('./ldapsearch --port 1389 --bindDN "cn=Directory Manager" --bindPassword password --baseDN "cn=Replication,cn=monitor" --searchScope sub "(&(objectClass=*)(domain-name=dc=example,dc=com))" \* + lost-connections received-updates sent-updates replayed-updates pending-updates replayed-updates-ok resolved-modify-conflicts resolved-naming-conflicts unresolved-naming-conflicts missing-changes approximate-delay')
		
		
		#for each line check to see if it contains a wanted variable
		for line in stdout:
			strArray = line.split(:)
			measureValue = strArray[1].strip(' ')
			
			if strArray[0] == "lost-connections": 
				self.results_builder.absolute(key='lost-connections', value=measureValue, entity_id=pgi_id) # send lost-connections measure
				
			elif strArray[0] == "received-updates":
				self.results_builder.absolute(key='received-updates', value=measureValue, entity_id=pgi_id) # send received-updates measure
				
			elif strArray[0] == "sent-updates":
				self.results_builder.absolute(key='sent-updates', value=measureValue, entity_id=pgi_id) # send sent-updates measure
				
			elif strArray[0] == "replayed-updates":
				self.results_builder.absolute(key='replayed-updates', value=measureValue, entity_id=pgi_id) # send replayed-updates measure
				
			elif strArray[0] == "pending-updates":
				self.results_builder.absolute(key='pending-updates', value=measureValue, entity_id=pgi_id) # send pending-updates measure
				
			elif strArray[0] == "replayed-updates-ok":
				self.results_builder.absolute(key='replayed-updates-ok', value=measureValue, entity_id=pgi_id) # send replayed-updates-ok measure
				
			elif strArray[0] == "resolved-modify-conflicts":
				self.results_builder.absolute(key='resolved-modify-conflicts', value=measureValue, entity_id=pgi_id) # send resolved-modify-conflicts measure
				
			elif strArray[0] == "resolved-naming-conflicts":
				self.results_builder.absolute(key='resolved-naming-conflicts', value=measureValue, entity_id=pgi_id) # send resolved-naming-conflicts measure
				
			elif strArray[0] == "unresolved-naming-conflicts":
				self.results_builder.absolute(key='unresolved-naming-conflicts', value=measureValue, entity_id=pgi_id) # send unresolved-naming-conflicts measure
				
			elif strArray[0] == "missing-changes":
				self.results_builder.absolute(key='missing-changes', value=measureValue, entity_id=pgi_id) # send missing-changes measure
				
			elif strArray[0] == "approximate-delay":
				self.results_builder.absolute(key='approximate-delay', value=measureValue, entity_id=pgi_id) # send approximate-delay measure
		
		client.close()

