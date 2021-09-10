# send-mqtt-heartbeat and send-vscp-heartbeat

Two scripts that help to send VSCP heartbeats from remote machines. One version is for sending VSCP heartbeats over MQTT and the other for sending VSCP heartbeats over the tcp/ip link protocol.

## Installation

You can either download the scripts from this repository (https://github.com/grodansparadis/vscp-python-send-heartbeat) or install them from the package manager. If you download from the repository you need to install the dependencies yourself.

The far easiest eay is to install with **pip** (https://pypi.org/project/vscp-python-send-heartbeat/1.0.0/).  The only thing needed to install the python package is the following:

```
pip3 install vscp-python-send-heartbeat
```

best is to install in a virtual environment. Use the following command to create a virtual environment:

```
mkdir project-name && cd project-name
python3 -m venv .env
source .env/bin/activate
```

the do the install of the package as described above.

After install you can use bot scripts, _send-vscp-heartbeat.py_ and _send-mqtt-heartbeat.py_, from the command line. Info on how to configure the scripts for your needs are below.


## send-mqtt-heartbeat
Send VSCP heartbeat to a MQTT broker (typically used in a cron job)

### Usage

```bash
./send-mqtt-heartbeat.py --broker=host -n --topic="/vscp" [--guid=""]
```
This will send a json formatted [heartbeat event](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) to the selected MQTT broker. You can set zone and subzone and also data byte zero content.

If a guid is not specified a GUID will be constructed from the machines MAC address. See [the specification](https://grodansparadis.github.io/vscp-doc-spec/#/./vscp_globally_unique_identifiers?id=predefined-vscp-guid39s) for more information on this.

The default topic is _"vscp/{xguid}/{xclass}/{xtype}"_ where {xguid} is replaced with the actual GUID and {xclass} is replaced with the VSCP class and {xtype} is replaced with the actual VSCP type.

The **-n** says that username and password should be fetched from the _.netrc_ file. See [Use .netrc](#use-.netrc) below. 


| Short parameter  | Long parameter  | Description |
| :--------------: | :-------------: | ----------- |
| -h | --help      |  Show help text |
| -v | --verbose   | Print output also to screen. |
| -c | --config    | Path to configuration file (--config="_some path_"). |
| -b | --broker    | Broker to connect to (--broker="_demo.vscp.org_"). |
| -p | --port      | Port on broker to connect to (--port=1883). |
| -u | --user      | Username to use as credentials (--user=_admin_). |
| -P | --password  | Password to use as credentials (--password=_secret_). |
| -g | --guid      | GUID to use for event (--guid=_FF:FF:FF:FF:FF:FF:FF:FE:60:A4:4C:E7:76:5A:00:00_). |
| -t | --topic     | Topic to publish heartbeat on (-topic=_the_fabulous_topic_). |
| -0 | --byte0     | Set optional byte 0 (--byte0=11). |
| -z | --zone      | Set zone (--zone=22). |
| -s | --subzone   | Set subzone (--subzone=33). |

### Example

```bash
./send-mqtt-heartbeat.py --broker=test.mosquitto.org -n -v -t="/vscp/FF:FF:FF:FF:FF:FF:FF:FE:60:A4:4C:E7:76:5A:00:00/20/9"
```

will send a VSCP [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) event to the MQTT mosquitto test broker using the specified topic.

### Example

```bash
./send-mqtt-heartbeat.py -v -c"./config.ini"
```

will send a VSCP [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) event to the broker specified in the configuration file.

Typically used in a cron job.

```bash
* * * * * root cd /root;./send_mqtt heartbeat.py -n
```

## send-vscp-heartbeat
Send VSCP heartbeat to a VSCP daemon or send (typically used in a cron job)

### Usage

```bash
./send-vscp-heartbeat.py --server=host -n [--guid=""]
```
This will send a [heartbeat event](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) to the selected VSCP sever. You can set zone and subzone and also data byte zero content.

If a guid is not specified a GUID will be constructed from the machines MAC address. See [the specification](https://grodansparadis.github.io/vscp-doc-spec/#/./vscp_globally_unique_identifiers?id=predefined-vscp-guid39s) for more information on this.

The **-n** says that username and password should be fetched from the _.netrc_ file. See [Use .netrc](#use-.netrc) below. 


| Short parameter  | Long parameter  | Description |
| :--------------: | :-------------: | ----------- |
| -h | --help      |  Show help text |
| -v | --verbose   | Print output also to screen. |
| -c | --config    | Path to configuration file (--config="_some path_"). |
| -b | --server    | Server to connect to (--server="_demo.vscp.org_"). |
| -p | --port      | Port on broker to connect to (--port=1883). |
| -u | --user      | Username to use as credentials (--user=_admin_). |
| -P | --password  | Password to use as credentials (--password=_secret_). |
| -g | --guid      | GUID to use for event (--guid=_FF:FF:FF:FF:FF:FF:FF:FE:60:A4:4C:E7:76:5A:00:00_). |
| -0 | --byte0     | Set optional byte 0 (--byte0=11). |
| -z | --zone      | Set zone (--zone=22). |
| -s | --subzone   | Set subzone (--subzone=33). |

### Example

```bash
./send-vscp-heartbeat.py --broker=test.mosquitto.org -n -v -t="/vscp/FF:FF:FF:FF:FF:FF:FF:FE:60:A4:4C:E7:76:5A:00:00/20/9"
```

will send a VSCP [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) event to the MQTT mosquitto test broker using the specified topic.

### Example

```bash
./send-vscp-heartbeat.py -v -c"./config.ini"
```

will send a VSCP [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) event to the host specified in the configuration file. 

Typically used in a cron job.

## Use .netrc

The switch **-n** or **--netrc** says that username and password should be fetched from the _.netrc_ file in the executing user's home directory. This file should only be readable by the owner no one else. The format is

```
machine host1 
login user1 
password pass1

machine host2 
login user2 
password pass2
```

which also can be written as

```
machine host1 login user1 password pass1
machine host2 login user2 password pass2
```

The command line argument

´´´
--broker=host

or

--server=host
´´´

select the entry (can also be given as _-bhost_).

This is the secure way to use the script not exposing any credentials. Another alternative is to store this information in the configuration file and set proper access rights for this file. The insecure way is to enter the credentials on the command line which even if supported is not secure.


## Configuration file format

A typical configuration file have the following content. The content should be selfexlpratory.

```
# Configuration file example for send_mqtt_heartbeat.py and send_vscp_heartbeat.py

[GENERAL]

# Show info when the script is eceuted
bVerbose = True

# GUID to use for heartbeat event
# If empty MAC address will be used to construct GUID
guid=

# Optional byte zero to use for heartbeat event
byte0=0

# Zone to use for heartbeat event
zone=80

# Subzone to use for heartbeat event
subzone=0

[VSCP]

# The VSCP daemon to connect to.
# If .netrc is used this should be the machine name.
host = vscp

# (comment out if using .netrc)
user = vscp

# (comment out if using .netrc)
password = secret

[MQTT]
# MQTT host address
host=mqtt

# MQTT host port
port=1883

# MQTT username (comment out if using .netrc)
user=vscp

# MQTT password (comment out if using .netrc)
password=secret

# Topics for VSCP JSON event publishing
topic_temperature=vscp/{xguid}/{xclass}/{xtype}

```

----
This file is part of the VSCP project (https://www.vscp.org)
