# Simple utility to see the top disk users at a given path on collectively multiple hosts

## Prerequisites
* Python3
* pip3
* fabric3

## Install Fabric
```pip3 install -r requiremetns.txt```

## Configure Hostsfile
Add the list of hosts to the hostsfile.txt per line

## Assumptions
It is asumed that there is one user who is capable of logging in to all the
hosts without the need of having passwords (ssh keys) for better utility.

## Usage
```fab --fabfile app.py check_space_on_machines```
