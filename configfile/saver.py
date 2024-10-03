import yaml
from models.vlan import Vlan, Route
from models.router import Router, Bgp
from models.dp import DP, Interface
from models.acls import ACL, Rule, Action, OutputAction, TunnelAction
from models.config import Config
from models.meter import Meter  # Import Meter class

# Custom representer for Vlan objects
# Custom representer for Vlan objects
def vlan_representer(dumper, data):
    attributes = {
        'vid': data.vid,
        'description': data.description,
        'acls_in': data.acls_in,
        'faucet_mac': data.faucet_mac,
        'faucet_vips': data.faucet_vips,
        'routes': [{'route': {'ip_dst': route.ip_dst, 'ip_gw': route.ip_gw}} for route in data.routes],
        'acl_in': data.acl_in,
        'dot1x_assigned': data.dot1x_assigned,
        'max_hosts': data.max_hosts,
        'minimum_ip_size_check': data.minimum_ip_size_check,
        'name': data.name,
        'proactive_arp_limit': data.proactive_arp_limit,
        'proactive_nd_limit': data.proactive_nd_limit,
        'targeted_gw_resolution': data.targeted_gw_resolution,
        'unicast_flood': data.unicast_flood
    }
    
    # Filter out attributes with a value of None, 0, or False
    filtered_attributes = {k: v for k, v in attributes.items() if v not in (None, 0, False, [])}
    
    return dumper.represent_dict(filtered_attributes)

# Custom representer for Router objects
def router_representer(dumper, data):
    return dumper.represent_dict({
        'vlans': data.vlans,
        'vlan': data.bgp.vlan,
        'as_number': data.bgp.as_number,
        'port': data.bgp.port,
        'routerid': data.bgp.routerid,
        'server_addresses': data.bgp.server_addresses,
        'neighbor_addresses': data.bgp.neighbor_addresses,
        'neighbor_as': data.bgp.neighbor_as
    })


# Custom representer for Config objects
def config_representer(dumper, data):
    return dumper.represent_dict({
        'vlans': data.vlans,
        'routers': data.routers,
        'dps': data.dps
    })

# Custom representer for ACL objects
def acl_representer(dumper, data):
    rules = [{'rule': rule} for rule in data.rules]
    return dumper.represent_list(rules)

# Custom representer for Rule objects
def rule_representer(dumper, data):
    # Create a dictionary of attributes and their values
    attributes = {
        'actions': data.actions,
        'actset_output': getattr(data, 'actset_output', None),
        'arp_op': getattr(data, 'arp_op', None),
        'arp_sha': getattr(data, 'arp_sha', None),
        'arp_spa': getattr(data, 'arp_spa', None),
        'arp_tha': getattr(data, 'arp_tha', None),
        'arp_tpa': getattr(data, 'arp_tpa', None),
        'dl_dst': getattr(data, 'dl_dst', None),
        'dl_src': getattr(data, 'dl_src', None),
        'dl_type': getattr(data, 'dl_type', None),
        'eth_dst': getattr(data, 'eth_dst', None),
        'eth_src': getattr(data, 'eth_src', None),
        'eth_type': getattr(data, 'eth_type', None),
        'hard_timeout': getattr(data, 'hard_timeout', None),
        'icmp_code': getattr(data, 'icmp_code', None),
        'icmp_type': getattr(data, 'icmp_type', None),
        'idle_timeout': getattr(data, 'idle_timeout', None),
        'in_port': getattr(data, 'in_port', None),
        'ip_dscp': getattr(data, 'ip_dscp', None),
        'ip_ecn': getattr(data, 'ip_ecn', None),
        'ip_proto': getattr(data, 'ip_proto', None),
        'ipv4_dst': getattr(data, 'ipv4_dst', None),
        'ipv4_src': getattr(data, 'ipv4_src', None),
        'ipv6_dst': getattr(data, 'ipv6_dst', None),
        'ipv6_src': getattr(data, 'ipv6_src', None),
        'metadata': getattr(data, 'metadata', None),
        'mpls_label': getattr(data, 'mpls_label', None),
        'mpls_tc': getattr(data, 'mpls_tc', None),
        'mpls_bos': getattr(data, 'mpls_bos', None),
        'priority': getattr(data, 'priority', None),
        'table_id': getattr(data, 'table_id', None),
        'tcp_dst': getattr(data, 'tcp_dst', None),
        'tcp_src': getattr(data, 'tcp_src', None),
        'udp_dst': getattr(data, 'udp_dst', None),
        'udp_src': getattr(data, 'udp_src', None),
        'vlan_vid': getattr(data, 'vlan_vid', None),
        'vlan_pcp': getattr(data, 'vlan_pcp', None)
    }

    # Filter out attributes with None values
    filtered_attributes = {k: v for k, v in attributes.items() if v is not None}

    # Represent the filtered dictionary
    return dumper.represent_dict(filtered_attributes)

# Custom representer for Action objects
def action_representer(dumper, data):
    return dumper.represent_dict({
        'type': data.type,
        'params': data.params
    })

