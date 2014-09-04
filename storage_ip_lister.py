#!/usr/bin/env python
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import re
import yaml
import iptools

from sh import nmap
from dns import reversename, resolver


def config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with file(config_path, 'r') as config_file:
        config_dict = yaml.load(config_file)
        return config_dict


def disp_storage_ips(subnets):
    nmap_args = ["-nsP"] + [item for item in subnets]
    vlans = nmap(nmap_args)
    ip_patt = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    p = re.compile(ip_patt)
    #p.findall(vlans.stdout)
    active_ips = p.findall(vlans.stdout)

    storage_ips = [iptools.IpRangeList(subnet) for subnet in subnets]

    ip_usage = []

    for vlan in storage_ips:
        vlan_list = []
        for ip in vlan:
            try:
                host = reversename.from_address(ip)
                name = resolver.query(host, 'PTR')[0].to_text()
            except resolver.NXDOMAIN:
                name = ''
            if ip in active_ips:
                vlan_list.append([ip, 'ACTIVE', name])
            else:
                vlan_list.append([ip, 'INACTIVE', name])
        ip_usage.append(vlan_list)
    return ip_usage

def ip_poll():
    print("ip scan start")
    global ip_scan
    ip_scan = disp_storage_ips(config()['subnets'])
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
    http_server.listen(config()['port_listen'])
    loop = tornado.ioloop.IOLoop.instance()
    def sigint_handler(signum, frame):
        print('signal handler called with %s, frame %s' % (signum, frame))
        periodic_cbk.stop()
        loop.stop()
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGHUP, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)
    poll_interval = config()['poll_interval']
    periodic_cbk = tornado.ioloop.PeriodicCallback(ip_poll,
                                                   poll_interval*60*1000,
                                                   loop)
    periodic_cbk.start()
    ip_poll()
    loop.start()
