# OpenDJ-Plugin
OpenDJ Plugin for Dynatrace Saas/Managed

# Purpose
This plugin is to provide metrics on the replication status of an OpenDJ system. 
It uses the paramiko library to ssh to the openDJ host and run the ldapsearch command to pull back metrics.  
		  
# Config For These Done in Dynatrace UI
	1.) Host Name
	2.) User Name
	3.) User Password or Private Key Location 
	4.) Host Key Verification if doing Password Auth
	5.) Path to ldapsearch command  
	6.) ldapPort, bindDN, bindPassword, baseDN, and domain-name 
	
# Metrics Provided 
	lost-connections 
	received-updates
	sent-updates
	replayed-updates
	pending-updates
	replayed-updates-ok
	resolved-modify-conflicts
	resolved-naming-conflicts
	unresolved-naming-conflicts
	missing-changes
	approximate-delay
	
# See this page for a description of the metrics
https://backstage.forgerock.com/knowledge/kb/article/a54492144#monitoring

# Paramiko Documentation
http://docs.paramiko.org
https://github.com/paramiko/paramiko

# For Dynatrace Plugin Information, please see these pages
## For Plugin Python Code questions
https://dynatrace.github.io/plugin-sdk/readme.html

## For Plugin.json questions
https://dynatrace.github.io/plugin-sdk/api/plugin_json_apidoc.html