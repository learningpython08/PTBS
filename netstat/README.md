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

Sample output:

```
$ ./netstat.py -t
User    Proto   Local Address   Remote Address  State   PID Command
root    tcp 127.0.0.1:25    0.0.0.0:0   LISTEN  None    None
statd   tcp 0.0.0.0:39973   0.0.0.0:0   LISTEN  None    None
root    tcp 0.0.0.0:111 0.0.0.0:0   LISTEN  None    None
root    tcp 127.0.0.1:53    0.0.0.0:0   LISTEN  None    None
root    tcp 192.168.1.61:51068  151.101.129.69:80   TIME_WAIT   1272    /lib/systemd/systemd--user
root    tcp 192.168.1.61:52940  216.58.221.142:443  TIME_WAIT   1272    /lib/systemd/systemd--user
root    tcp 192.168.1.61:54862  216.58.197.110:443  TIME_WAIT   1272    /lib/systemd/systemd--user

```



### License
MIT

