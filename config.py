import os

def str2int(v):
    return int(v)


HAPROXY_CFG_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'haproxy.cfg.template')

def default_cfg():
    if not os.path.exists(HAPROXY_CFG_TEMPLATE_PATH):
        return None
    with open(HAPROXY_CFG_TEMPLATE_PATH, 'r') as f:
        return f.read()
    
# envvar
DEBUG = os.getenv("DEBUG", False)
SERVICE_NAME = os.getenv("SERVICE_NAME", None)
SERVICE_PORT = str2int(os.getenv("SERVICE_PORT", 80))
HAPROXY_CFG_TEMPLATE = os.getenv("HAPROXY_CFG_TEMPLATE", default_cfg())

HAPROXY_CFG_PATH = "/etc/haproxy.cfg"
HAPROXY_RUN_COMMAND = ['/usr/local/sbin/haproxy', '-f', HAPROXY_CFG_PATH, '-db', '-q']
