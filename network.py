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
import re

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
	#first open a handle to the key in the registry that contains all the adapter information
	handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,REG_ADAPTERS)
	index = 0
	#loop indefinitely until either an OSError occurs which winreg.EnumKey will cause once the value at index isn't available or until we find properties
	#overkill  to check for both but better safe than sorry
	while True:
		try:
			#enumerate over other keys in the system will raise OSError if none are found
			#Store the name of the key that's returned for later use
			keyName = winreg.EnumKey(handle,index)
			if keyName != "Properties":
				try:
					#open a new handle this time it's going to the Key name that we stored
					keyHandle = winreg.OpenKey(handle,keyName)
					query = winreg.QueryValueEx(keyHandle,"DriverDesc")
					#print out the query and use the index but add 1 to it to make it more readable
					#Tossing zero onto a numbered list can confuse people
					print("{0}.\t{1}".format(index + 1,query[0]))
					#close our key handle and then increase index by 1
					winreg.CloseKey(keyHandle)
					index += 1
				except OSError: winreg.CloseKey(handle)
			else : break
		except OSError: break
	#lets get some input and make the magic happen
	choice = input("Select your choice. Use the numbers: ")
	try:
		#parse our choice and decrement it by one because we used numbered list to show the person
		index = int(choice) - 1
		#as long as the command isn't equal to reset we continue on as normal otherwise we gotta do things different
		if mac.lower() != "reset":
			#use regex to trim out popular syntax formatting
			mac = re.sub("[:-]","",mac)
			#make it all upper case. Windows is pretty strict on it
			#then make sure we are strictly at a length of 12 for it. otherwise it is not a "valid" mac address. At least length wise
			mac = mac.upper()
			if len(mac) == 12:
				#same as way above open a handle, this time based on the index supplied by choice
				#if the value is there it will overwrite it otherwise it will create it
				keyName = winreg.EnumKey(handle,index)
				keyHandle = winreg.OpenKey(handle,keyName,access=winreg.KEY_WRITE)
				winreg.SetValueEx(keyHandle,REG_VALUE_NETWORKADDRESS,0,winreg.REG_SZ,mac)
				#and of course close our handle to our key that we modified
				winreg.CloseKey(keyHandle)
				print("Applying Mac Address {0} to device".format(mac))
			else:
				print("Failed to apply")
		else:
			#we must be reseting our mac address
			#this is done by simply deleting the NetworkAddress value in the registry of the keys
			#again we get the correct one through the index which is whatever choice was made - 1 to bring it back to zero-based land
			try:
				keyname = winreg.EnumKey(handle,index)
				keyHandle = winreg.OpenKey(handle,keyname,access=winreg.KEY_WRITE)
				winreg.DeleteValue(keyHandle,REG_VALUE_NETWORKADDRESS)
				winreg.CloseKey(keyHandle)
				print("Mac address reset.Please reset your interface now")
			except FileNotFoundError: print("No spoof  was previously applied")
			except OSError: print("Failed to modify")
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
	#Let's fgure out what command we want to do, and set it to something netsh can use
	cmd = ""
	if op == COMMAND_ON:
		cmd = "enable"
	elif op == COMMAND_OFF:
		cmd = "disable"
	else:
		cmd = ""
	#if we are not using the reset command then we simply do one call
	if op != COMMAND_RESET:
		print("Adjusting Interface: {0}".format(interfaceName))
		TryCall("netsh interface set interface name=\"{0}\" {1}".format(interfaceName,cmd))
	else: 
		#Otherwise to reset we simply call netsh twice. Once to disable and then enable
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
if len(sys.argv) >= 2: #check for a primary command
	if sys.argv[1].lower() == "list":
		ListInterfaces()
	elif sys.argv[1].lower() == "spoof":
		if len(sys.argv) >= 3:
			Spoof(sys.argv[2])
		else: print("No mac address provided. Cannot continue")
	else:
		interface = sys.argv[1]
		if len(sys.argv) >= 3: #make sure we have an argument that follows  our primary command
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