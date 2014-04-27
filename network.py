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
REG_ADAPTERS = "SYSTEM\\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
REG_VALUE_NETWORKADDRESS = "NetworkAddress"
interface = "Local Area Connection"

def spoof(mac):
	handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,REG_ADAPTERS)
	index = 0
	while True:
		try:
			keyName = winreg.EnumKey(handle,index)
			if keyName != "Properties":
				try:
					keyHandle = winreg.OpenKey(handle,keyName)
					query = winreg.QueryValueEx(keyHandle,"DriverDesc")
					print("{0}.\t{1}".format(index + 1,query[0]))
					winreg.CloseKey(keyHandle)
					index = index + 1
				except OSError: winreg.CloseKey(handle)
			else : break
		except OSError: break
	choice = input("Select your choice. Use the numbers: ")
	try:
		index = int(choice) - 1
		mac = mac.replace(":","")
		mac = mac.replace("-","")
		mac = mac.upper()
		if len(mac) == 12:
			keyName = winreg.EnumKey(handle,index)
			keyHandle = winreg.OpenKey(handle,keyName,access=winreg.KEY_WRITE)
			winreg.SetValueEx(keyHandle,REG_VALUE_NETWORKADDRESS,0,winreg.REG_SZ,mac)
			winreg.CloseKey(keyHandle)
			print("Applying Mac Address {0} to device".format(mac))
		else:
			print("Failed to apply")
	except TypeError: 
		print("Bad Choice")
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
	elif sys.argv[1].lower() == "spoof":
		if len(sys.argv) >= 3:
			spoof(sys.argv[2])
		else: print("No mac address provided. Cannot continue")
	else:
		interface = sys.argv[1]
		if len(sys.argv) >= 3:
			if sys.argv[2].lower() == "off":
				AdjustInterface(interface,COMMAND_OFF)
			elif sys.argv[2].lower() == "on":
				AdjustInterface(interface,COMMAND_ON)
			else: 
				print("Invalid argument")
		else:
			print("No command specified to work on {0} interface".format(interface))
else:
	print("No additional command specified")