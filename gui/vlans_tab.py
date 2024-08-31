# vlans_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

def create_vlans_tab(config):
    vlans_tab = QWidget()
    vlans_layout = QVBoxLayout()
    for name, vlan in config.vlans.items():
        vlan_group = QWidget()
        vlan_groupbox = QGroupBox(name)
        vlan_layout = QFormLayout()
        vlan_groupbox.setLayout(vlan_layout)
        #vlan_layout.addWidget(QLabel(f"VLAN Name: {name}"))
        
        #vlan_name_edit = QLineEdit(name)
        ##vlan_layout.addWidget(QLabel("VLAN Name:"))
        #vlan_layout.addWidget(vlan_name_edit)
    
        vlan_layout.addRow("VID:", QLineEdit(str(vlan.vid), vlan_groupbox))
        vlan_layout.addRow("Description:", QLineEdit(vlan.description, vlan_groupbox))
        vlan_layout.addRow("ACLs In:", QLineEdit(', '.join(vlan.acls_in), vlan_groupbox))
        vlan_layout.addRow("Faucet MAC:", QLineEdit(vlan.faucet_mac, vlan_groupbox))
        vlan_layout.addRow("Faucet VIPs:", QLineEdit(', '.join(vlan.faucet_vips), vlan_groupbox))
        vlan_layout.addRow("ACL In:", QLineEdit(vlan.acl_in, vlan_groupbox))
        vlan_layout.addRow("Dot1x Assigned:", QLineEdit(str(vlan.dot1x_assigned), vlan_groupbox))  # Convert bool to str
        vlan_layout.addRow("Max Hosts:", QLineEdit(str(vlan.max_hosts), vlan_groupbox))
        vlan_layout.addRow("Minimum IP Size Check:", QLineEdit(str(vlan.minimum_ip_size_check), vlan_groupbox))
        vlan_layout.addRow("Name:", QLineEdit(vlan.name, vlan_groupbox))
        vlan_layout.addRow("Proactive ARP Limit:", QLineEdit(str(vlan.proactive_arp_limit), vlan_groupbox))
        vlan_layout.addRow("Proactive ND Limit:", QLineEdit(str(vlan.proactive_nd_limit), vlan_groupbox))
        vlan_layout.addRow("Targeted GW Resolution:", QLineEdit(str(vlan.targeted_gw_resolution), vlan_groupbox))  # Convert bool to str
        vlan_layout.addRow("Unicast Flood:", QLineEdit(str(vlan.unicast_flood), vlan_groupbox))  # Convert bool to str

        routes_label = QLabel("Routes:")
        vlan_layout.addRow(routes_label)
        for route in vlan.routes:
            vlan_layout.addRow(QLabel(f"  - Destination: {route['ip_dst']}, Gateway: {route['ip_gw']}"))

        #vlan_group.setLayout(vlan_layout)
        vlans_layout.addWidget(vlan_groupbox)

    vlans_tab.setLayout(vlans_layout)
    return vlans_tab