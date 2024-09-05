class ACL:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

class Rule:
    def __init__(self, rule_data):
        # Check if rule_data contains a single key and extract the nested dictionary if necessary
        if len(rule_data) == 1 and 'rule' in rule_data:
            rule_data = rule_data['rule']

        # Print the rule_data dictionary to debug
        #print(f"Rule init rule_data type: {type(rule_data)}, content: {rule_data}")
        #print(f"rule_data: {rule_data}")
        for k, v in rule_data.items():
            print(f'k={k} v={v}')
        # Initialize attributes from the rule_data dictionary
        self.actset_output = rule_data.get('actset_output', None)
        self.arp_op = rule_data.get('arp_op', None)
        self.arp_sha = rule_data.get('arp_sha', None)
        self.arp_spa = rule_data.get('arp_spa', None)
        self.arp_tha = rule_data.get('arp_tha', None)
        self.arp_tpa = rule_data.get('arp_tpa', None)
        self.dl_dst = rule_data.get('dl_dst', None)
        self.dl_src = rule_data.get('dl_src', None)
        self.dl_type = rule_data.get('dl_type', None)
        self.dl_vlan = rule_data.get('dl_vlan', None)
        self.dl_vlan_pcp = rule_data.get('dl_vlan_pcp', None)
        self.eth_dst = rule_data.get('eth_dst', None)
        self.eth_src = rule_data.get('eth_src', None)
        self.eth_type = rule_data.get('eth_type', None)
        self.icmpv4_code = rule_data.get('icmpv4_code', None)
        self.icmpv4_type = rule_data.get('icmpv4_type', None)
        self.icmpv6_code = rule_data.get('icmpv6_code', None)
        self.icmpv6_type = rule_data.get('icmpv6_type', None)
        self.in_phy_port = rule_data.get('in_phy_port', None)
        self.in_port = rule_data.get('in_port', None)  
        self.ip_dscp = rule_data.get('ip_dscp', None)
        self.ip_ecn = rule_data.get('ip_ecn', None)
        self.ip_proto = rule_data.get('ip_proto', None)
        self.ipv4_dst = rule_data.get('ipv4_dst', None)
        self.ipv4_src = rule_data.get('ipv4_src', None)
        self.ipv6_dst = rule_data.get('ipv6_dst', None)
        self.ipv6_exthdr = rule_data.get('ipv6_exthdr', None)
        self.ipv6_flabel = rule_data.get('ipv6_flabel', None)
        self.ipv6_nd_sll = rule_data.get('ipv6_nd_sll', None)
        self.ipv6_nd_target = rule_data.get('ipv6_nd_target', None)
        self.ipv6_nd_tll = rule_data.get('ipv6_nd_tll', None)
        self.ipv6_src = rule_data.get('ipv6_src', None)
        self.metadata = rule_data.get('metadata', None)
        self.mpls_bos = rule_data.get('mpls_bos', None)
        self.mpls_label = rule_data.get('mpls_label', None)
        self.mpls_tc = rule_data.get('mpls_tc', None)
        self.nw_dst = rule_data.get('nw_dst', None)
        self.nw_proto = rule_data.get('nw_proto', None)
        self.nw_src = rule_data.get('nw_src', None)
        self.nw_tos = rule_data.get('nw_tos', None)
        self.packet_type = rule_data.get('packet_type', None)
        self.pbb_isid = rule_data.get('pbb_isid', None)
        self.pbb_uca = rule_data.get('pbb_uca', None)
        self.sctp_dst = rule_data.get('sctp_dst', None)
        self.sctp_src = rule_data.get('sctp_src', None)
        self.tcp_dst = rule_data.get('tcp_dst', None)
        self.tcp_flags = rule_data.get('tcp_flags', None)
        self.tcp_src = rule_data.get('tcp_src', None)
        self.tp_dst = rule_data.get('tp_dst', None)
        self.tp_src = rule_data.get('tp_src', None)
        self.tunnel_id = rule_data.get('tunnel_id', None)
        self.udp_dst = rule_data.get('udp_dst', None)
        self.udp_src = rule_data.get('udp_src', None)
        self.vlan_pcp = rule_data.get('vlan_pcp', None)
        self.vlan_vid = rule_data.get('vlan_vid', None)
        self.actions = rule_data.get('actions', {})
        
        # Print the contents of self.dl_type
        print(f"actions: {self.actions}")

class Action:
    def __init__(self, action_data):
        self.allow = action_data.get('allow', False)
        self.force_port_vlan = action_data.get('force_port_vlan', False)
        self.cookie = action_data.get('cookie', None)
        self.meter = action_data.get('meter', None)
        self.mirror = action_data.get('mirror', None)
        self.output = action_data.get('output', None)
        self.ct = action_data.get('ct', None)

class OutputAction:
    def __init__(self, output_data):
        self.set_fields = output_data.get('set_fields', [])
        self.port = output_data.get('port', None)
        self.ports = output_data.get('ports', [])
        self.pop_vlans = output_data.get('pop_vlans', False)
        self.vlan_vid = output_data.get('vlan_vid', None)
        self.swap_vid = output_data.get('swap_vid', None)
        self.vlan_vids = output_data.get('vlan_vids', [])
        self.failover = output_data.get('failover', None)
        self.tunnel = output_data.get('tunnel', None)

class TunnelAction:
    def __init__(self, tunnel_data):
        self.type = tunnel_data.get('type', 'vlan')
        self.tunnel_id = tunnel_data.get('tunnel_id', None)
        self.dp = tunnel_data.get('dp', None)
        self.port = tunnel_data.get('port', None)
        self.exit_instructions = tunnel_data.get('exit_instructions', [])
        self.maintain_encapsulation = tunnel_data.get('maintain_encapsulation', False)
        self.bi_directional = tunnel_data.get('bi_directional', False)
        self.reverse = tunnel_data.get('reverse', False)