# loader.py

import yaml
from models.vlan import Vlan
from models.router import Router
from models.dp import DP, Interface
from models.config import Config
from models.acls import ACL, Rule


# Custom exception for invalid YAML format
class InvalidYAMLFormatError(Exception):
    pass

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
    #lldp_beacon = data.get('lldp_beacon', None)  # Set to None if not provided
    #lldp_beacon_org_tlvs = []
    #print(lldp_beacon['org_tlvs'])
    # if lldp_beacon:
    #     lldp_beacon_org_tlvs = [
    #         {
    #             'info': tlv.get('info'),
    #             'oui': tlv.get('oui'),
    #             'subtype': tlv.get('subtype')
    #         } for tlv in lldp_beacon.get('org_tlvs', None)
    #     ]
    #     lldp_beacon['org_tlvs'] = lldp_beacon_org_tlvs

    stack = data.get('stack', {})
    lldp_beacon = data.get('lldp_beacon', {})

    return Interface(
        name=data['name'],
        description=data['description'],
        native_vlan=data.get('native_vlan'),
        tagged_vlans=data.get('tagged_vlans', []),
        acls_in=data.get('acls_in', []),
        acl_in=data.get('acl_in'),
        dot1x=data.get('dot1x'),
        dot1x_acl=data.get('dot1x_acl'),
        dot1x_mab=data.get('dot1x_mab'),
        enabled=data.get('enabled'),
        hairpin=data.get('hairpin'),
        lldp_beacon=lldp_beacon,
        loop_protect=data.get('loop_protect'),
        loop_protect_external=data.get('loop_protect_external'),
        max_hosts=data.get('max_hosts'),
        mirror=data.get('mirror', []),
        number=data.get('number'),
        opstatus_reconf=data.get('opstatus_reconf'),
        output_only=data.get('output_only'),
        permanent_learn=data.get('permanent_learn'),
        stack=stack,
        unicast_flood=data.get('unicast_flood'),
        restricted_bcast_arpnd=data.get('restricted_bcast_arpnd'),
        coprocessor=data.get('coprocessor')
    )

def load_dp(data):
    interfaces = {k: load_interface(v) for k, v in data['interfaces'].items()}
    lldp_beacon = data.get('lldp_beacon', {})
    stack = data.get('stack', {})

    return DP(
        dp_id=data.get('dp_id'),
        hardware=data.get('hardware'),
        advertise_interval=data.get('advertise_interval'),
        arp_neighbor_timeout=data.get('arp_neighbor_timeout'),
        description=data.get('description'),
        drop_broadcast_source_address=data.get('drop_broadcast_source_address'),
        drop_spoofed_faucet_mac=data.get('drop_spoofed_faucet_mac'),
        group_table=data.get('group_table'),
        high_priority=data.get('high_priority'),
        highest_priority=data.get('highest_priority'),
        ignore_learn_ins=data.get('ignore_learn_ins'),
        interface_ranges=data.get('interface_ranges'),
        learn_ban_timeout=data.get('learn_ban_timeout'),
        learn_jitter=data.get('learn_jitter'),
        low_priority=data.get('low_priority'),
        lowest_priority=data.get('lowest_priority'),
        max_host_fib_retry_count=data.get('max_host_fib_retry_count'),
        max_hosts_per_resolve_cycle=data.get('max_hosts_per_resolve_cycle'),
        max_resolve_backoff_time=data.get('max_resolve_backoff_time'),
        metrics_rate_limit_sec=data.get('metrics_rate_limit_sec'),
        name=data.get('name'),
        ofchannel_log=data.get('ofchannel_log'),
        packetin_pps=data.get('packetin_pps'),
        slowpath_pps=data.get('slowpath_pps'),
        priority_offset=data.get('priority_offset'),
        proactive_learn_v4=data.get('proactive_learn_v4'),
        proactive_learn_v6=data.get('proactive_learn_v6'),
        timeout=data.get('timeout'),
        use_idle_timeout=data.get('use_idle_timeout'),
        table_sizes=data.get('table_sizes'),
        port_table_scale_factor=data.get('port_table_scale_factor'),
        global_vlan=data.get('global_vlan'),
        dot1x=data.get('dot1x'),
        interfaces=interfaces,   
        lldp_beacon=lldp_beacon,
        stack=stack         
    )

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

# def convert_dl_type_to_hex(data):
#     if 'dl_type' in data and isinstance(data['dl_type'], int):
#         data['dl_type'] = hex(data['dl_type'])
#     return data

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

    default_acl = ACL(
        name='New ACL',
        rules=[]
    )

    vlans = {'default_vlan': default_vlan}
    dps = {'default_dp': default_dp}
    acls = {'default_acls': default_acl}
    routers = {}

    return Config(vlans=vlans, routers=routers, dps=dps, acls=acls)