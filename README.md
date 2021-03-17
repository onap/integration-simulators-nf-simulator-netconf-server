# Netconf Server
This server uses sysrepo to simulate network configuration.
It is base od sysrepo-netopeer2 image.

## User guide
### starting server
In order to start server use docker-compose located in root catalog:
```shell
  docker-compose up -d
```
or run image using docker:
```shell
  docker run -it -p 830:830 -p 6513:6513 onap/org.onap.integration.simulators.netconf-server:latest
```

### using server
Server allows:
 - installing custom configuration models on start up.
 - changing configuration of that modules on runtime.

Config can be changed with use of **SSH, be default expose on port 830**
and **TLS, be default exposed on port 6513**.
- SSH works "out of the box" with a username and password *netconf*.
- **TLS is disabled be default**, 
  in order to enable it, set environment variable `ENABLE_TLS=true`.
  More about TLS in ***TLS*** section. 

### custom models
new models are loaded on the image start up from catalog `/resources/models`.
Be default this directory contains `pnf-simulator.yang` model and
default configuration file for config change subscription `models-configuration.ini`.
This file is required for application to start.
More about that file in ***config change subscription*** section.
In order to load custom models on start up,
volume with models and configuration file, should be mounted to `/resources/models` directory.
It can be done in docker-compose, by putting 
`./path/to/cusom/models:/resources/models` in *volumes* section.

### TLS
TLS in disabled be default with environment variable `ENABLE_TLS` set to false.
In order to enable TLS, that environment variable need to be set to `true` 
**on container start up**.
It can be done in docker-compose, 
by putting `ENABLE_TLS=true` in *environment* section.

#### custom certificate
When TLS is enabled server will use auto generated certificates, be default.
That certificates are generated during image build and 
are located in `/resources/certs` directory.
Certificates are loaded during image start up.
**In order to use custom certs**
volume with certificates needs to be mounted to `/resources/certs` directory.
In this volume following files are required, **named accordingly**:
- **ca.crt** - CA/Root certificate
- **client.crt** - client certificate
- **server.crt** - server certificate
- **server.key** - server private key
- **server_pub.key** -  server public key

### config change subscription
Netconf server image run python application on the startup.
More on that application in README located in `src/python` directory.
This application allows subscribing on config change for selected models.
Data about witch models change should be subscribed to, are located in config file.
Config file must be located in models directory, on the image that directory is  `/resources/models`.
For more data about models go back to ***custom models*** section.
Configuration file should be called `models-configuration.ini`, 
although that can be changed, by setting environment variable `MODELS_CONFIGURATION_FILE_NAME`.
Configuration file should be formatted in proper way:
```ini
[SUBSCRIPTION]
models = my-model-1,my-model-2,my-model-3
```
Custom modules, to subscribe to, should be separated with comma.  

### logging
Netconf server print all logs on to the console.
Logs from python application are also stored in file `/logs/netconf_saver.log`

## Development guide 
### building image
In order to build image mvn command can be run:
```shell
  mvn clean install -p docker 
```

### Image building process
To build image, Dockerfile is used.

#### During an image building:
 - catalog `scripts` is copied to image home directory.
   That catalog contains all scripts needed for
   installing initial models and configuring TLS.
 - catalog `models`  is copied to image directory `/resources/models`.
   That catalog contains default models 
   that will be installed on image start up.
 - default certificates and keys for TLS are generated and 
   stored in `/resources/certs` directory.
 - set-up-netopeer script is set to be run on image start up.

#### During an image startup:
 - install all models from `/resources/models` directory
 - if flag `ENABLE_TLS` is set to true, configure TLS 
 - run python netconf server application in detach mode.
 More on that application in README located in `src/python` directory.
    

### change log
This project contains `Changeloge.md` file.
Please update this file when change is made,
according to the guidelines.
