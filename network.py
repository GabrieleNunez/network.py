#Windows Only Script
#Author: Gabriele M. Nunez (P13Darksight) (http://thecoconutcoder.com
#Lets you enable/disable/list your network interfaces as well as spoof
#TODO mac address spoofing

import sys
import subprocess
import winreg

COMMAND_OFF = 1
COMMAND_ON = 2
COMMAND_LIST = 3
ADAPTER_REGISTRY_LOCATION = "SYSTEM\\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

interface = "Local Area Connection"

#not done yet, don't use, still implementing
def spoof(mac):
	handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,ADAPTER_REGISTRY_LOCATION)
	index = 0
	while True:
		try:
			keyName = winreg.EnumKey(handle,index)
			index++
		except winreg.WindowsError: break
	winreg.CloseKey(handle)
def TryCall(call):
	try:
		subprocess.check_call(call,shell=True)
	except subprocess.CalledProcessError: print("There was a problem with execution")
	
def AdjustInterface(interfaceName,op):
	cmd = ""
	if op == COMMAND_ON:
		cmd = "enable"
	elif op == COMMAND_OFF:
		cmd = "disable"
	else:
		cmd = ""
	print("Adjusting Interface: {0}".format(interfaceName))
	TryCall("netsh interface set interface name=\"{0}\" {1}".format(interfaceName,cmd))
	
def ListInterfaces():
	TryCall("netsh interface show interface")
	
if len(sys.argv) >= 2:
	if sys.argv[1].lower() == "list":
		ListInterfaces()
		sys.exit()
	else:
		interface = sys.argv[1]
else:
	print("No interface specified")
	sys.exit()
if len(sys.argv) >= 3:
	if sys.argv[2].lower() == "off":
		AdjustInterface(interface,COMMAND_OFF)
	elif sys.argv[2].lower() == "on":
		AdjustInterface(interface,COMMAND_ON)
	else: 
		print("Invalid argument")
else:
	print("No command specified to work on {0} interface".format(interface))