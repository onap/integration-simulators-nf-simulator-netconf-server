# Netconf Server Python Applications
This Python project contains two entry points for two applications. 
These applications are providing core Netconf Server capabilities.
They are both started in detached mode on image startup.

Applications:
- netconf_change_listener
- netconf_rest

This approach was selected due to problem with opening two connections to sysrepo in one process.
Moreover, both applications are independent, they use sysrepo to communicate.

*netconf_rest -> sysrepo -> netconf_change_listener -> kafka*

Common parts for both entry points is located in python package netconf-server.


## Netconf change listener
Change listener is subscribing on sysrepo model configuration change.
Then it connects to *Kafka* message queue as a *KafkaProducer*.
In order to connect to *Kafka* application parameters are used. 

**Application capabilities:**
- Subscribing on config change per model.
    - Models to subscribe to are loaded from configuration file,
      provided as application parameter.
    - When configuration of one of models change
      information about change are logged and send to *Kafka*


## Netconf rest
Creates endpoints that can be used to communicate with sysrepo.   
Then it connects to *Kafka* message queue as a *KafkaConsumer*.
In order to connect to *Kafka* application parameters are used.

Available endpoints:
- *GET* `/healthcheck` returns 200 "UP" if server is up and running
- *POST* `/readiness` return 200 "Ready" if server is ready, if not, returns 503 "Not Ready"
  - readiness check is trying to connect with *Kafka* as a consumer,
    if this connection fails application is returning "Not Ready".
- *POST* `/change_config/<path:module_name>` changes configuration ad returns 202 "Accepted"
  - performs configuration change for given module (module_name) using sysrepo-python library.
- *GET* `/get_config/<path:module_name>` returns 200 and current configuration
  - performs get configuration for given module (module_name) using sysrepo-python library.
- *GET* `/change_history` returns 200 and change history as json
  - Connects to *Kafka* as a consumer and pulls all changes, then returns them in json form. 


## Testing
Tox file with pytest are used fo testing. 


## Logging
Applications print logs on to the console and to files located in `/logs` directory
