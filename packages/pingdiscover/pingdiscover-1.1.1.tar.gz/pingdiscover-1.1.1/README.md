# pingdiscover is simple commandline app for looking up hosts in given network 
# Installation
### Using Pip```bash
  $ pip install pingdiscover
```## Manual```bash
  $ git clone https://github.com/
  $ cd pingdiscover
  $ python3 setup.py install

### Using Makefile
  $ make install

# Usage
$ pingdiscover 192.168.0.0/24 --concurrent 8 --timeout 3
$ pingdiscover 192.168.0.0/24 --concurrent 10

