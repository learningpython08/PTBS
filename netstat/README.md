### A simple netstat-like script ###
This script does the same like `netstat -nlp[t|u]` command with IPv4 support only

#### How to use

```
python netstat.py --help
usage: netstat.py [-h] [-u] [-t]

optional arguments:
 -h, --help  show this help message and exit
 -u, --udp   Netstat for UDP
 -t, --tcp   Netstat for TCP

```

You have to use `sudo` or run it under `root` in order to list all processes owned by `root` user.


### License
MIT

