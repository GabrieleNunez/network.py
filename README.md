network.py
==========

network.py is a handy script that lets you enable/disable/alter/spoof mac address on the network

##Some Examples
=============
##Spoofing
--------------------------------------------
```
> python network.py spoof [mac address here]
> [follow prompts]
> python network.py ["interface name here"] reset
```
--------------------------------------------
##To reset to default mac
```
> python network.py spoof reset
> [follow prompts]
> python network.py ["interface name here"] reset
```
##Example for network interface manipulation
To list available interfaces:
--------------------------------------------
```
> python network.py list
```
--------------------------------------------
To turn off,on,reset interface
--------------------------------------------
```
> python network.py "[interface name here"] [on,off,reset]
```
