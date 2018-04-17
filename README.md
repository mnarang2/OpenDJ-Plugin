# OpenDJ-Plugin
OpenDJ Plugin for Dynatrace Saas/Managed

# Purpose
This plugin is to provide metrics on the replication status of an OpenDJ system. 
It uses the paramiko library to ssh to the openDJ host and run the ldapsearch command to pull back metrics.  
		  
# Needed Changes in opendj-plugin.py
	1.) Change hostName variable
	2.) Change hostUserName variable
	3.) Change userPassword variable 
	4.) Replace base64 version of the host key for verification purposes
	5.) For pgi_id change the Process Name to OpenDJ Process
	6.) Change path of "cd" linux command to correct location for ldapsearch 
	
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