---
title: Network Connectivity through Wireless interface for Debian
abstract: test
keywords: proxmox, WiFi usb adapter
categories: IT
weblogName: arrays.stream
postDate: 2020-04-17T00:22:23.6197990-04:00
---

# Network Connectivity through Wireless interface for Debian

##### Problem
I have a couple of Proxmox servers which I use to host Kubernetes nodes. I keep them at the basement because I do not want to deal with the noise. But there are no wired connections available. 

##### Rules
I am not buying an extender and be done with it. 

##### Solution 
###### Attempt #1
I have a TP-Link Dual Band WiFi router lying around. It does have WDS feature and can act as a repeater. :bulb: Idea !

Jumped across the room and appreciated myself. Then went ahead and did the following steps.

* Disabled DHCP - IP assignment will be handled by the main router.
* Changed the IP address from 192.168.0.1 to something else. - It is no longer the gateway.
* Enabled WDS bridging
* Surveyed the WiFi AP I want to access and gave credentials.
* Changed the Channel to the same channel as original network is at. 
* Disabled SSID broadcast - Not necessary. 
* Reboot

Plugged in patch cables from both servers and turned on. Well, I now have internet for those machines.

Days went by and I was happy. Suddenly one day the router started dropping connections and I am no longer happy. Sometimes my machines were not reachable for days. It used to recover by itself in a couple hours or immediately with a reboot.

It happened again and this time even multiple reboots did not work. So I moved on to next attempt.

###### Attempt #2
I purchased two types of WiFi USB adapters. One rated at 1200 MBPS and other one at 600 MBPS. Not great but will work fine for my use case.

Chinese made, and have great reviews right off of Amazon. Problem is there are no drivers available for this. Actually there is no information on what chip set is used. Included drivers work fine for Windows. I'm not sure if MacOS drivers works the same but, I believe it does. 

Connected the USB devices one by one and did  *lsusb* which outputs this:
```bash
Bus 001 Device 002: ID 0bda:0811 Realtek Semiconductor Corp.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 002 Device 002: ID 0627:0001 Adomax Technology Co., Ltd
Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
```

###### RTL8811AU - 600 mbps 
I found an answer from Ask Ubuntu (linked below) where there is a Github repository who adopted the driver code for Ubuntu 19.10. Follow the following steps to install. 

```bash
sudo apt install git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
sudo modprobe 88XXau
```
There might be a few issues you might face if you are trying to do in Proxmox.

##### First one:
```bash
root@pve:~/rtl8812au/rtl8812au# sudo ./dkms-install.sh
About to run dkms install steps...

Creating symlink /var/lib/dkms/rtl8812au/5.6.4.2/source ->
                 /usr/src/rtl8812au-5.6.4.2

DKMS: add completed.
Error! Your kernel headers for kernel 5.3.10-1-pve cannot be found.
Please install the linux-headers-5.3.10-1-pve package,
or use the --kernelsourcedir option to tell DKMS where it's located
Error! Your kernel headers for kernel 5.3.10-1-pve cannot be found.
Please install the linux-headers-5.3.10-1-pve package,
or use the --kernelsourcedir option to tell DKMS where it's located
Finished running dkms install steps.
```
To fix this, we need to install the missing libraries.
* Add /src/apt/sources.list with the below repo.
    ```bash
    # PVE pve-no-subscription repository provided by proxmox.com,
    # NOT recommended for production use
    deb http://download.proxmox.com/debian/pve buster pve-no-subscription
    ```
* Update the indices
    ```bash
    apt update
    ```
* Install headers
    ```bash
    apt install pve-headers-$(uname -r)
    ```
    
Done ! We have the headers now.
```bash
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  pve-headers-5.3.10-1-pve
0 upgraded, 1 newly installed, 0 to remove and 88 not upgraded.
Need to get 9,869 kB of archives.
After this operation, 67.1 MB of additional disk space will be used.
Get:1 http://download.proxmox.com/debian/pve buster/pve-no-subscription amd64 pve-headers-5.3.10-1-pve amd64 5.3.10-1 [9,869 kB]
Fetched 9,869 kB in 0s (20.1 MB/s)
Selecting previously unselected package pve-headers-5.3.10-1-pve.
(Reading database ... 64168 files and directories currently installed.)
Preparing to unpack .../pve-headers-5.3.10-1-pve_5.3.10-1_amd64.deb ...
Unpacking pve-headers-5.3.10-1-pve (5.3.10-1) ...
Setting up pve-headers-5.3.10-1-pve (5.3.10-1) ...
```
Now let's try build.


```bash
root@pve:~/rtl8812au/rtl8812au# sudo ./dkms-install.sh
About to run dkms install steps...
Error! DKMS tree already contains: rtl8812au-5.6.4.2
You cannot add the same module/version combo more than once.

Kernel preparation unnecessary for this kernel.  Skipping...

Building module:
cleaning build area...
'make' -j2 KVER=5.3.10-1-pve KSRC=/lib/modules/5.3.10-1-pve/build....................
cleaning build area...

DKMS: build completed.

88XXau.ko:
Running module version sanity check.
 - Original module
   - No original module exists within this kernel
 - Installation
   - Installing to /lib/modules/5.3.10-1-pve/updates/dkms/

depmod.....

DKMS: install completed.
Finished running dkms install steps.
```

Success :thumbsup: we now have the driver installed.

Now you should have an interface showing up with a name starting at wl.

```bash
#From an Ubuntu 18.04 Server - ifconfig
wlxe**e066c81b0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 2312
        inet6 fd**:f81d:fad:5**2:ea4e:6ff:f**c:81b0  prefixlen 64  scopeid 0x0<global>
        inet6 fe**::ea4e:6**:fe6c:8**0  prefixlen 64  scopeid 0x20<link>
        ether **:**:**:6c:81:b0  txqueuelen 1000  (Ethernet)
        RX packets 40  bytes 6076 (6.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15  bytes 3346 (3.3 KB)
        TX errors 0  dropped 2 overruns 0  carrier 0  collisions 0
```


















##### References

[AskUbuntu - rtl8814au-driver-for-kernel-5-3-on-ubuntu-19-10][1]  
[Proxmox - Package repositories][2]

  [1]: https://askubuntu.com/questions/1185952/need-rtl8814au-driver-for-kernel-5-3-on-ubuntu-19-10#comment2004621_1185986
  [2]: https://pve.proxmox.com/wiki/Package_Repositories
