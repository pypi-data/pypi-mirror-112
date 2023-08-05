Piotr: Pythonic IoT exploitation and Research
=============================================

System dependencies
-------------------

$ apt install qemu-system-arm


Introduction to Piotr
---------------------

Piotr is an emulation helper for Qemu that provides a convenient way to
create, share and run virtual IoT devices. It only supports the ARM Architecture
at the moment.

Piotr is heavily inspired from @therealsaumil's ARM-X framework and keeps the
same approach: emulated devices run inside an emulated host that provides
all the tools you may need and creates a fake environment for them. This
approach allows remote debugging with gdbserver or fridaserver, provides a
steady platform for vulnerability research, exploitation and training.

Moreover, Piotr is able to package any emulated device into a single file that
may be shared and imported by other users, thus sharing its kernel, DTB file or
even its host filesystem. This way, it is possible to create new emulated
devices based upon existing ones, and to improve all of them by simply changing
a single file (kernel, host filesystem, etc.).


How does Piotr work ?
---------------------

Piotr stores everything it needs inside a specific user directory called `.piotr`,
located in the user's home directory. This directory stores all the kernels, dtb
files, host filesystems and emulated devices.

Each emulated device is stored in a specific subdirectory of your `.piotr/devices`
directory, and must contain at least:

 * a *config.yaml* file containing the device's qemu configuration in a readable way
 * a root filesystem with correct permissions and groups and users

When Piotr is asked to emulate a specific device, it loads its *config.yaml* file,
parses it and creates a Qemu emulated device with the corresponding specifications.

This emulated device can then be driven by Piotr's helper tools in order to:

 * list or kill running processes
 * dynamically configure network interfaces
 * debug any process running on the emulated device
 * ...

Create your own emulated embedded device
----------------------------------------

If you want to emulate a specific embedded device, you may follow these steps:

 * use piotr to create a device skeleton: piotr device create <device name>
 * edit the new *config.yaml* file created in the device's directory in order to fit the specifications:
   * specify the kernel version to use (you may want to build a new one with *buildroot* if it is not available, see XXX)
   * specify the host filesystem version to use
   * specify the bootargs, the network configuration, the memory size, etc.
 * rebuild the entire filesystem from the embedded device in the rootfs directory

Import our example emulated Teltonika RUTX10 router
---------------------------------------------------

Download our example device from here: TODO, and then import it:

```
$ sudo piotr device add teltonika-rutx10.piotr
```

This command will ask Piotr to add the Teltonika RUTX10 emulated router to your
own devices. By doing so, Piotr will create the device in your *.piotr/devices/*
directory, install the required kernel and host filesystem, and make it ready to
use.

Start an emulated embedded device
---------------------------------

To start an emulated device, just type the following:

```
$ sudo piotr device start rutx10
```

This will starts a *qemu-system-arm* command that will display a login prompt.
This login prompt belongs to the emulation host, which is basically the emulated
device. Enter *piotr* as user, and no password, this will give you a shell on the
emulated device.

Then, start the target device emulation by issuing the following command:

```
[Host]# target-start
```

If you try this with our RUTX10 example device, this will start its web server
that will listen on port 80 on a tap network interface. On your host machine,
configure the tap inferface:

```
# ifconfig eth0 192.168.100.1
```

Then, launch a web browser and browse to http://192.168.100.2/ to show RUTX10
web administration interface.

Stop an emulated embedde device
-------------------------------

First, find your emulated device by listing running instances:

```
$ sudo piotr device running
```

Each instance has a given name, use the name of the instance you want to stop
to make it stop:

```
$ sudo piotr device stop <instance name>
```
