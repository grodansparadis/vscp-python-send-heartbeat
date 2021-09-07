# vscp-python-send-heartbeat

Send VSCP heartbeat to a VSCP daemon (typically in a cron job)

## Usage

```bash
./vscp-python-send-heartbeat.py host user password [guid]
```

| Parameter | Description |
|----------|-------------|
| host     | VSCP daemon hostname or IP address |
| user     | VSCP daemon username |
| password | VSCP daemon password |
| [guid]     | GUID to use for heartbeat (default: none) |

## Example

```bash
./vscp-python-send-heartbeat.py 192.168.1.7 admin secret
```

will send a VSCP node [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) to the VSCP daemon running on 192.168.1.7 using the interface guid.

## Example

```bash
./vscp-python-send-heartbeat.py 192.168.1.7 admin secret FF:FF:FF:FF:FF:FF:FF:FE:2E:8C:03:D5:62:31:00:01
```

will send a VSCP node [heartbeat](https://grodansparadis.github.io/vscp-doc-spec/#/./class1.information?id=type9) to the VSCP daemon running on 192.168.1.7 using guid "FF:FF:FF:FF:FF:FF:FF:FE:2E:8C:03:D5:62:31:00:01".

Typically use in a cron job.

```bash
* * * * * root cd /root;./send_heartbeat.py 192.168.1.7 admin secret FF:FF:FF:FF:FF:FF:FF:FE:B8:27:EB:0A:11:62:00:00
```

----
This file is part of the VSCP project (https://www.vscp.org)
