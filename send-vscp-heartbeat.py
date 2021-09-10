#!/usr/bin/python
"""
// File: send_vscp_heartbeat.py
//
// Usage: send_vscpt_heartbeat.py broker port user password topic
//
// Described here https://github.com/grodansparadis/vscp-python-send-heartbeat
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version
// 2 of the License, or (at your option) any later version.
//
// This file is part of the VSCP (http://www.vscp.org)
//
// Copyright (C) 2000-2021
// Ake Hedman, Grodans Paradis AB, <akhe@grodansparadis.com>
//
// This file is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this file see the file COPYING.  If not, write to
// the Free Software Foundation, 59 Temple Place - Suite 330,
// Boston, MA 02111-1307, USA.
//
"""
# https://pythontic.com/fileformats/netrc/introduction
# https://everything.curl.dev/usingcurl/netrc
import netrc
import configparser
import getopt
import json
import math
import sys
import time
from ctypes import c_byte, c_short, c_ubyte

import getpass
import telnetlib
import vscp
import vscp_class as vc
import vscp_type as vt

# ----------------------------------------------------------------------------
#                              C O N F I G U R E
# ----------------------------------------------------------------------------

# Print some info along the way
bVerbose = False

# Set to true to use .netrc for credentials
bNetrc = False

# Print debug info if true
bDebug = False

# GUID to use for heartbeat event
# If empty (or all null) MAC address will be used to construct GUID
guid = "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"

# VSCP daemon
host = "127.0.0.1"

# VSCP daemon port
port = 1883

# Username to login at server
user = "admin"

# Password to login at server
password = "secret"

# Optional byte 0
byte0 = 0

# Zone for module
zone = 0

# Subzone for module
subzone = 0

# Configuration will be read from path set here
cfgpath = ""

# ----------------------------------------------------------------------------------------

netrc = netrc.netrc()
config = configparser.ConfigParser()

def usage():
    print("usage: send_mqtt_heartbeat.py -v -c <pat-to-config-file> -h ")
    print("------------------------------------------------------------")
    print("-h/--help      - This text.")
    print("-v/--verbose   - Print output also to screen.")
    print("-c/--config    - Path to configuration file.")
    print("-b/--server    - Server to connect to.")
    print("-p/--port      - Port on broker to connect to.")
    print("-u/--user      - Username to use as credentials.")
    print("-P/--password  - Password to use as credentials.")
    print("-g/--guid      - GUID to use for event.")
    print("-t/--topic     - Topic to publish heartbeat on.")
    print("-0/--byte0     - Set optional byte 0.")
    print("-z/--zone      - Set zone.")
    print("-s/--subzone    - Set subzone.")

# ----------------------------------------------------------------------------

args = sys.argv[1:]
nargs = len(args)

try:
  opts, args = getopt.getopt(args, 
                        "hvc:b:p:u:P:0:z:s:n", 
                        ["help", 
                          "verbose", 
                          "config=",
                          "host=",
                          "port=",
                          "user=",
                          "password=",
                          "byte0=",
                          "zone=",
                          "subzone=",
                          "netrc",
                          ])
except getopt.GetoptError:
  print("unrecognized format!")
  usage()
  sys.exit(2)

for opt, arg in opts:
  if opt in ("-h", "--help"):
    print("HELP")
    usage()
    sys.exit()
  elif opt in ("-v", "--verbose"):
    bVerbose = True
  elif opt in ("-n", "--netrc"):
    bNetrc = True  
  elif opt in ("-c", "--config"):
    cfgpath = arg
    if bVerbose:
      print("cfgpath=", cfgpath)
  elif opt in ("-b", "--host"):
    host = arg
    if bVerbose:
      print("host=", host)
  elif opt in ("-p", "--port"):
    port = arg
    if bVerbose:
      print("port=", port)
  elif opt in ("-u", "--user"):
    user = arg
    if bVerbose:
      print("user=", user)
  elif opt in ("-P", "--password"):
    password = arg  
    if bVerbose:
      print("password=", password)
  elif opt in ("-0", "--byte0"):
    byte0 = int(arg) & 0xff
    if bVerbose:
      print("byte0=", byte0)    
  elif opt in ("-z", "--zone"):
    zone = int(arg) & 0xff
    if bVerbose:
      print("zone=", zone)    
  elif opt in ("-s", "--subzone"):
    subzone = int(arg) & 0xff
    if bVerbose:
      print("subzone=", subzone)

