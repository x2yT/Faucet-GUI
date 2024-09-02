import yaml
from models.vlan import Vlan
from models.router import Router
from models.dp import DP
from models.config import Config

# Custom representer for Vlan objects
def vlan_representer(dumper, data):
    return dumper.represent_dict({
        'vid': data.vid,
        'description': data.description,
        'acls_in': data.acls_in,
        'faucet_mac': data.faucet_mac,
        'faucet_vips': data.faucet_vips,
        'routes': data.routes,
        'acl_in': data.acl_in,
        'dot1x_assigned': data.dot1x_assigned,
        'max_hosts': data.max_hosts,
        'minimum_ip_size_check': data.minimum_ip_size_check,
        'name': data.name,
        'proactive_arp_limit': data.proactive_arp_limit,
        'proactive_nd_limit': data.proactive_nd_limit,
        'targeted_gw_resolution': data.targeted_gw_resolution,
        'unicast_flood': data.unicast_flood
    })

# Custom representer for Router objects
def router_representer(dumper, data):
    return dumper.represent_dict({
        'vlans': data.vlans
    })

# Custom representer for DP objects
def dp_representer(dumper, data):
    return dumper.represent_dict({
        'dp_id': data.dp_id,
        'hardware': data.hardware,
        'interfaces': data.interfaces
    })

# Custom representer for Config objects
def config_representer(dumper, data):
    return dumper.represent_dict({
        'vlans': data.vlans,
        'routers': data.routers,
        'dps': data.dps
    })

# Register the custom representers with PyYAML
yaml.add_representer(Vlan, vlan_representer)
yaml.add_representer(Router, router_representer)
yaml.add_representer(DP, dp_representer)
yaml.add_representer(Config, config_representer)

def save_config(config, yaml_file, save_vlans=True, save_routers=True, save_dps=True):
    # Create a dictionary to hold the parts of the configuration to save
    data_to_save = {}
    
    if save_vlans:
        data_to_save['vlans'] = config.vlans
    if save_routers:
        data_to_save['routers'] = config.routers
    if save_dps:
        data_to_save['dps'] = config.dps

    # Open the specified YAML file in write mode
    with open(yaml_file, 'w') as file:
        # Dump the selected parts of the configuration data to the YAML file
        yaml.dump(data_to_save, file)