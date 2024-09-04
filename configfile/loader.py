# loader.py

import yaml
import re
from models.vlan import Vlan
from models.router import Router
from models.dp import DP, Interface
from models.config import Config
from models.acls import ACL, Rule


# Custom exception for invalid YAML format
class InvalidYAMLFormatError(Exception):
    pass

# Constructor to handle hexadecimal values (need to display the hexadecimal) 
def hex_int_constructor(loader, node):
    value = loader.construct_scalar(node)
    if value.startswith('0x'):
        return value
    try:
        return int(value, 0)
    except ValueError:
        return value

# Register the custom constructor for YAML
hex_pattern = re.compile(r'^0x[0-9a-fA-F]+$')
yaml.SafeLoader.add_implicit_resolver('!hex_int', hex_pattern, None)
yaml.SafeLoader.add_constructor('!hex_int', hex_int_constructor)

# Load the VLAN data from the config file
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
    return Router(router=data['routers'])

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

def load_acls(acls_data):
    print(f"load acls acls_data type: {type(acls_data)}, content: {acls_data}")
    acls = {}
    if isinstance(acls_data, dict):
        for acl_name, acl_rules in acls_data.items():
            rules = [Rule(rule) for rule in acl_rules]
            acls[acl_name] = ACL(name=acl_name, rules=rules)
    else:
        raise TypeError("Expected acls_data to be a dictionary")
    return acls

# load the selected faucet yaml configuration file
def load_config(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            if data is None:
                raise InvalidYAMLFormatError("Faucet configuration file is empty or contains only comments")
    except yaml.YAMLError as e:
        raise InvalidYAMLFormatError(f"Invalid YAML format: {e}")
    
    vlans = {k: load_vlan(v) for k, v in data.get('vlans', {}).items()}
    routers = {k: load_router(v) for k, v in data.get('routers', {}).items()}
    dps = {k: load_dp(v) for k, v in data.get('dps', {}).items()}
    acls_data = data.get('acls', {})
    #print(f"acls_data type: {type(acls_data)}, content: {acls_data}")
    acls = load_acls(acls_data)
    
    return Config(vlans=vlans, routers=routers, dps=dps, acls=acls)


def new_config():
    default_vlan = Vlan(
        vid=1,
        description='Default VLAN',
        acls_in=[],
        faucet_mac='',
        faucet_vips=[],
        routes=[],
        acl_in=None,
        dot1x_assigned=False,
        max_hosts=255,
        minimum_ip_size_check=True,
        name='default',
        proactive_arp_limit=2052,
        proactive_nd_limit=2052,
        targeted_gw_resolution=False,
        unicast_flood=True
    )

    default_dp = DP(
        dp_id=1,
        hardware='default_hardware',
        interfaces={}
    )

    vlans = {'default_vlan': default_vlan}
    dps = {'default_dp': default_dp}
    routers = {}

    return Config(vlans=vlans, routers=routers, dps=dps)