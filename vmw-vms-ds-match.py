#!/usr/bin/env python
#
#  vmw-vms-ds-match.py:
#  Generates CSV output of all ESX virtual machines that uses any datastores in a user-defined list.
#  User must define datastores in: datastore_list
#  Requires: [1]  pyvmomi (https://github.com/vmware/pyvmomi)  [2]  Python 2.7.7 or greater.
#  Optional: [1] User created & defined config file to connect to vCenter. 
#  See: "##  CONFIGURATIONS:" below for configuration options.
#  Last update: 12-20-2018
#  archie@archcast.net || https://github.com/archcast

import pyVmomi, sqlite3, os.path, re, os, sys, requests, atexit, getpass, ssl

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
from os.path import expanduser

##  CONFIGURATIONS:

# Values for vCenter configs
home = expanduser("~")        # Define user home directory.  Works on all OSes.
vcenter_conf_path = home      # Modify this if necessary. 

# Uncomment and update it as needed:
# vcenter_conf_file = '.vcenter-host01'   # [Content]  Line 1: vcenter location.  Line 2:  Username.  Line 3:  Password.

# User-defined list of datastores to match.
# Uncomment below and modify to your specifications:
# datastore_list = ["[datastore_001]", "[datastore_002]", "[datastore_003]", "[datastore_004]"]

# CSV fields
csv_header = 'HOSTNAME,IP ADDRESS,VM LABEL,POWERSTATE'

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

def virtualmachines(virtual_machines):

    # CSV fields
    print csv_header 

    for virtualmachine in virtual_machines:

      row = ()

      summary = virtualmachine.summary
      runtime = virtualmachine.runtime
      config = virtualmachine.config
      hardware = virtualmachine.config.hardware
      devices = virtualmachine.config.hardware.device

      toolsrunning = virtualmachine.summary.guest.toolsRunningStatus

      hostName = virtualmachine.summary.guest.hostName
      ipAddress = virtualmachine.summary.guest.ipAddress

      obj_vm_id = summary.vm
      vm_id = str(summary.vm).strip( "'" )
      vm_numvirtualdisks = summary.config.numVirtualDisks

      obj_vm_host = runtime.host
      vm_host = str(runtime.host).strip("'")

      vm_powerstate = runtime.powerState

      vm_name = config.name
      vm_guestfullname = config.guestFullName
      vm_config = config.files.vmPathName


      '''
      key = 1000:  ParaVirtualSCSIController, SCSI controller 0, etc
      key = 4000:  VirtualVmxnet3, Network adapter 1, VM Network, vim.Network:network-25
      '''

      vm_conf = vm_config.split(' ')[0]
         
      # key range from 2000 to 2999 are hard disks devices.         
      for device in devices:
          if device.key in range(1999, 2999):
              vm_hd_label = device.deviceInfo.label
              vm_hd_size = device.deviceInfo.summary
              vm_hd_ds_name = device.backing.fileName.split(' ')[0]
              vm_hd_ds = device.backing.datastore
              # vm_hd_ds_size = device.capacityInBytes / 1073741824
              vm_hd_ds_size = device.capacityInKB / 1048576

              # Output all VMs hard disk(s) that uses any datastores in the user-defined list: 
              if (vm_hd_ds_name in datastore_list):
                print "%s,%s,%s,%s" % (hostName, ipAddress, vm_name, vm_powerstate)
                break
              else:
                pass


def main(si):

  atexit.register(Disconnect, si)
  content = si.RetrieveContent()

  virtual_machine_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
  virtual_machines = virtual_machine_content.view
  virtual_machine_content.Destroy()
  virtualmachines(virtual_machines)
 

if __name__ == "__main__":

  # The following will fail if Python version is < 2.7.7:
  ssl._create_default_https_context = ssl._create_unverified_context
  requests.packages.urllib3.disable_warnings()

  login = vcenter_to_connect()
  server, username, password = login[0], login[1], login[2]
  si = SmartConnect(host=server, user=username, pwd=password, port=443)

  main(si)
