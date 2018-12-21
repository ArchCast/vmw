# vmw
Codex of my VMware-related CLI utilities written in Python 2.

A collection of quick utilities that allow users to generate reports associated with VMware virtual machines, ESXi hosts, datastores and changing its powered state.


## Utilities:

**vmw-vms-ds-match.py**: Generates a CSV output of all virtual machines that uses any of the datastores the user have defined.

**vmw-host-swapfile.py**: Generates a CSV output of all ESXi hosts and the datastore used by the host's swapfile.

**vmw-vms-poweron.py**:  Generates a list of all virtual machines and its current power state.  Then the user may choose to toggle (on/off) the power state of the VM.



## Getting Started

These instructions will get the vmw utilities up and running:

1.  Prerequisite software installed.  See Prerequisites > Software section.

2.  Login(s) to vCenter host with appropriate privileges.  See Prerequisites > Credential section. 

3.  Minor changes in the code is necessary for *vmw-vms-ds-match.py* and *vmw-host-swapfile.py*.  The changes involves applying names of datastores that is specific to their environment.  Refer to the comments in the code for more details.

4.  [OPTIONAL] vmw utilities can allow the user to automatically log into vCenter with credentials saved on their local machine.  Otherwise, it will prompt the user for login information to the vCenter host.  See Configuration > Config file for more details.



## Prerequisites

**Software**

* [Python 2.7.7 or greater](https://www.python.org/)
* [pyVmomi](https://github.com/vmware/pyvmomi) - VMware vSphere API Python Bindings


**Credential**

* Username and password with appropriate (or adequate) privileges for retrieving information from the vCenter host.  Additionally, using *vmw-vms-poweron.py* requires appropriate privileges to change the virtual machines' power state.  Login(s) with [Administrator Role](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vsphere.security.doc/GUID-93B962A7-93FA-4E96-B68F-AE66D3D6C663.html) will work with vmw.



## Configuration

**Config file**

This is section optional.

If the user wishes vmw utilities to log into vCenter automatically without being prompted for credentials every time, a config file on the user's machine will help achieve this.

By default, the utilities will attempt to read from a config file on the user's local machine in their home directory - if it exists.  If the config file does not exist, it will then proceed to prompt the user to enter in their vCenter host's location and credential.

Note: The information stored in the config file are in plain text.  So use this at your own risk!


1.  In the user home directory, create a file called: *.vcenter-host01*
2.  The first line of this file will contain the location (or IP address) of the vCenter host.
3.  The second line will contain the username for the vCenter host.
4.  The third line will contain the password associated with the username.

Example:

```
cat ~/.vcenter-host01

vcenter1.company.com
Administrator
12341234
```

Again, the information in this config file is stored in plain text.

The default directory and filename for the config file are defined in the variables: *vcenter_conf_path* and *vcenter_conf_file*, respectively in the code.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
