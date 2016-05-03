#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

def run(upstream, server_name_port, hosts_fname):
    try:
        host, port = upstream.split(":")
        import socket
        ip4addr = socket.gethostbyname(host)
        
        snp_lst = server_name_port.split(":")
        server_name = snp_lst[0]
        server_port = snp_lst[1] if len(snp_lst) > 1 else 80
    
        def get_contents(fname):
            with open(hosts_fname) as f:
                txt = f.read()
            return txt
            
        def write_hosts(txt):
            # :TODO: race conditions - вдруг 2 скрипта сразу пишут
            import o_p
            with o_p.for_write(hosts_fname) as f:
                f.write(txt)
    
        need_update_hosts = False
        hosts_txt = get_contents(hosts_fname)
            
        # 1 добавляем запись в /etc/hosts
        import re
        m = re.search(r"^.+[ \t]%s" % re.escape(server_name), hosts_txt, re.M)
        if not m:
            need_update_hosts = True
            temp_host_line = "\n%(ip4addr)s\t%(server_name)s" % locals()
            
            hosts_txt += temp_host_line
            write_hosts(hosts_txt)
            
    
        import signal
        
        def on_signal(_signum, _ignored_):
            print("Request to stop ...")
            # 3 обратно    
            if need_update_hosts:
                hosts_txt = get_contents(hosts_fname)
                m = re.search(r"^%s$" % re.escape(temp_host_line), hosts_txt, re.M)
                assert m
                
                hosts_txt = hosts_txt[:m.start()] + hosts_txt[m.end():]
                write_hosts(hosts_txt)
        
        
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, on_signal)
            
        # 2 проксирование
        cmd = "socat TCP4-LISTEN:%(server_port)s,fork,reuseaddr TCP4:%(upstream)s" % locals()
        import subprocess
        import shlex
        subprocess.call(shlex.split(cmd))
    except IOError, e:
        print(e)
        print("Use under root (sudo)")
        
def main():
    if True:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("upstream", help="host:port to proxy to")
        parser.add_argument("server_name_port", help="server_name[:port] to be frontend")
        args = parser.parse_args()
        
        run(args.upstream, args.server_name_port, "/etc/hosts")

    if False:
        upstream = "localhost:8080"
        server_name_port = "cat.bombono.org:2222"
            
        hosts_fname = "/home/ilya/opt/programming/catbo/stuff/authomatic/hosts"
        run(upstream, server_name_port, hosts_fname)
    
if __name__ == "__main__":
    main()