# Custom representer for OutputAction objects
def output_action_representer(dumper, data):
    return dumper.represent_dict({
        'port': data.port,
        'ports': data.ports,
        'pop_vlans': data.pop_vlans,
        'vlan_vid': data.vlan_vid,
        'swap_vid': data.swap_vid,
        'vlan_vids': data.vlan_vids,
        'failover': data.failover,
        'tunnel': data.tunnel
    })

# Custom representer for TunnelAction objects
def tunnel_action_representer(dumper, data):
    return dumper.represent_dict({
        'type': data.type,
        'tunnel_id': data.tunnel_id,
        'src_ip': data.src_ip,
        'dst_ip': data.dst_ip
    })

def meter_representer(dumper, data):
    # Create a dictionary representation of the Meter instance
    return dumper.represent_dict({
        'meter_id': data.meter_id,
        #'rate': data.rate,  # Include rate
        #'burst_size': data.burst_size,  # Include burst size
        'flags': data.flags,  # Include flags
        'bands': data.bands  # Assuming bands is already a list of dictionaries
    })


# Custom representer for DP objects
def dp_representer(dumper, data):
    # Retrieve all attributes of the DP object
    attributes = {attr: getattr(data, attr) for attr in dir(data) if not callable(getattr(data, attr)) and not attr.startswith("__")}

    # Filter out empty attributes
    filtered_attributes = {k: v for k, v in attributes.items() if v not in (None, '', [], {})}

    # Represent the filtered dictionary
    return dumper.represent_dict(filtered_attributes)


# Custom representer for Interface objects
def interface_representer(dumper, data):
    attributes = {
        'name': data.name,
        'acl_in': data.acl_in,
        'acls_in': data.acls_in,
        'description': data.description,
        'dot1x': data.dot1x,
        'dot1x_acl': data.dot1x_acl,
        'dot1x_mab': data.dot1x_mab,
        'enabled': data.enabled,
        'hairpin': data.hairpin,
        'loop_protect': data.loop_protect,
        'loop_protect_external': data.loop_protect_external,
        'max_hosts': data.max_hosts,
        'mirror': data.mirror,
        'native_vlan': data.native_vlan,
        'number': data.number,
        'opstatus_reconf': data.opstatus_reconf,
        'output_only': data.output_only,
        'permanent_learn': data.permanent_learn,
        'tagged_vlans': data.tagged_vlans,
        'unicast_flood': data.unicast_flood,
        'restricted_bcast_arpnd': data.restricted_bcast_arpnd,
        'lldp_beacon': data.lldp_beacon,
        'stack': data.stack
    }

    # Filter out empty attributes
    filtered_attributes = {k: v for k, v in attributes.items() if v not in (None, '', [], {})}

    # Represent the filtered dictionary
    return dumper.represent_dict(filtered_attributes)

# Register the custom representers with PyYAML
yaml.add_representer(Vlan, vlan_representer)
yaml.add_representer(Router, router_representer)
yaml.add_representer(Config, config_representer)
yaml.add_representer(ACL, acl_representer)
yaml.add_representer(Rule, rule_representer)
yaml.add_representer(Action, action_representer)
yaml.add_representer(OutputAction, output_action_representer)
yaml.add_representer(TunnelAction, tunnel_action_representer)
yaml.add_representer(DP, dp_representer)
yaml.add_representer(Interface, interface_representer)

# Register the custom representer with PyYAML
yaml.add_representer(Meter, meter_representer)

def save_config(config, yaml_file, save_vlans=True, save_routers=True, save_dps=True, save_acls=True, save_meters=True):
    # Create a dictionary to hold the parts of the configuration to save
    data_to_save = {}

    print('####config.routers')
    print(config.routers)
    
    if save_vlans:
        # Convert route dictionaries back into Route objects
        for vlan in config.vlans.values():
            vlan.routes = [Route(route['ip_dst'], route['ip_gw']) for route in vlan.routes]
        data_to_save['vlans'] = config.vlans
    if save_routers:
        data_to_save['routers'] = {}
        for name, route in config.routers.items():
            kconfig = {
                'vlans': route.vlans,
                'bgp': {
                    'as': route.bgp.as_number,
                    'connect_mode': route.bgp.connect_mode,  
                    'neighbor_as': route.bgp.neighbor_as,
                    'routerid': route.bgp.routerid,
                    'server_addresses': route.bgp.server_addresses,
                    'neighbor_addresses': route.bgp.neighbor_addresses,
                    'vlan': route.bgp.vlan,
                    'port': route.bgp.port,
                }
            }
            data_to_save['routers'][name] = kconfig
    if save_dps:
        data_to_save['dps'] = config.dps
    if save_acls:
        data_to_save['acls'] = config.acls
    if save_meters:
        data_to_save['meters'] = config.meters

    # Open the specified YAML file in write mode
    with open(yaml_file, 'w') as file:
        # Dump the selected parts of the configuration data to the YAML file
        yaml.dump(data_to_save, file)
