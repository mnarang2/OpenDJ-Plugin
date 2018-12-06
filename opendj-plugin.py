import base64
import paramiko
import logging 
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name

class OpenDJPlugin(BasePlugin):
	def query(self, **kwargs):
		#initialize variables
		processName = "org.opends.server.core.DirectoryServer"
		hostName = "localhost"
		userName = "null"
		userPassword = "null"
		pathToKey = ""
		hostKey = "null"
		key = ""
		pathToLDAPSearch = "/opt/opendj/bin"
		ldapPort = "1389"
		bindDN = "cn=Directory Manager"
		bindPassword = ""
		baseDN = "cn=Replication,cn=monitor"
		
		config = kwargs['config']
		#add in variable values from kwargs
		try:
			if processName in config:
				processName = config['processName']
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
			if bindPassword in config:
				bindPassword = config['bindPassword']
			self.logger.info ('--- List of kwargs --')
			for item in config.values():
				self.logger.info(item)
		except:
			self.logger.info('There was an error with the parameters.')
		
		# Find Dynatrace pgi_id from oneAgent monitoring of OpenDJ
		pgi = self.find_single_process_group(pgi_name(processName))
		pgi_id = pgi.group_instance_id
		
		#these are the metrics the values will be captured for
		key_mapper = ["lost-connections", "received-updates", "sent-updates", "replayed-updates", "pending-updates", "replayed-updates-ok", "resolved-modify-conflicts", "resolved-naming-conflicts", "unresolved-naming-conflicts", "missing-changes", "approximate-delay"]
		
		#connect to host
		client = paramiko.SSHClient()
		try:
			if userName != "null" and hostName != "null":
				if pathToKey != "":
					#Using private keys to connect to host 
					key = paramiko.RSAKey.from_private_key_file(pathToKey)
					client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					client.connect(hostname = hostName, username = userName, pkey = key)
				elif userPassword != "null" and hostKey != "null":
					##Using host key verification & password auth to connect
					key = paramiko.RSAKey(data=base64.b64decode(hostKey)) #base64 RSA host key for verification
					client.get_host_keys().add(hostName, 'ssh-rsa', key)
					client.connect(hostName, username=userName, password=userPassword)
			else :
				self.logger.info ('No User or Host provided - Could not Connect') 
		except:
			self.logger.info('Generic Could not Connect to Host')
		
		if ldapPort != "" and bindPassword != "":
			linuxCommand = 'cd ' + pathToLDAPSearch + ' ; ./ldapsearch --port ' + ldapPort + ' --bindDN "' + bindDN + '" --bindPassword ' + bindPassword + ' --baseDN "' + baseDN + '" --searchScope sub "(objectClass=*)" \* + lost-connections received-updates sent-updates replayed-updates pending-updates replayed-updates-ok resolved-modify-conflicts resolved-naming-conflicts unresolved-naming-conflicts missing-changes approximate-delay'
		else :
			self.logger.info('Issue with LDAP Port or Bind Password')
	
		try: 
			#first move to correct directory then run ldapsearch command and pipe all data to stdin, stdout, & stderr
			stdin, stdout, stderr = client.exec_command(linuxCommand)
		except:
			self.logger.info('Issue with running linux ldapsearch command')
		
		#for each line check to see if it contains a wanted variable
		for line in stdout:
			strArray = line.split(":")
			measureValue = strArray[1].strip(' ')
			
			if strArray[0] in key_mapper :
				self.logger.info(strArray[0] + ' : ' + strArray[1])
				self.results_builder.absolute(key=strArray[0], value=measureValue, entity_id=pgi_id) # send measure
		client.close()
		
