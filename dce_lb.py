# -*- coding: utf-8 -*-

import logging
import sys
import subprocess
import thread
import time
import signal
import os

from dns import resolver
from jinja2 import Template

from config import DEBUG, HAPROXY_CFG_TEMPLATE, HAPROXY_CFG_PATH, \
    HAPROXY_RUN_COMMAND, SERVICE_NAME

LOG = logging.getLogger(__name__)

def run_haproxy(msg=None):
    LOG.info("==========BEGIN==========")
    if msg:
        LOG.info(msg)
    haproxy = Haproxy()
    haproxy.update()
    
def save_to_file(name, content):
    with open(name, 'w') as f:
        f.write(content)
    
def run_reload(old_process):
    if old_process:
        # Reload haproxy
        LOG.info("Reloading HAProxy")
        new_process = subprocess.Popen(HAPROXY_RUN_COMMAND + ["-sf", str(old_process.pid)])
        thread.start_new_thread(wait_log, (old_process,))
        LOG.info("HAProxy has been reloaded(PID: %s)", str(new_process.pid))
    else:
        # Launch haproxy
        LOG.info("Launching HAProxy")
        new_process = subprocess.Popen(HAPROXY_RUN_COMMAND)
        LOG.info("HAProxy has been launched(PID: %s)", str(new_process.pid))

    return new_process
    
def wait_log(process):
    process.wait()
    LOG.info("HAProxy(PID:%s) has been terminated" % str(process.pid))
    time.sleep(1)
    if Haproxy.last_proc == process:
        LOG.info("HAProxy has been terminated, Exiting...")
        sys.exit(1)

def dns_query(service_name):
    try:
        return set(map(str, resolver.query("%s." % service_name)))
    except Exception as e:
        LOG.warn("DNS query %s error %s" % (service_name, e))
        return set()

class Haproxy(object):
    last_cfg = None
    last_proc = None
    last_hosts = None
    
    def update(self):
        template = Template(HAPROXY_CFG_TEMPLATE)
        hosts = dns_query(SERVICE_NAME)
        cfg = template.render(SERVICE_HOSTS=hosts, **os.environ)
        self._update_haproxy(cfg)
        Haproxy.last_hosts = hosts
        
    def _update_haproxy(self, cfg):
        if Haproxy.last_cfg == cfg:
            LOG.info("configuration remains unchanged")
            return
            
        LOG.info("change haproxy configuration")
        save_to_file(HAPROXY_CFG_PATH, cfg)
        Haproxy.last_cfg = cfg
        Haproxy.last_proc = run_reload(Haproxy.last_proc)
        LOG.info("===========END===========")
        
def listen_dns_srv_changed():
    while True:
        hosts = dns_query(SERVICE_NAME)
        if len(hosts) and Haproxy.last_hosts != hosts:  # 避免DNS意外失效
            return
        time.sleep(1)
               
def on_user_reload(signum, frame):
    Haproxy.last_cfg = None
    run_haproxy("User reload")
                
def main():
    logging.basicConfig(stream=sys.stdout)
    LOG.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    if DEBUG:
        LOG.setLevel(logging.DEBUG)

    signal.signal(signal.SIGUSR1, on_user_reload)
    signal.signal(signal.SIGTERM, sys.exit)

    run_haproxy("Initial start")
    while True:
        listen_dns_srv_changed()
        run_haproxy('Reconnect dns_srv')
    

if __name__ == '__main__':
    main()
