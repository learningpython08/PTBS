#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A netstat -nlp[t|u] python script
Author: https://github.com/cuongnv23
'''

import os
import sys
import re
import glob
import argparse


def get_ip(hex):
    ''' Calculate IP from hex '''

    ip_hex = [hex[i:i+2] for i in range(0, len(hex), 2)][::-1]
    ip_dec = []
    [ip_dec.append(str(int(iph, 16))) for iph in ip_hex]
    return '.'.join(ip_dec)


def error(message, err):
    ''' Custom error message and detail err'''
    print "{}".format(message)
    print "Detail: {}".format(err)
    sys.exit(1)


def read_file(path, is_continue=None):
    ''' Read file and return file object '''
    try:
        with open(path, 'rb') as f:
            return f.read()
    except IOError as e:
        error("Unable to read {}".format(path), e)
    except:
        raise


def get_owner(uid):
    ''' Get owner of running uid '''
    pwd = read_file('/etc/passwd')
    for line in pwd.splitlines():
        if line.split(':')[2] == str(uid):
            return line.split(':')[0]


def get_state(state):
    ''' Get status of socket based on state code '''
    STAT = {1: 'ESTABLISHED',
            2: 'SYN_SENT',
            3: 'SYN_RECV',
            4: 'FIN_WAIT1',
            5: 'FIN_WAIT2',
            6: 'TIME_WAIT',
            7: 'CLOSE',
            8: 'CLOSE_WAIT',
            9: 'LAST_ACK',
            10: 'LISTEN',
            11: 'CLOSING',
            12: 'NEW_SYN_RECV'}
    return STAT[int(state, 16)]


def get_cmd_pid(inode):
    ''' Return list of pid and cmdline '''
    real_paths = [os.path.realpath(i) for i in glob.glob('/proc/*/fd/*')]
    for path in real_paths:
        if re.search(inode, path):
            pid = path.split('/')[2]
            cmd_file = os.path.join('/proc', str(pid), 'cmdline')
            try:
                with open(cmd_file) as f:
                    return [pid, f.read()]
            except IOError:
                continue


def parse_line(line):
    ''' Parse line structure '''
    l = line.split()
    laddr = l[1].split(':')[0]
    lport = l[1].split(':')[1]
    raddr = l[2].split(':')[0]
    rport = l[2].split(':')[1]
    state = l[3]
    uid = l[7]
    inode = l[9]
    return {'laddr': laddr,
            'lport': lport,
            'raddr': raddr,
            'rport': rport,
            'state': state,
            'uid': uid,
            'inode': inode}


def netstat(pro):
    ''' Read pro(tcp/udp) socket file '''
    print "User\tProto\tLocal Address\tRemote Address\tState\tPID\tCommand"
    proc = read_file('/proc/net/' + pro)
    for line in proc.splitlines()[1:]:
        l = parse_line(line)
        p = get_cmd_pid(l.get('inode'))
        # tricky
        if not p:
            p = [None, None]

        if pro == 'tcp':
            print "{}\t{}\t{}:{}\t{}:{}\t{}\t{}\t{}".format(
                get_owner(l['uid']), pro, get_ip(l['laddr']),
                int(l['lport'], 16), get_ip(l['raddr']),
                int(l['rport'], 16), get_state(l['state']),
                p[0], p[1])
        else:
            print "{}\t{}\t{}:{}\t{}:{}\t{}\t{}\t{}".format(
                get_owner(l['uid']), pro, get_ip(l['laddr']),
                int(l['lport'], 16), get_ip(l['raddr']),
                int(l['rport'], 16), '',
                p[0], p[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--udp", help="Netstat for UDP",
                        action="store_true")
    parser.add_argument("-t", "--tcp", help="Netstat for TCP",
                        action="store_true")
    if len(sys.argv) != 2:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    if args.tcp:
        netstat('tcp')
    elif args.udp:
        netstat('udp')
    else:
        parser.print_help()
        sys.exit(1)
