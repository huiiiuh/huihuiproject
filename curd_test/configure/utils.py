import ipaddress

import IPy
from IPy import IP


def cal_ip(ip_net):
    try:
        ip_list = IPy.IP(ip_net, make_net=True)
        host = [x for x in ip_list]
        min_mask_str = str(host[0])
        max_mask_str = str(host[-1])
        return min_mask_str, max_mask_str
    except Exception as e:
        raise ValueError(e)


def iptoint(num):
    h = []
    s = num.split(".")
    e = 0
    for temp in s:
        a = bin(int(temp))[2:]
        a = a.zfill(8)
        h.append(a)
        g = "".join(h)
        e = int(g, 2)
    return e


if __name__ == '__main__':
    ip_net = '192.168.1.1/31'
    # cal_ip(ip_net)
    # iptoint('172.16.82.1')
    ips = IPy.IP('192.168.1.0/23', make_net=True)
    for ip in ips:
        print(ip)