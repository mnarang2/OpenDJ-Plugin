import base64
import paramiko
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name

class OpenDJPlugin(BasePlugin):
	def query(self, **kwargs):
		#initialize variables
		hostName = ""
		userName = ""
		userPassword = ""
		pathToKey = ""
		hostKey = ""
		key = ""
		pathToLDAPSearch = ""
		ldapPort = "1389"
		bindDN = "cn=Directory Manager"
		bindPassword = ""
		baseDN = "cn=Replication,cn=monitor"
		domainName = "dc=example,dc=com"
		
		config = kwargs['config']
		#add in variable values from kwargs
		try:
			if 'hostName' in config:
				hostName = config['hostName']
			if 'userName' in config:
				userName = config['userName']
			if 'userPassword' in config:
				userPassword = config['userPassword']
			if 'pathToKey' in config:
				pathToKey = config['pathToKey']
			if 'hostKey' in config:
				hostKey = config['hostKey']
			if 'pathToLDAPSearch' in config:
				pathToLDAPSearch = config['pathToLDAPSearch']
			if 'ldapPort' in config:
				ldapPort = config['ldapPort']
			if bindDN in config:
				bindDN = config['bindDN']
			if bindPassword in config:
				bindPassword = config['bindPassword']
			if baseDN in config: 
				baseDN = config['baseDN']
			if domainName in config:
				domainName = config['domainName']
			print ('--- List of kwargs --')
			for item in config.values():
				print(item)
		except:
			print('There was an error with the parameters.')
		
		# Find Dynatrace pgi_id from oneAgent monitoring of OpenDJ
		pgi = self.find_single_process_group(pgi_name('OpenDJ'))
		pgi_id = pgi.group_instance_id
		
		#these are the metrics the values will be captured for
		key_mapper = ["lost-connections", "received-updates", "sent-updates", "replayed-updates", "pending-updates", "replayed-updates-ok", "resolved-modify-conflicts", "resolved-naming-conflicts", "unresolved-naming-conflicts", "missing-changes", "approximate-delay"]
		
		#connect to host
		client = paramiko.SSHClient()
		try:
			if userName != "" and hostName != "":
				if pathToKey != "":
					#Using private keys to connect to host 
					key = paramiko.RSAKey.from_private_key_file(pathToKey)
					client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					client.connect(hostname = hostName, username = userName, pkey = key)
				elif userPassword != "" and hostKey != "":
					##Using host key verification & password auth to connect
					key = paramiko.RSAKey(data=base64.b64decode(hostKey)) #base64 RSA host key for verification
					client.get_host_keys().add(hostName, 'ssh-rsa', key)
					client.connect(hostName, username=userName, password=userPassword)
			else 
				print ('No User or Host provided - Could not Connect') 
		except:
			print('Generic Could not Connect to Host')
		
		linuxCommand = 'cd ' + pathToLDAPSearch + ' ; ./ldapsearch --port ' + ldapPort + ' --bindDN "' + bindDN + '" --bindPassword ' + bindPassword + ' --baseDN "' + baseDN + '" --searchScope sub "(&(objectClass=*)(domain-name=' + domainName + '))" \* + lost-connections received-updates sent-updates replayed-updates pending-updates replayed-updates-ok resolved-modify-conflicts resolved-naming-conflicts unresolved-naming-conflicts missing-changes approximate-delay'
	
		#first move to correct directory then run ldapsearch command and pipe all data to stdin, stdout, & stderr
		stdin, stdout, stderr = client.exec_command(linuxCommand)
		
		
		#for each line check to see if it contains a wanted variable
		for line in stdout:
			strArray = line.split(:)
			measureValue = strArray[1].strip(' ')
			
			if strArray[0] in key_mapper
				print(strArray[0] + ' : ' + strArray[1])
				self.results_builder.absolute(key=strArray[0], value=measureValue, entity_id=pgi_id) # send measure
		client.close()
		
