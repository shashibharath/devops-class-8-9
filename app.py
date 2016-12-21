''' Importing fabric to execute commands and collect
information of the execution into python objects for
further evaluation Also import regular expressions'''

from fabric.api import *
import re

''' Defining the my_hosts variable reading from the 
separate hosts file. This is used as a decorator to
run the tasks. Now the decorator @hosts(my_hosts) 
can be specified to execute the task on those hosts '''


with open('hostsfile.txt')as f:
    my_hosts = f.read().splitlines()


''' Task to get the disk utilization on any host,
per user and collect them into a computable object
and utilize the object later for sorting and other
use cases.''' 

def space_per_user():
    result = run('''find /local -type f -printf '%u %k\n' | awk '{ \ 
                                        arr[$1] += $2 \ 
                                    } END { \ 
                                        for ( i in arr ) { \ 
                                            print i": "arr[i] \
                                        } \
                                    }' \
                                    ''')
    result = result.splitlines()
    return result
 
''' Applying the task decorator and performing the space_per_user
 method on the list of hosts from the text file. The output is given
as a dict of hosts as keys and values being a list of users and their
disk space utilisation in a tricky format. We are creating a new dict
 by of users with their disk utilisation summed up from all the hosts
and then we are sorting them in the reverse order with the sorted method
of python and then using lambda function to generate readable output
of users and their corresponding total utilisation indexing only 10
items of all ''' 


@task
def check_space_on_machines():
    with settings(
       hide('running', 'warnings', 'stdout', 'stderr'),
       warn_only = True
    ):
       result = execute(space_per_user, hosts=my_hosts)
       users = {}
       for i in result:
           for j in result[i]:
               name, val = j.split(':')
               users[name] = users.get(name, 0) + int(re.findall('\d+', val)[0])
       sort_users = sorted(users.items(), key=lambda x: x[1], reverse=True)[:10]
       print("The top ten users with their disk utilisation summed up in all the hosts is\n %s" % sort_users)
