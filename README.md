Mininet Extreme: An Enhanced Version of Mininet
========================================================

### What is Mininet Extreme?

Mininet Extreme introduces mount and PID namespaces to Mininet.
This makes it possible to execute applications in containers which require
independent configuration spaces, such as `Quagga` or `OpenVPN`. Built-in
configurations make adding a Quagga router to a network topology easy. In 
addition, Mininet Extreme is capable of connecting to the Transit Portal BGP 
multiplexing service to provide BGP connectivity to emulated routers.

Mininet Extreme enables emulation of complex network topologies, including
networks which combine technologies such as SDN and BGP. Networks can 
exchange routes and traffic with the real internet by combining Mininet Extreme
with Transit Portal.
  
### Added Functionality

Mininet Extreme adds:

* Support for mount namespaces, PID namespaces, legacy switches, legacy routers

* Built-in support for the Transit Portal BGP multiplexer and Quagga router

* New utilities to support topologies with configuration data

* New examples (in the `examples/` directory) to help you get started.

### Features to be added

* Support for generic hosts to make use of PID and mount namespaces

* Polishing of PID namespaces, enabling individual containers to have
  their own `init` and view only their processes through `ps aux` & etc.

### Debugging & Notes

* Errors about controllers or bridges `(mn-br#)` already existing

  If Mininet is not closed properly, it may not cleanup the junk 
  (interfaces, processes, files in /tmp, etc.) which might be left 
  around by Mininet or Linux. Try this if things stop working!

  `sudo mn -c`

* `mount` does not show the expected bindings!

  By default, `mount` references `/etc/mtab`, which is shared and
  updated by all containers and the host physical machine. As a result,
  this file does not remain in sync with the actual state of the system.
  To view the mounts within a specific container, execute:
  
  `cat /proc/PID/mounts`
  
  where `PID` references the bash shell or another process within the
  container in question. To view the current mounts of the host system,
  replace `PID` with `1`
  
### Installation and Sample Topology

See `INSTALL` for installation instructions and details.

### Credits

The Mininet Extreme Team:

* Brandon Schlinker (Network Systems Lab, USC)

The Mininet 2.1.0 Team:

* Bob Lantz
* Brian O'Connor
