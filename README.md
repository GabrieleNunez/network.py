network.py
==========

*network.py* is a handy script that lets you enable/disable/alter/spoof mac address on your computer. 
It does use windows code so it is windows only. SORRY! It was written in *Python 3.4*

And it has been tested on Windows 8. If it works on anything else let me know! Or if any issues then well mark them up!

###TODO

* Better code documentation
* Easier way to modify interfaces and adapters (Possibly alias them and bind them together?)

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
