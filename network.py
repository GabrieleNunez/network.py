#Windows Only Script
#Author: Gabriele M. Nunez (P13Darksight) (http://thecoconutcoder.com)
#Lets you enable/disable/list your network interfaces as well as spoof
#example for spoof
#--------------------------------------------
#> python network.py spoof [mac address here]
#> [follow prompts]
#> python network.py ["interface name here"] reset
#--------------------------------------------
#To reset to default mac
#> python network.py spoof reset
#> [follow prompts]
#> python network.py ["interface name here"] reset
#example for network interface manipulation
#To list available interfaces:
#--------------------------------------------
#> python network.py list
#--------------------------------------------
#To turn off,on,reset interface
#--------------------------------------------
#> python network.py "[interface name here"] [on,off,reset]

import sys
import subprocess
import winreg


#Initialize any variables
#Will use these as constants
COMMAND_OFF = 1
COMMAND_ON = 2
COMMAND_LIST = 3
COMMAND_RESET = 0
REG_ADAPTERS = "SYSTEM\\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
REG_VALUE_NETWORKADDRESS = "NetworkAddress"

interface = "Local Area Connection"

#Spoof(mac) is a function that lets us modify our network card's physical address
#By doing this we can "imitate" other device's on the network
#Many possibilities with spoofing
def Spoof(mac):
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
					index += 1
				except OSError: winreg.CloseKey(handle)
			else : break
		except OSError: break
	choice = input("Select your choice. Use the numbers: ")
	try:
		index = int(choice) - 1
		if mac.lower() != "reset":
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
		else:
			keyname = winreg.EnumKey(handle,index)
			keyHandle = winreg.OpenKey(handle,keyname,access=winreg.KEY_WRITE)
			winreg.DeleteValue(keyHandle,REG_VALUE_NETWORKADDRESS)
			winreg.CloseKey(keyHandle)
			printf("Mac address reset. Reset your interface now")
	except TypeError: 
		print("Bad Choice")
	winreg.CloseKey(handle)

#TryCall(call) is a simple helper function that wraps subprocess.check_call around a try catch statement
#If it fails we simply end it with a print statement saying there was a problem with execution
def TryCall(call):
	try:
		subprocess.check_call(call,shell=True)
	except subprocess.CalledProcessError: print("There was a problem with execution")

#AdjustInterface(interfaceName,op) is a function that lets us work with the network "interface"
#It basically figures out what we want to do and then calls netsh through the shell
def AdjustInterface(interfaceName,op):
	cmd = ""
	if op == COMMAND_ON:
		cmd = "enable"
	elif op == COMMAND_OFF:
		cmd = "disable"
	else:
		cmd = ""
	if op != COMMAND_RESET:
		print("Adjusting Interface: {0}".format(interfaceName))
		TryCall("netsh interface set interface name=\"{0}\" {1}".format(interfaceName,cmd))
	else:
		print("Resetting interface: {0}".format(interfaceName))
		TryCall("netsh interface set interface name=\"{0}\" disable".format(interfaceName))
		TryCall("netsh interface set interface name=\"{0}\" enable".format(interfaceName))

#ListInterfaces() simply takes the shell output from "netsh show interface"
#It tells user's what interfaces are available to work with
#This is what they will pass as a argument to network.py
def ListInterfaces():
	TryCall("netsh interface show interface")

#Begin Script Execution
#Check sys.argv length make sure we have more then 2 arguments being passed
if len(sys.argv) >= 2:
	if sys.argv[1].lower() == "list":
		ListInterfaces()
	elif sys.argv[1].lower() == "spoof":
		if len(sys.argv) >= 3:
			Spoof(sys.argv[2])
		else: print("No mac address provided. Cannot continue")
	else:
		interface = sys.argv[1]
		if len(sys.argv) >= 3:
			if sys.argv[2].lower() == "off":
				AdjustInterface(interface,COMMAND_OFF)
			elif sys.argv[2].lower() == "on":
				AdjustInterface(interface,COMMAND_ON)
			elif sys.argv[2].lower() == "reset":
				AdjustInterface(interface,COMMAND_RESET)
			else: 
				print("Invalid argument")
		else:
			print("No command specified to work on {0} interface".format(interface))
else:
	print("No additional command specified")