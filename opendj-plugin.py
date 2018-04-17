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
		
		#these are the metrics the values will be captured for
		key_mapper = ["lost-connections", "received-updates", "sent-updates", "replayed-updates", "pending-updates", "replayed-updates-ok", "resolved-modify-conflicts", "resolved-naming-conflicts", "unresolved-naming-conflicts", "missing-changes", "approximate-delay"]
		
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
			
			if strArray[0] in key_mapper
				self.results_builder.absolute(key=strArray[0], value=measureValue, entity_id=pgi_id) # send measure
		
		client.close()
		
