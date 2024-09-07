class Interface:
    def __init__(self, name, description, native_vlan, tagged_vlans=None, acls_in=None, **kwargs):
        self.name = name
        self.description = description
        self.native_vlan = native_vlan
        self.tagged_vlans = tagged_vlans if tagged_vlans is not None else []
        self.acls_in = acls_in if acls_in is not None else []
        self.acl_in = kwargs.get('acl_in', None)
        self.dot1x = kwargs.get('dot1x', None)
        self.dot1x_acl = kwargs.get('dot1x_acl', None)
        self.dot1x_mab = kwargs.get('dot1x_mab', None)
        self.enabled = kwargs.get('enabled', None)
        self.hairpin = kwargs.get('hairpin', None)
        self.lldp_beacon = kwargs.get('lldp_beacon', None)  # Set to None if not provided
        self.loop_protect = kwargs.get('loop_protect', None)
        self.loop_protect_external = kwargs.get('loop_protect_external', None)
        self.max_hosts = kwargs.get('max_hosts', None)
        self.mirror = kwargs.get('mirror', None)
        self.number = kwargs.get('number', None)
        self.opstatus_reconf = kwargs.get('opstatus_reconf', None)
        self.output_only = kwargs.get('output_only', None)
        self.permanent_learn = kwargs.get('permanent_learn', None)
        self.stack = kwargs.get('stack', None)
        self.unicast_flood = kwargs.get('unicast_flood', None)
        self.restricted_bcast_arpnd = kwargs.get('restricted_bcast_arpnd', None)
        self.coprocessor = kwargs.get('coprocessor', None)

        # LLDP Beacon attributes
        if self.lldp_beacon:
            print('self.lldp_beacon' + self.lldp_beacon)
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
        else:
            self.lldp_beacon_enable = None
            self.lldp_beacon_org_tlvs = []
            self.lldp_beacon_port_descr = None
            self.lldp_beacon_system_name = None

class DP:
    def __init__(self, dp_id, hardware, interfaces, **kwargs):
        self.dp_id = dp_id
        self.hardware = hardware
        self.interfaces = interfaces
        self.advertise_interval = kwargs.get('advertise_interval', None)
        self.arp_neighbor_timeout = kwargs.get('arp_neighbor_timeout', None)
        self.description = kwargs.get('description', None)
        self.dot1x = kwargs.get('dot1x', None)
        self.drop_broadcast_source_address = kwargs.get('drop_broadcast_source_address', None)
        self.drop_spoofed_faucet_mac = kwargs.get('drop_spoofed_faucet_mac', None)
        self.group_table = kwargs.get('group_table', None)
        self.high_priority = kwargs.get('high_priority', None)
        self.highest_priority = kwargs.get('highest_priority', None)
        self.ignore_learn_ins = kwargs.get('ignore_learn_ins', None)
        self.interface_ranges = kwargs.get('interface_ranges', None)
        self.learn_ban_timeout = kwargs.get('learn_ban_timeout', None)
        self.learn_jitter = kwargs.get('learn_jitter', None)
        self.lldp_beacon = kwargs.get('lldp_beacon', None)
        self.low_priority = kwargs.get('low_priority', None)
        self.lowest_priority = kwargs.get('lowest_priority', None)
        self.max_host_fib_retry_count = kwargs.get('max_host_fib_retry_count', None)
        self.max_hosts_per_resolve_cycle = kwargs.get('max_hosts_per_resolve_cycle', None)
        self.max_resolve_backoff_time = kwargs.get('max_resolve_backoff_time', None)
        self.metrics_rate_limit_sec = kwargs.get('metrics_rate_limit_sec', None)
        self.name = kwargs.get('name', None)
        self.ofchannel_log = kwargs.get('ofchannel_log', None)
        self.packetin_pps = kwargs.get('packetin_pps', None)
        self.slowpath_pps = kwargs.get('slowpath_pps', None)
        self.priority_offset = kwargs.get('priority_offset', None)
        self.proactive_learn_v4 = kwargs.get('proactive_learn_v4', None)
        self.proactive_learn_v6 = kwargs.get('proactive_learn_v6', None)
        self.stack = kwargs.get('stack', None)
        self.timeout = kwargs.get('timeout', None)
        self.use_idle_timeout = kwargs.get('use_idle_timeout', None)
        self.table_sizes = kwargs.get('table_sizes', None)
        self.port_table_scale_factor = kwargs.get('port_table_scale_factor', None)
        self.global_vlan = kwargs.get('global_vlan', None)

        # LLDP Beacon attributes
        self.lldp_beacon_system_name = self.lldp_beacon.get('system_name', None)
        self.lldp_beacon_send_interval = self.lldp_beacon.get('send_interval', None)
        self.lldp_beacon_max_per_interval = self.lldp_beacon.get('max_per_interval', None)

        # Stack attributes
        self.stack_priority = self.stack.get('priority', None)
        self.stack_down_time_multiple = self.stack.get('down_time_multiple', None)
        self.stack_min_stack_health = self.stack.get('min_stack_health', None)
        self.stack_min_lacp_health = self.stack.get('min_lacp_health', None)