class Route:
    def __init__(self, ip_dst, ip_gw):
        self.ip_dst = ip_dst
        self.ip_gw = ip_gw

class Vlan:
    def __init__(self, vid, description='', acls_in=None, faucet_mac='', faucet_vips=None, routes=None,
                 acl_in=None, dot1x_assigned=False, max_hosts=255, minimum_ip_size_check=True, name='',
                 proactive_arp_limit=2052, proactive_nd_limit=2052, targeted_gw_resolution=False, unicast_flood=True):
        self.vid = vid
        self.description = description
        self.acls_in = acls_in if acls_in is not None else []
        self.faucet_mac = faucet_mac
        self.faucet_vips = faucet_vips if faucet_vips is not None else []
        self.routes = routes if routes is not None else []
        self.acl_in = acl_in
        self.dot1x_assigned = dot1x_assigned
        self.max_hosts = max_hosts
        self.minimum_ip_size_check = minimum_ip_size_check
        self.name = name
        self.proactive_arp_limit = proactive_arp_limit
        self.proactive_nd_limit = proactive_nd_limit
        self.targeted_gw_resolution = targeted_gw_resolution
        self.unicast_flood = unicast_flood

class Vlans:
    def __init__(self, vlans_data):
        self.vlans = {}
        for vlan_name, vlan_info in vlans_data.items():
            self.vlans[vlan_name] = Vlan(
                vid=vlan_info.get('vid'),
                description=vlan_info.get('description'),
                acls_in=vlan_info.get('acls_in', []),
                faucet_mac=vlan_info.get('faucet_mac'),
                faucet_vips=vlan_info.get('faucet_vips', []),
                routes=vlan_info.get('routes', [])
            )

    def get_vlan(self, vlan_name):
        return self.vlans.get(vlan_name)

    def get_all_vlans(self):
        return self.vlans