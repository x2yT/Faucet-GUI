# vlans_tab.py

from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout

def create_vlans_tab(config):
    vlans_tab = QWidget()
    vlans_layout = QVBoxLayout()

    # Create a new Groupbox for each VLAN
    for name, vlan in config.vlans.items():
        
        vlan_group = QWidget()
        # Create a QGroupBox with the VLAN name
        vlan_groupbox = QGroupBox(name)
        
        # Create a QGridLayout for the VLAN details
        vlan_layout = QGridLayout()
        
        # Set the layout for the group box
        vlan_groupbox.setLayout(vlan_layout)
        
        row = 0  # Initialize row counter
        
        # Function to create a QLineEdit with fixed width
        def create_line_edit(text, parent, width=200):
            line_edit = QLineEdit(text, parent)
            line_edit.setFixedWidth(width)  # Set fixed width
            return line_edit
        
        # Check if acl_in is present and add it to the form if it has data
        if vlan.acl_in:
            # acl_in is deprecated, only show it if the file we read from has a value in it
            vlan_layout.addWidget(QLabel("ACL In:"), row, 0)
            vlan_layout.addWidget(QLineEdit(vlan.acl_in, vlan_groupbox), row, 1)
            row += 1
        
        # Add other VLAN details to the form
        vlan_layout.addWidget(QLabel("ACLs In:"), row, 0)
        vlan_layout.addWidget(create_line_edit(', '.join(vlan.acls_in), vlan_groupbox), row, 1)
        row += 1
        
        vlan_layout.addWidget(QLabel("Description:"), row, 0)
        vlan_layout.addWidget(QLineEdit(vlan.description, vlan_groupbox), row, 1, 1, 3)
        row += 1
        
        vlan_layout.addWidget(QLabel("Dot1x Assigned:"), row, 0)
        vlan_layout.addWidget(QLineEdit(str(vlan.dot1x_assigned), vlan_groupbox), row, 1)  # Convert bool to str
        row += 1
        
        # Add Faucet VIPs and Faucet MAC on the same row
        vlan_layout.addWidget(QLabel("Faucet VIPs:"), row, 0)
        vlan_layout.addWidget(QLineEdit(', '.join(vlan.faucet_vips), vlan_groupbox), row, 1)
        vlan_layout.addWidget(QLabel("Faucet MAC:"), row, 2)
        vlan_layout.addWidget(QLineEdit(vlan.faucet_mac, vlan_groupbox), row, 3)
        row += 1
        
        # vlan_layout.addWidget(QLabel("Max Hosts:"), row, 0)
        # vlan_layout.addWidget(QLineEdit(str(vlan.max_hosts), vlan_groupbox), row, 1)
        # row += 1

        vlan_layout.addWidget(QLabel("Max Hosts:"), row, 0)
        vlan_layout.addWidget(create_line_edit(str(vlan.max_hosts), vlan_groupbox, 100), row, 1)
        row += 1
        
        vlan_layout.addWidget(QLabel("Minimum IP Size Check:"), row, 0)
        vlan_layout.addWidget(create_line_edit(str(vlan.minimum_ip_size_check), vlan_groupbox, 100), row, 1)
        row += 1
        
        # vlan_layout.addWidget(QLabel("Name:"), row, 0)
        # vlan_layout.addWidget(QLineEdit(vlan.name, vlan_groupbox), row, 1)
        # row += 1
        
        # Add Proactive ARP Limit and Proactive ND Limit on the same row
        vlan_layout.addWidget(QLabel("Proactive ARP Limit:"), row, 0)
        vlan_layout.addWidget(create_line_edit(str(vlan.proactive_arp_limit), vlan_groupbox, 100), row, 1)
        vlan_layout.addWidget(QLabel("Proactive ND Limit:"), row, 2)
        vlan_layout.addWidget(create_line_edit(str(vlan.proactive_nd_limit), vlan_groupbox, 100), row, 3)
        row += 1
        
        vlan_layout.addWidget(QLabel("Targeted GW Resolution:"), row, 0)
        vlan_layout.addWidget(QLineEdit(str(vlan.targeted_gw_resolution), vlan_groupbox), row, 1)  # Convert bool to str
        row += 1
        
        vlan_layout.addWidget(QLabel("Unicast Flood:"), row, 0)
        vlan_layout.addWidget(create_line_edit(str(vlan.unicast_flood), vlan_groupbox, 100), row, 1)  # Convert bool to str
        row += 1
        
        vlan_layout.addWidget(QLabel("VID:"), row, 0)
        vlan_layout.addWidget(create_line_edit(str(vlan.vid), vlan_groupbox, 100), row, 1)
        row += 1

        # Add static routes to the form
        routes_label = QLabel("Static Routes:")
        vlan_layout.addWidget(routes_label, row, 0, 1, 2)
        row += 1
        for route in vlan.routes:
            vlan_layout.addWidget(QLabel(f"  - Destination: {route['ip_dst']}, Gateway: {route['ip_gw']}"), row, 0, 1, 2)
            row += 1

        # Add the group box to the main layout
        vlans_layout.addWidget(vlan_groupbox)

    # Set the layout for the VLANs tab
    vlans_tab.setLayout(vlans_layout)

    # Return the configured VLANs tab
    return vlans_tab

# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QGroupBox, QFormLayout, QLabel, QLineEdit
# from PyQt6.QtGui import QIcon
# from PyQt6.QtCore import Qt

# def create_vlans_tab(config):
#     vlans_tab = QWidget()
#     vlans_layout = QVBoxLayout()

#     # Create a new Groupbox for each VLAN
#     for name, vlan in config.vlans.items():
        
#         vlan_group = QWidget()
#         # Create a QGroupBox with the VLAN name
#         vlan_groupbox = QGroupBox(name)
        
#         # Create a QFormLayout for the VLAN details
#         vlan_layout = QFormLayout()
        
#         # Set the layout for the group box
#         vlan_groupbox.setLayout(vlan_layout)
        
#         # Check if acl_in is present and add it to the form if it has data
#         if vlan.acl_in:
#             # acl_in is deprecated, only show it if the file we read from has a value in it
#             vlan_layout.addRow("ACL In:", QLineEdit(vlan.acl_in, vlan_groupbox))
        
#         # Add other VLAN details to the form
#         vlan_layout.addRow("ACLs In:", QLineEdit(', '.join(vlan.acls_in), vlan_groupbox))
#         vlan_layout.addRow("Description:", QLineEdit(vlan.description, vlan_groupbox))
#         vlan_layout.addRow("Dot1x Assigned:", QLineEdit(str(vlan.dot1x_assigned), vlan_groupbox))  # Convert bool to str

#         vlan_layout.addRow("Faucet VIPs:", QLineEdit(', '.join(vlan.faucet_vips), vlan_groupbox))
#         vlan_layout.addRow("Faucet MAC:", QLineEdit(vlan.faucet_mac, vlan_groupbox))


#         vlan_layout.addRow("Max Hosts:", QLineEdit(str(vlan.max_hosts), vlan_groupbox))
#         vlan_layout.addRow("Minimum IP Size Check:", QLineEdit(str(vlan.minimum_ip_size_check), vlan_groupbox))
#         #vlan_layout.addRow("Name:", QLineEdit(vlan.name, vlan_groupbox))
#         vlan_layout.addRow("Proactive ARP Limit:", QLineEdit(str(vlan.proactive_arp_limit), vlan_groupbox))
#         vlan_layout.addRow("Proactive ND Limit:", QLineEdit(str(vlan.proactive_nd_limit), vlan_groupbox))
#         vlan_layout.addRow("Targeted GW Resolution:", QLineEdit(str(vlan.targeted_gw_resolution), vlan_groupbox))  # Convert bool to str
#         vlan_layout.addRow("Unicast Flood:", QLineEdit(str(vlan.unicast_flood), vlan_groupbox))  # Convert bool to str
#         vlan_layout.addRow("VID:", QLineEdit(str(vlan.vid), vlan_groupbox))

#         # Add static routes to the form
#         routes_label = QLabel("Static Routes:")
#         vlan_layout.addRow(routes_label)
#         for route in vlan.routes:
#             vlan_layout.addRow(QLabel(f"  - Destination: {route['ip_dst']}, Gateway: {route['ip_gw']}"))

#         # Add the group box to the main layout
#         vlans_layout.addWidget(vlan_groupbox)

#     # Set the layout for the VLANs tab
#     vlans_tab.setLayout(vlans_layout)

#     # Return the configured VLANs tab
#     return vlans_tab