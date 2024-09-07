class Interface:
    def __init__(self, name, description, native_vlan, tagged_vlans=None, acls_in=None, **kwargs):
        self.name = name
        self.description = description
        self.native_vlan = native_vlan
        self.tagged_vlans = tagged_vlans if tagged_vlans is not None else []
        self.acls_in = acls_in if acls_in is not None else []
        self.acl_in = kwargs.get('acl_in')
        self.dot1x = kwargs.get('dot1x')
        self.dot1x_acl = kwargs.get('dot1x_acl')
        self.dot1x_mab = kwargs.get('dot1x_mab')
        self.enabled = kwargs.get('enabled')
        self.hairpin = kwargs.get('hairpin')
        self.lldp_beacon = kwargs.get('lldp_beacon', {})
        self.loop_protect = kwargs.get('loop_protect')
        self.loop_protect_external = kwargs.get('loop_protect_external')
        self.max_hosts = kwargs.get('max_hosts')
        self.mirror = kwargs.get('mirror', [])
        self.number = kwargs.get('number')
        self.opstatus_reconf = kwargs.get('opstatus_reconf')
        self.output_only = kwargs.get('output_only')
        self.permanent_learn = kwargs.get('permanent_learn')
        self.stack = kwargs.get('stack', {})
        self.unicast_flood = kwargs.get('unicast_flood')
        self.restricted_bcast_arpnd = kwargs.get('restricted_bcast_arpnd')
        self.coprocessor = kwargs.get('coprocessor')

        # LLDP Beacon attributes
        self.lldp_beacon_enable = self.lldp_beacon.get('enable')
        self.lldp_beacon_org_tlvs = [
            {
                'info': tlv.get('info'),
                'oui': tlv.get('oui'),
                'subtype': tlv.get('subtype')
            } for tlv in self.lldp_beacon.get('org_tlvs', [])
        ]
        self.lldp_beacon_port_descr = self.lldp_beacon.get('port_descr')
        self.lldp_beacon_system_name = self.lldp_beacon.get('system_name')

        # Stack attributes
        self.stack_dp = self.stack.get('dp')
        self.stack_port = self.stack.get('port')

class DP:
    def __init__(self, dp_id, hardware, interfaces, **kwargs):
        self.dp_id = dp_id
        self.hardware = hardware
        self.interfaces = interfaces
        self.advertise_interval = kwargs.get('advertise_interval')
        self.arp_neighbor_timeout = kwargs.get('arp_neighbor_timeout')
        self.description = kwargs.get('description')
        self.dot1x = kwargs.get('dot1x')
        self.drop_broadcast_source_address = kwargs.get('drop_broadcast_source_address')
        self.drop_spoofed_faucet_mac = kwargs.get('drop_spoofed_faucet_mac')
        self.group_table = kwargs.get('group_table')
        self.high_priority = kwargs.get('high_priority')
        self.highest_priority = kwargs.get('highest_priority')
        self.ignore_learn_ins = kwargs.get('ignore_learn_ins')
        self.interface_ranges = kwargs.get('interface_ranges')
        self.learn_ban_timeout = kwargs.get('learn_ban_timeout')
        self.learn_jitter = kwargs.get('learn_jitter')
        self.lldp_beacon = kwargs.get('lldp_beacon', {})
        self.low_priority = kwargs.get('low_priority')
        self.lowest_priority = kwargs.get('lowest_priority')
        self.max_host_fib_retry_count = kwargs.get('max_host_fib_retry_count')
        self.max_hosts_per_resolve_cycle = kwargs.get('max_hosts_per_resolve_cycle')
        self.max_resolve_backoff_time = kwargs.get('max_resolve_backoff_time')
        self.metrics_rate_limit_sec = kwargs.get('metrics_rate_limit_sec')
        self.name = kwargs.get('name')
        self.ofchannel_log = kwargs.get('ofchannel_log')
        self.packetin_pps = kwargs.get('packetin_pps')
        self.slowpath_pps = kwargs.get('slowpath_pps')
        self.priority_offset = kwargs.get('priority_offset')
        self.proactive_learn_v4 = kwargs.get('proactive_learn_v4')
        self.proactive_learn_v6 = kwargs.get('proactive_learn_v6')
        self.stack = kwargs.get('stack', {})
        self.timeout = kwargs.get('timeout')
        self.use_idle_timeout = kwargs.get('use_idle_timeout')
        self.table_sizes = kwargs.get('table_sizes')
        self.port_table_scale_factor = kwargs.get('port_table_scale_factor')
        self.global_vlan = kwargs.get('global_vlan')

        # LLDP Beacon attributes
        self.lldp_beacon_system_name = self.lldp_beacon.get('system_name')
        self.lldp_beacon_send_interval = self.lldp_beacon.get('send_interval')
        self.lldp_beacon_max_per_interval = self.lldp_beacon.get('max_per_interval')

        # Stack attributes
        self.stack_priority = self.stack.get('priority')
        self.stack_down_time_multiple = self.stack.get('down_time_multiple')
        self.stack_min_stack_health = self.stack.get('min_stack_health')
        self.stack_min_lacp_health = self.stack.get('min_lacp_health')