network.py
==========

*network.py* is a *Python 3.4* handy script that lets you enable/disable/alter/spoof mac address on your computer.  Windows Only

###TODO

* ~~Better code documentation~~
* Easier way to modify interfaces and adapters (Possibly alias them and bind them together?)
* ~~Implement Mac address generator~~

##Some Examples
##Spoofing
--------------------------------------------
```
> python network.py spoof [mac address here]
> [follow prompts]
> python network.py ["interface name here"] reset
```
--------------------------------------------
##To reset to default mac address
--------------------------------------------
```
> python network.py spoof reset
> [follow prompts]
> python network.py ["interface name here"] reset
```
--------------------------------------------
##To list available interfaces:
--------------------------------------------
```
> python network.py list
```
--------------------------------------------
##To turn off,on,reset interface
--------------------------------------------
```
> python network.py "[interface name here"] [on,off,reset]
```
--------------------------------------------
