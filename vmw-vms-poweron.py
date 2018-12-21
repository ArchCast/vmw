#!/usr/bin/env python

#  vmw-vms-poweron.py:
#  [1] Output all ESX virtual machines and its Powered state in an enumerated list and
#  [2] allows user to toggle the power state (on/off) from the listed virtual machine(s).
#  Note: Output utilizes ANSI (escape) colors.
#  Requires: [1]  pyvmomi (https://github.com/vmware/pyvmomi)  [2]  Python 2.7.7 or greater.
#  Optional: [1] User created & defined config file to connect to vCenter. 
#  See: "##  CONFIGURATIONS:" below for configuration options.
#  Last update: 12-20-2018
#  archie@archcast.net || https://github.com/archcast

import pyVmomi, requests, atexit, getpass, ssl, os

from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
from ConfigParser import SafeConfigParser

##  CONFIGURATIONS:

# Values for vCenter configs
home = expanduser("~")        # Define user home directory.  Works on all OSes.
vcenter_conf_path = home      # Modify this if necessary. 

# Uncomment and update it as needed:
# vcenter_conf_file = '.vcenter-host01'   # [Content]  Line 1: vcenter location.  Line 2:  Username.  Line 3:  Password.

##  END OF CONFIGURATIONS


def vm_display(vmlist):

  for vm in enumerate(vmlist, start=1):
    (vm_number, vm_id, vm_name, vm_state) = vm[0], vm[1][0], vm[1][1], vm[1][2]

    if vm_state == '[On]':
      print "\033[38;5;118m%10s%3s: %s \033[0m" % (vm_state, vm_number, vm_name)
    else:
      print "%10s%3s: %s" % (vm_state, vm_number, vm_name)

  # User chooses to toggle the powered state of the virtual machines from an enumerated list
  choice = input('\n   \033[38;5;39mToggle #\033[0m ')
  selected = vmlist[(choice - 1)]
  (id_selected, name_selected, state) = selected[0], selected[1], selected[2]

  if state == '[On]':
    print "  \033[38;5;160mPowering off:\033[0m ", name_selected
    task = id_selected.PowerOff()

  if state == '[Off]':
    print "  \033[38;5;118mPowering on:\033[0m ", name_selected
    task = id_selected.PowerOn()


def main(si):

  atexit.register(Disconnect, si)
  content = si.RetrieveContent()

  VirtualMachine_content = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
  virtual_machines = VirtualMachine_content.view
  VirtualMachine_content.Destroy()
  vm_list = []

  for virtualmachine in virtual_machines:

    vm = virtualmachine.summary
    runtime_powerstate = vm.runtime.powerState

    if runtime_powerstate == 'poweredOff': 
      powerstate = '[Off]'
    if runtime_powerstate == 'poweredOn':
      powerstate = '[On]'

    vm_id = (vm.vm, str(vm.config.name), powerstate)
    vm_list.append(vm_id)

  vm_choice = vm_display(vm_list)


if __name__ == "__main__":

  # The following will fail if Python version is < 2.7.7:
  ssl._create_default_https_context = ssl._create_unverified_context
  requests.packages.urllib3.disable_warnings()

  login = vcenter_to_connect()
  server, username, password = login[0], login[1], login[2]
  si = SmartConnect(host=server, user=username, pwd=password, port=443)

  main(si)
