---
title: Network Connectivity through Wireless interface for Debian
abstract: test
keywords: proxmox, WiFi usb adapter
categories: IT
weblogName: arrays.stream
postDate: 2020-04-17T00:22:23.6197990-04:00
---

# Network Connectivity through Wireless interface for Debian  
  

![xkcd](https://imgs.xkcd.com/comics/tar.png)  
Permanent link to this comic: https://xkcd.com/1168/

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

###### RTL88XXBU - 1200 mbps 
```bash
sudo apt install git dkms
git clone https://github.com/cilynx/rtl88x2bu.git
cd rtl88x2bu
VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
sudo rsync -rvhP ./ /usr/src/rtl88x2bu-${VER}
sudo dkms add -m rtl88x2bu -v ${VER}
sudo dkms build -m rtl88x2bu -v ${VER}
sudo dkms install -m rtl88x2bu -v ${VER}
sudo modprobe 88x2bu
```

There might be a few issues you might face if you are trying to do these in Proxmox.

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
#From an Ubuntu 18.04 Server - ifconfig - Obfuscated for kicks
wlxe**e066c81b0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 2312
        inet6 fd**:f81d:fad:5**2:ea4e:6ff:f**c:81b0  prefixlen 64  scopeid 0x0<global>
        inet6 fe**::ea4e:6**:fe6c:8**0  prefixlen 64  scopeid 0x20<link>
        ether **:**:**:6c:81:b0  txqueuelen 1000  (Ethernet)
        RX packets 40  bytes 6076 (6.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15  bytes 3346 (3.3 KB)
        TX errors 0  dropped 2 overruns 0  carrier 0  collisions 0
```

---

If you my goal was to get a typical Ubuntu box, I would be done by now. But, we need a Linux Bridge for Proxmox machine which can enslave the new wifi module. And then we connect that bridge to all the VM NICs

---

Well, I realized that it cannot be done or I don't understand it enough to do that. That is when I came across this post from super helpful folks at Proxmox - [link][3]. The issue mentioned here is not exactly what my problem is  but it gave me a framework to work with.

> As per, Stoiko Ivanov, Proxmox Staff Member:  
>
> AFAIR wifi-interfaces usually do not support being part of a bridge in station (client) mode (i.e. you can only add them in access-point mode).
> 
> What should work is using a NAT/routed config - see https://pve.proxmox.com/pve-docs/ch..._nat_with_span_class_monospaced_iptables_span
> 
> just take the wlo1 as interface holding the default route, add a vmbr0 without any physical ports, configure ip-forwarding and optionally add NAT rules.
> 
> hope this helps!

#### Alright the new plan!

We are not going to enslave the WiFi adapter and instead we will create a Linux Bridge without any physical ports and setup up default gateway only on the WiFi interface.

> HA! That worked. 

So the final configuration looks like this.

```bash
root@pve:~# cat /etc/network/interfaces
auto lo
iface lo inet loopback

#iface ens18 inet manual - DISABLED ETHERNET PORT

auto wlx1****2ee2b #Wireless device
iface wlx1****2ee2b inet static
        address 192.168.0.29
        netmask 255.255.255.0
        gateway 192.168.0.1
        wpa-ssid SSID_NAME
        wpa-psk 761185c*******aea444****5900db9

auto vmbr0  #Bridge with no ports for the Linux bridge
iface vmbr0 inet static
        address  10.10.10.1
        netmask  255.255.255.0
        bridge_ports none
        bridge_stp off
        bridge_fd 0
        #Masquerading rules below
        post-up   echo 1 > /proc/sys/net/ipv4/ip_forward
        post-up   iptables -t nat -A POSTROUTING -s '10.10.10.0/24' -o wlx1****2ee2b -j MASQUERADE
        post-down iptables -t nat -D POSTROUTING -s '10.10.10.0/24' -o wlx1****2ee2b -j MASQUERADE
        # Exposing port 22 of a VM connected to Linux Bridge.
        post-up iptables -t nat -A PREROUTING -i vmbr0 -p tcp --dport 2222 -j DNAT --to 10.10.10.25:22
        post-down iptables -t nat -D PREROUTING -i vmbr0 -p tcp --dport 2222 -j DNAT --to 10.10.10.25:22
```

I am now able to reach to internet and other local network from Proxmox (Debian) shell. 

Data transfer rates with WiFi adapters (rated at 600 Mbps to 1200 Mbps but only giving 45 mbps) were disappointing at best, but it works for my use case. 

I ran some tests using iPerf3 - Look here for instructions.

```bash
#Test was between another machine in the same network - Interface is WIFI
#Both test machines are using same wifi adapters. No wired connection.
user@kubernetes:~/iperf$ iperf3 -c 192.168.0.18
Connecting to host 192.168.0.18, port 5201
[  4] local 192.168.0.24 port 34256 connected to 192.168.0.18 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec  6.45 MBytes  54.1 Mbits/sec    0    215 KBytes
[  4]   1.00-2.00   sec  5.94 MBytes  49.9 Mbits/sec    0    215 KBytes
[  4]   2.00-3.00   sec  5.51 MBytes  46.3 Mbits/sec    0    215 KBytes
[  4]   3.00-4.00   sec  5.39 MBytes  45.2 Mbits/sec    0    215 KBytes
[  4]   4.00-5.00   sec  4.96 MBytes  41.6 Mbits/sec    0    215 KBytes
[  4]   5.00-6.00   sec  3.80 MBytes  31.9 Mbits/sec    0    215 KBytes
[  4]   6.00-7.00   sec  1.96 MBytes  16.4 Mbits/sec    0    215 KBytes
[  4]   7.00-8.00   sec  6.62 MBytes  55.5 Mbits/sec    0    215 KBytes
[  4]   8.00-9.00   sec  6.31 MBytes  52.9 Mbits/sec    0    215 KBytes
[  4]   9.00-10.00  sec  5.94 MBytes  49.8 Mbits/sec    0    215 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  52.9 MBytes  44.4 Mbits/sec    0             sender
[  4]   0.00-10.00  sec  51.9 MBytes  43.5 Mbits/sec                  receiver
```

### Next Steps:
Now I have Proxmox servers with WiFi connectivity, but I still  have to figure out the internal network for the VMs. 
There are still many many concerns to be addressed:
* How the routing happens
* speed
* DHCP assignments
* How do I get into that box - VPN or bridge
* iDrac have an Ethernet port and I need to find a way to get that online too.

Possible directions:
* I got my Archer C7 upgraded to the latest firmware and it seems to be working fine now. So now I'm back to using wired connections for most of the things and WIFI is like a back up if Archer C7 starts dropping connections.
* Get Linux ready WiFi adapters and see how the speeds improve.
* Learn more about Linux networking and Proxmox to figure out the vlan setup with the bridge and might use Vyos as a virtualized internal network router.



##### References
I have used so many resources while I was trying to figure it out. Some of them are linked below.

[AskUbuntu - rtl8814au-driver-for-kernel-5-3-on-ubuntu-19-10][1]  
[Proxmox - Package repositories][2]  
[Proxmox - using wifi instead of ethernet][3]  
[Masquerading (NAT) with iptables][4]

  [1]: https://askubuntu.com/questions/1185952/need-rtl8814au-driver-for-kernel-5-3-on-ubuntu-19-10#comment2004621_1185986
  [2]: https://pve.proxmox.com/wiki/Package_Repositories
  [3]: https://forum.proxmox.com/threads/using-wifi-instead-of-ethernet.56691/
  [4]: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#_masquerading_nat_with_span_class_monospaced_iptables_span
