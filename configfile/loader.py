<<<<<<< HEAD
import yaml
from models.vlan import Vlan
from models.router import Router
from models.dp import DP, Interface
from models.config import Config

def load_vlan(data):
    return Vlan(
        vid=data.get('vid'),
        description=data.get('description', ''),
        acls_in=data.get('acls_in', []),
        faucet_mac=data.get('faucet_mac', ''),
        faucet_vips=data.get('faucet_vips', []),
        routes=[
            {
                'ip_dst': route['route'].get('ip_dst', ''),
                'ip_gw': route['route'].get('ip_gw', '')
            } for route in data.get('routes', [])
        ],
        acl_in=data.get('acl_in', None),
        dot1x_assigned=data.get('dot1x_assigned', False),
        max_hosts=data.get('max_hosts', 255),
        minimum_ip_size_check=data.get('minimum_ip_size_check', True),
        name=data.get('name', ''),
        proactive_arp_limit=data.get('proactive_arp_limit', 2052),
        proactive_nd_limit=data.get('proactive_nd_limit', 2052),
        targeted_gw_resolution=data.get('targeted_gw_resolution', False),
        unicast_flood=data.get('unicast_flood', True)
    )

def load_router(data):
    return Router(vlans=data['vlans'])

def load_interface(data):
    return Interface(
        name=data['name'],
        description=data['description'],
        native_vlan=data.get('native_vlan'),
        tagged_vlans=data.get('tagged_vlans', []),
        acls_in=data.get('acls_in', [])
    )

def load_dp(data):
    interfaces = {k: load_interface(v) for k, v in data['interfaces'].items()}
    return DP(dp_id=data['dp_id'], hardware=data['hardware'], interfaces=interfaces)

def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    
    vlans = {k: load_vlan(v) for k, v in data.get('vlans', {}).items()}
    routers = {k: load_router(v) for k, v in data.get('routers', {}).items()}
    dps = {k: load_dp(v) for k, v in data.get('dps', {}).items()}
    
=======
import yaml
from models.vlan import Vlan
from models.router import Router
from models.dp import DP, Interface
from models.config import Config

def load_vlan(data):
    return Vlan(
        vid=data.get('vid'),
        description=data.get('description', ''),
        acls_in=data.get('acls_in', []),
        faucet_mac=data.get('faucet_mac', ''),
        faucet_vips=data.get('faucet_vips', []),
        routes=[
            {
                'ip_dst': route['route'].get('ip_dst', ''),
                'ip_gw': route['route'].get('ip_gw', '')
            } for route in data.get('routes', [])
        ],
        acl_in=data.get('acl_in', None),
        dot1x_assigned=data.get('dot1x_assigned', False),
        max_hosts=data.get('max_hosts', 255),
        minimum_ip_size_check=data.get('minimum_ip_size_check', True),
        name=data.get('name', ''),
        proactive_arp_limit=data.get('proactive_arp_limit', 2052),
        proactive_nd_limit=data.get('proactive_nd_limit', 2052),
        targeted_gw_resolution=data.get('targeted_gw_resolution', False),
        unicast_flood=data.get('unicast_flood', True)
    )

def load_router(data):
    return Router(vlans=data['vlans'])

def load_interface(data):
    return Interface(
        name=data['name'],
        description=data['description'],
        native_vlan=data.get('native_vlan'),
        tagged_vlans=data.get('tagged_vlans', []),
        acls_in=data.get('acls_in', [])
    )

def load_dp(data):
    interfaces = {k: load_interface(v) for k, v in data['interfaces'].items()}
    return DP(dp_id=data['dp_id'], hardware=data['hardware'], interfaces=interfaces)

def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    
    vlans = {k: load_vlan(v) for k, v in data.get('vlans', {}).items()}
    routers = {k: load_router(v) for k, v in data.get('routers', {}).items()}
    dps = {k: load_dp(v) for k, v in data.get('dps', {}).items()}
    
>>>>>>> 3508a699cb3b3084ed8ee2b733643c54a21b8047
    return Config(include=data.get('include', []), vlans=vlans, routers=routers, dps=dps)