# vlans_tab.py

from PyQt6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox

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
        
        # Add a QCheckBox for dot1x_assigned
        vlan_layout.addWidget(QLabel("Dot1x Assigned:"), row, 0)
        dot1x_checkbox = QCheckBox(vlan_groupbox)
        dot1x_checkbox.setChecked(vlan.dot1x_assigned)
        vlan_layout.addWidget(dot1x_checkbox, row, 1)
        row += 1
        
        # Add Faucet VIPs and Faucet MAC 
        vlan_layout.addWidget(QLabel("Faucet VIPs:"), row, 0)
        vlan_layout.addWidget(QLineEdit(', '.join(vlan.faucet_vips), vlan_groupbox), row, 1, 1, 3)
        row += 1
        vlan_layout.addWidget(QLabel("Faucet MAC:"), row, 0)
        vlan_layout.addWidget(QLineEdit(vlan.faucet_mac, vlan_groupbox), row, 1, 1, 3)
        row += 1
        
        # Add a QSpinBox for max_hosts
        vlan_layout.addWidget(QLabel("Max Hosts:"), row, 0)
        max_hosts_spinbox = QSpinBox(vlan_groupbox)
        max_hosts_spinbox.setRange(0, 9999)
        max_hosts_spinbox.setValue(vlan.max_hosts)
        max_hosts_spinbox.setFixedWidth(90)  # Set fixed width to accommodate 4 digits
        vlan_layout.addWidget(max_hosts_spinbox, row, 1)
        row += 1
        
        # Add a QCheckBox for minimum_ip_size_check
        vlan_layout.addWidget(QLabel("Minimum IP Size Check:"), row, 0)
        minimum_ip_size_check_checkbox = QCheckBox(vlan_groupbox)
        minimum_ip_size_check_checkbox.setChecked(vlan.minimum_ip_size_check)
        vlan_layout.addWidget(minimum_ip_size_check_checkbox, row, 1)
        row += 1        
       
        # Add Proactive ARP Limit and Proactive ND Limit on the same row
        # Add a QSpinBox for proactive_arp_limit
        vlan_layout.addWidget(QLabel("Proactive ARP Limit:"), row, 0)
        proactive_arp_limit_spinbox = QSpinBox(vlan_groupbox)
        proactive_arp_limit_spinbox.setRange(0, 9999)
        proactive_arp_limit_spinbox.setValue(vlan.proactive_arp_limit)
        proactive_arp_limit_spinbox.setFixedWidth(90)  # Set fixed width to accommodate 4 digits
        vlan_layout.addWidget(proactive_arp_limit_spinbox, row, 1)
        # Add a QSpinBox for proactive_nd_limit
        vlan_layout.addWidget(QLabel("Proactive ND Limit:"), row, 2)
        proactive_nd_limit_spinbox = QSpinBox(vlan_groupbox)
        proactive_nd_limit_spinbox.setRange(0, 9999)
        proactive_nd_limit_spinbox.setValue(vlan.proactive_nd_limit)
        proactive_nd_limit_spinbox.setFixedWidth(90)  # Set fixed width to accommodate 4 digits
        vlan_layout.addWidget(proactive_nd_limit_spinbox, row, 3)
        row += 1
        
        # Add a QCheckBox for targeted_gw_resolution
        vlan_layout.addWidget(QLabel("Targeted GW Resolution:"), row, 0)
        targeted_gw_resolution_checkbox = QCheckBox(vlan_groupbox)
        targeted_gw_resolution_checkbox.setChecked(vlan.targeted_gw_resolution)
        vlan_layout.addWidget(targeted_gw_resolution_checkbox, row, 1)
        row += 1

        # Add a QCheckBox for minimum_ip_size_check
        vlan_layout.addWidget(QLabel("Unicast Flood:"), row, 0)
        unicast_flood_checkbox = QCheckBox(vlan_groupbox)
        unicast_flood_checkbox.setChecked(vlan.unicast_flood)
        vlan_layout.addWidget(unicast_flood_checkbox, row, 1)
        row += 1
        
        # Add a QSpinBox for vid
        vlan_layout.addWidget(QLabel("VID:"), row, 0)
        vid_spinbox = QSpinBox(vlan_groupbox)
        vid_spinbox.setRange(0, 9999)
        vid_spinbox.setValue(vlan.vid)
        vid_spinbox.setFixedWidth(90)  # Set fixed width to accommodate 4 digits
        vlan_layout.addWidget(vid_spinbox, row, 1)
        row += 1

        # Add Static Routes group box
        routes_groupbox = QGroupBox("Static Routes", vlan_groupbox)
        routes_layout = QGridLayout()
        routes_groupbox.setLayout(routes_layout)
        
        route_row = 0  # Initialize route row counter
        for route in vlan.routes:
            routes_layout.addWidget(QLabel(f"Destination:"), route_row, 0)
            routes_layout.addWidget(QLineEdit(route['ip_dst'], routes_groupbox), route_row, 1)
            routes_layout.addWidget(QLabel(f"Gateway:"), route_row, 2)
            routes_layout.addWidget(QLineEdit(route['ip_gw'], routes_groupbox), route_row, 3)
            route_row += 1
        
        vlan_layout.addWidget(routes_groupbox, row, 0, 1, 4)
        row += 1

        # Add the group box to the main layout
        vlans_layout.addWidget(vlan_groupbox)

    # Set the layout for the VLANs tab
    vlans_tab.setLayout(vlans_layout)

    # Return the configured VLANs tab
    return vlans_tab