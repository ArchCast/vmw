#!/usr/bin/env python
#  
#  vmw-host-swapfile.py:
#  CSV output all ESXi hosts and its swapfile location (as currently configured) 
#  Requires: [1]  pyvmomi.  [2]  Python 2.7.7 or greater.
#  Optional: [1] User created & defined config file to connect to vCenter. 
#  See: "##  CONFIGURATIONS:" below for configuration options.
#  Last update: 12-19-2018
#  archie@archcast.net || https://github.com/archcast

import pyVmomi, sqlite3, os.path, re, os, sys, requests, atexit, getpass, ssl, time

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
from os.path import expanduser

from sys import getsizeof

##  CONFIGURATIONS:

# Values for vCenter configs
home = expanduser("~")        # Define user home directory.  Works on all OSes.
vcenter_conf_path = home      # Modify this if necessary. 

# Uncomment and update it as needed:
# vcenter_conf_file = '.vcenter-host01'   # [Content]  Line 1: vcenter location.  Line 2:  Username.  Line 3:  Password.

# Define CSV output header
csv_header = "ESXi HOST,SWAP FILE LOCATION"
csv_header_timestamp_desc = "CURRENT AS OF: "
csv_header_timestamp_time = time.strftime("%m-%d-%Y") + ' ' + time.strftime("%-H:%M")
csv_header_timestamp = csv_header_timestamp_desc + csv_header_timestamp_time

# Uncomment below and update as needed:
# swapfile_ds_list = ['vm_swap_sata_a', 'vm_swap_sata_2a']

vm_swapfile_dict = {}
datastore_dict = {}
host_swapfile_dict = {}

host_dict = {}

##  END OF CONFIGURATIONS


def vcenter_to_connect():

  vcenter_conf = vcenter_conf_path + '/' + vcenter_conf_file

  if os.path.isfile(vcenter_conf):
    (server, username, password) = (line.rstrip('\n') for line in open(vcenter_conf))
  else:
    # If vCenter host does not exist, then manually input info for vCenter host:
    print "vCenter login file not file.\n"
    server = raw_input("Enter name of vCenter: ")
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ")
  return (server, username, password)

def show_output(ds, esxihost):
  

  print csv_header + ',' + csv_header_timestamp

  for host in hosts:
    host_name = (host.summary.config.name).split('.')[0]    #  output: hostname name only (no FQDN, etc.)
    localSwapDatastore = host.config.localSwapDatastore
    swap_ds = str(localSwapDatastore).strip("'")
    print "%s,%s" % (host_name, datastore_dict[swap_ds])



def main(si):

  atexit.register(Disconnect, si)
  content = si.RetrieveContent()

  # Monkey patch output:
  # print csv_header_timestamp_time
  # #  Datastore
  # datastore_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
  # datastores = datastore_content.view
  # datastore_content.Destroy()

  # for datastore in datastores:
  #   (ds_id, ds_name) = str(datastore.summary.datastore).strip( "'" ), datastore.info.name
  #   datastore_dict.update({ds_id: ds_name})
  # datastore_dict.update({'None': 'None'})    # This is added in or show_hosts() will fail to look up datastore name 'none'
  
  # print csv_header_timestamp_time

  # Virtual Machines
  virtual_machine_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
  virtual_machines = virtual_machine_content.view
  virtual_machine_content.Destroy()

  for virtualmachine in virtual_machines:

    blade = virtualmachine.runtime.host
    # for dsname in virtualmachine.config.datastoreUrl:
    vm_swapfile_dict.update({virtualmachine.config.name: blade})

    print "%s,%s" % (virtualmachine.config.name, blade) 
  # csv_header_timestamp_time
        

  # ESXi host
  host_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
  hosts = host_content.view
  host_content.Destroy()

  for host in hosts:
    host_name = (host.summary.config.name).split('.')[0]    #  output: hostname name only (no FQDN, etc.)
    host_id = host.summary.host
    # host_id = host_id.strip("'")

    print "%s,%s" %(host_name,host_id)
    # host_dict.update({host_id: host_name})

    # swap_ds = str(localSwapDatastore).strip("'")
    # print "%s,%s" % (host_name, host_id)


  # print "%s,%s" % ()
  print "\nvm_swapfile_dict:\n", vm_swapfile_dict
  # print "\ndatastore_dict:\n", datastore_dict
  # print "\nhost_swapfile_dict:\n", host_swapfile_dict

  # show_output(datastore_dict, host_swapfile_dict)
 

if __name__ == "__main__":

  print csv_header_timestamp_time

  # The following will fail if Python version is < 2.7.7:
  ssl._create_default_https_context = ssl._create_unverified_context
  requests.packages.urllib3.disable_warnings()

  login = vcenter_to_connect()
  server, username, password = login[0], login[1], login[2]
  si = SmartConnect(host=server, user=username, pwd=password, port=443)

  main(si)
