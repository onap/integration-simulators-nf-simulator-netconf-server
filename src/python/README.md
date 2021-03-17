# Netconf Server Python Application
This application is providing core Netconf Server capabilities.
It is started in detached mode on image startup.

Application capabilities:
 - Subscribing on config change per model.
   - Models to subscribe to are loaded from configuration file, 
     provided as application parameter.
   - When configuration of one of models change
     information about change are logged 


## Testing
Tox file with pytest are used fo testing. 

## Logging
Application prints logs on to the console and to file `/logs/netconf_saver.log`