if (len(cfgpath)):

  init = config.read(cfgpath)

  if bVerbose:
    print("Reading configuration from=", cfgpath)

  # ----------------- GENERAL -----------------

  if 'bVerbose' in config['GENERAL']:
	  bVerbose = config.getboolean('GENERAL', 'bVerbose')
	  if bVerbose:
	    print('Verbose mode enabled.')

  
  if 'netrc' in config['GENERAL']:
	  bNetrc = config.getboolean('GENERAL', 'netrc')
	  if bVerbose:
	    print('Will use .netrc for credentials.')

  if 'guid' in config['GENERAL']:
	  guid = config['GENERAL']['guid']
	  if bVerbose:
	    print("guid =", guid)

  if 'byte0' in config['GENERAL']:
	  byte0 = int(config['GENERAL']['byte0'])
	  if bVerbose:
	    print("zone =", zone)

  if 'zone' in config['GENERAL']:
	  zone = int(config['GENERAL']['zone'])
	  if bVerbose:
	    print("zone =", zone)

  if 'subzone' in config['GENERAL']:
	  subzone = int(config['GENERAL']['subzone'])
	  if bVerbose:
	    print("subzone =", subzone)

# ----------------- VSCP -----------------

  if 'host' in config['VSCP']: 
	  host = config['VSCP']['host']
	  if bVerbose:
	    print("host =", host)

  if 'port' in config['VSCP']:
	  port = int(config['VSCP']['port'])
	  if bVerbose:
	    print("port =", port)

  if 'user' in config['VSCP']:
	  user = config['VSCP']['user']
	  if bVerbose:
	    print("user =", user)

  if 'password' in config['VSCP']:
	  password = config['VSCP']['password']
	  if bVerbose:
	    print("password =", "***********")
	    # print("password =", password)

# -----------------------------------------------------------------------------

# Initialize VSCP event content
def initEvent(ex,byte0,vscpClass,vscpType):
  # Dumb node, priority normal
  ex.head = vscp.VSCP_PRIORITY_NORMAL | vscp.VSCP_HEADER16_DUMB
  g = vscp.guid()
  if (("" != guid) and ("00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00" != guid)):
    g.setFromString(guid)
  else:
    g.setGUIDFromMAC(byte0)
    ex.guid = g.guid
  ex.vscpclass = vscpClass
  ex.vscptype = vscpType
  ex.data[0] = byte0 & 0xff
  return g
  
# -----------------------------------------------------------------------------


if bNetrc :
  if bVerbose:
    print(".netrc machine = ", host)
  authTokens = netrc.authenticators(host)
  user = authTokens[0]
  password = authTokens[2]
  if bVerbose :
    print("-------------------------------------------------------------------------------")
    print("Credentials")
    print("Remote Host Name: '%s'" % (host))
    print("User Name at remote host: '%s'" % (authTokens[0]))
    print("Account Password: '%s'"  % (authTokens[1]))
    print("Password for the user name at remote host: '%s'" % (authTokens[2]))

if bVerbose :
  print("\n\nConnection in progress...", host, port)

# Connect to VSCP daemon
tn = telnetlib.Telnet(host, 9598)
tn.read_until(b"+OK",2)

# Login
tn.write(b"user " + user.encode('utf8') +  b"\n")
tn.read_until(b"+OK", 2)

tn.write(b"pass " + password.encode('utf8') + b"\n")
tn.read_until(b"+OK - Success.", 2)

# -----------------------------------------------------------------------------
#                             H E A R T B E A T
# -----------------------------------------------------------------------------

ex = vscp.vscpEventEx()
g = initEvent(ex, byte0, vc.VSCP_CLASS1_INFORMATION, vt.VSCP_TYPE_INFORMATION_NODE_HEARTBEAT)

# Size is predata + string length + terminating zero
ex.sizedata = 3
ex.data[0] = byte0
ex.data[1] = zone
ex.data[2] = subzone

# Send event to server
tn.write(b"send " +  ex.toString().encode('utf8') + b"\n") 
tn.read_until(b"+OK - Success.", 2)

if bVerbose:
  print("Sent Event=",ex.toString())

tn.write(b"quit\n")

# -----------------------------------------------------------------------------


if bVerbose :
    print("-------------------------------------------------------------------------------")
    print("Closed")

# -----------------------------------------------------------------------------


