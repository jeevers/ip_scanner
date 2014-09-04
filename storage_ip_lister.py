#!/usr/bin/env python
from sh import nmap
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import re

ip_nets = ["192.168.11.",
       "192.168.12.",
       "192.168.15.",
       "192.168.22.",
       "192.168.122.",
       "192.168.115."]
#ip_nets = ["192.168.11."]
port_listen = 8068
poll_interval = 20
ip_scan = []

def disp_storage_ips(subnets):
    nmap_args = ["-sP"] + [item+"0/24" for item in subnets]
    vlans = nmap(nmap_args)
    ip_patt = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    p = re.compile(ip_patt)
    p.findall(vlans.stdout)

    dns_resolved = "Host (.*) \(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\) appears to be up"
    resolved_re = re.compile(dns_resolved)
    resolved = resolved_re.findall(vlans.stdout)

    hostname_dict = {}

    for record in resolved:
        hostname_dict[record[1]] = record[0]

    storage_ips = [[subnet+str(last_oct) for last_oct in range(1,256)] for subnet in subnets]

    active_ips = p.findall(vlans.stdout)

    ip_usage = []

    for vlan in storage_ips:
        vlan_list = []
        for ip in vlan:
            if ip in active_ips:
                try:
                    vlan_list.append([ip, 'ACTIVE', hostname_dict[ip]]) 
                except KeyError:
                    vlan_list.append([ip, 'ACTIVE', ''])
            else:
                vlan_list.append([ip, 'INACTIVE', ''])
        ip_usage.append(vlan_list)
    return ip_usage

def ip_poll():
    print("ip scan start")
    global ip_scan
    ip_scan = disp_storage_ips(ip_nets)
    print("ip scan stop")

class mainHandler(tornado.web.RequestHandler):
    def get(self):
        global ip_scan
        if ip_scan == []:
            raise tornado.web.HTTPError(504)
        else:
            #ip_usage = disp_storage_ips(ip_nets)
            self.render('ip_table.tpl', ip_usage=ip_scan)

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates')
}

application = tornado.web.Application([
	(r'/', mainHandler),
], **settings)

if __name__ == '__main__':
    import signal
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port_listen)
    loop = tornado.ioloop.IOLoop.instance()
    def sigint_handler(signum, frame):
        print('signal handler called with %s, frame %s' % (signum, frame))
        periodic_cbk.stop()
        loop.stop()
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGHUP, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    periodic_cbk = tornado.ioloop.PeriodicCallback(ip_poll,
                                                   poll_interval*60*1000,
                                                   loop)
    periodic_cbk.start()
    ip_poll()
    loop.start()
