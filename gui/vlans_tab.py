# vlans_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, q
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

def create_vlans_tab(config):
    vlans_tab = QWidget()
    vlans_layout = QVBoxLayout()
    for name, vlan in config.vlans.items():
        vlan_group = QWidget()
        vlan_layout = QGridLayout()
        #vlan_layout.addWidget(QLabel(f"VLAN Name: {name}"))
        
        vlan_name_edit = QLineEdit(name)
        vlan_layout.addWidget(QLabel("VLAN Name:"))
        vlan_layout.addWidget(vlan_name_edit)

        vlan_layout.addWidget(QLabel(f"VID: {vlan.vid}"))
        vlan_layout.addWidget(QLabel(f"Description: {vlan.description}"))
        vlan_layout.addWidget(QLabel(f"ACLs In: {', '.join(vlan.acls_in)}"))
        vlan_layout.addWidget(QLabel(f"Faucet MAC: {vlan.faucet_mac}"))
        vlan_layout.addWidget(QLabel(f"Faucet VIPs: {', '.join(vlan.faucet_vips)}"))
        vlan_layout.addWidget(QLabel(f"ACL In: {vlan.acl_in}"))
        vlan_layout.addWidget(QLabel(f"Dot1x Assigned: {vlan.dot1x_assigned}"))
        vlan_layout.addWidget(QLabel(f"Max Hosts: {vlan.max_hosts}"))
        vlan_layout.addWidget(QLabel(f"Minimum IP Size Check: {vlan.minimum_ip_size_check}"))
        vlan_layout.addWidget(QLabel(f"Name: {vlan.name}"))
        vlan_layout.addWidget(QLabel(f"Proactive ARP Limit: {vlan.proactive_arp_limit}"))
        vlan_layout.addWidget(QLabel(f"Proactive ND Limit: {vlan.proactive_nd_limit}"))
        vlan_layout.addWidget(QLabel(f"Targeted GW Resolution: {vlan.targeted_gw_resolution}"))
        vlan_layout.addWidget(QLabel(f"Unicast Flood: {vlan.unicast_flood}"))

        routes_label = QLabel("Routes:")
        vlan_layout.addWidget(routes_label)
        for route in vlan.routes:
            vlan_layout.addWidget(QLabel(f"  - Destination: {route['ip_dst']}, Gateway: {route['ip_gw']}"))

        vlan_group.setLayout(vlan_layout)
        vlans_layout.addWidget(vlan_group)

    vlans_tab.setLayout(vlans_layout)
    return vlans_tab