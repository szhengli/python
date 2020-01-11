#!/usr/bin/python3
from dns import resolver as reso
from subprocess import check_call , check_output
from time import sleep

host = "api.weixin.qq.com"

def get_ip_from_hosts (host):
    cmd_ip = "awk  '/" + host + "/ {print $1} '  /etc/hosts"
    ip_from_hosts=check_output(cmd_ip, shell=True).decode().strip()
    return ip_from_hosts

def health_check(ip):
    try:
        check_call("ping -c 1  " + ip + " 2>/dev/null 1>/dev/null", shell=True, timeout=1)
        return True
    except Exception:
        return False

def get_good_ip(host):
    ip_from_hosts = get_ip_from_hosts(host)
    resolver = reso.Resolver()
    resolver.timeout=1
    resolver.nameservers = ["223.5.5..5","114.114.114.114"]
    try:
        res = resolver.query(host, "A")
        ips = [rc.address for rc in res.rrset.items]
    except Exception:
        ips = [ip_from_hosts]
    if (ip_from_hosts in ips) and health_check(ip_from_hosts) :
        print("no need to change")
        return ip_from_hosts
    else:
        for ip in ips:
            if health_check(ip):
                print(ip)
                return ip

def check_hosts(good):
    ip_from_hosts = get_ip_from_hosts(host)
    if not ip_from_hosts == good:
        cmd_sed= "sed -i 's/" + ip_from_hosts +  "/" + good + "/'   /etc/hosts"
        check_call(cmd_sed, shell=True, timeout=1)
        cmd_log = "echo changed to " + good + "  >>/var/log/ip_change.log"
        check_call(cmd_log, shell=True, timeout=1)

def main():
    while True:
        print("begin sleep")
        sleep(5)
        good = get_good_ip(host)
        print(good)
        if good :
            check_hosts(good)

main()



