# vlans_tab.py

from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QSizePolicy
from configfile.loader import new_config, Vlan  # Assuming new_config is imported from loader.py
import globals

# Define a dialog class for adding routes
class AddRouteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Route")
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.addStretch(1)
        
        # Input fields for ip_dst and ip_gw
        self.ip_dst_edit = QLineEdit(self)
        self.ip_gw_edit = QLineEdit(self)
        
        layout.addWidget(QLabel("Destination IP:"))
        layout.addWidget(self.ip_dst_edit)
        layout.addWidget(QLabel("Gateway IP:"))
        layout.addWidget(self.ip_gw_edit)
        
        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        cancel_button = QPushButton("Cancel", self)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect buttons to their respective slots
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
    def get_values(self):
        return self.ip_dst_edit.text(), self.ip_gw_edit.text()
    
# Function to add a new route
def add_route(config, routes_groupbox, vlan_name):
    # Check the vlan exists
    vlan = config.vlans.get(vlan_name)
    if vlan is None:
        print(f"VLAN {vlan_name} not found in config.")
        return
    
    dialog = AddRouteDialog(routes_groupbox)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print('accepted')
        ip_dst, ip_gw = dialog.get_values()
        if ip_dst and ip_gw:
            print('ip_dst=' + ip_dst)   
            
            # Ensure vlan.routes is initialized
            if not hasattr(vlan, 'routes'):
                vlan.routes = []
            
            print(*vlan.routes, sep=", ")
            # Add the new route to the VLAN's routes
            vlan.routes.append({'ip_dst': ip_dst, 'ip_gw': ip_gw})
            print(*vlan.routes, sep=", ")

            # Update the routes_groupbox UI
            route_row = routes_groupbox.layout().rowCount()
            routes_groupbox.layout().addWidget(QLabel(f"Destination:"), route_row, 0)
            routes_groupbox.layout().addWidget(QLineEdit(ip_dst, routes_groupbox), route_row, 1)
            routes_groupbox.layout().addWidget(QLabel(f"Gateway:"), route_row, 2)
            routes_groupbox.layout().addWidget(QLineEdit(ip_gw, routes_groupbox), route_row, 3)
#________________________________________________________________________________________________

# Function to refresh the VLAN tab
def refresh_vlans_tab(config, vlans_layout, scroll_area):
    # Clear the existing layout
    for i in reversed(range(vlans_layout.count())):
        widget = vlans_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    # Recreate the VLAN tab
    create_vlans_tab(config, vlans_layout, scroll_area)

# Create the VLAN tab
def create_vlans_tab(config, vlans_layout=None, scroll_area=None):

    if vlans_layout is None:
        vlans_tab = QWidget()
        vlans_layout = QVBoxLayout()
        vlans_layout.addStretch(1)
        vlans_tab.setLayout(vlans_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(vlans_tab)
    else:
        vlans_tab = vlans_layout.parentWidget()

    # Button to add a new VLAN
    add_vlan_button = QPushButton("Add VLAN")
    vlans_layout.addWidget(add_vlan_button)
    # Slot function to add a new VLAN
    def add_vlan():
        # Create a new VLAN object with initial values
        new_vlan_name = "New VLAN"
        new_vlan = Vlan(
            vid=1,
            description='Default VLAN',
            acls_in=[],
            faucet_mac='',
            faucet_vips=[],
            routes=[],
            acl_in=None,
            dot1x_assigned=False,
            max_hosts=255,
            minimum_ip_size_check=True,
            name='default',
            proactive_arp_limit=2052,
            proactive_nd_limit=2052,
            targeted_gw_resolution=False,
            unicast_flood=True
        )
        config.vlans[new_vlan_name] = new_vlan
        # Refresh the VLAN tab
        refresh_vlans_tab(config, vlans_layout, scroll_area)
        # Scroll to the bottom
        scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())
        globals.unsaved_changes = True  # Mark as unsaved changes
    # Connect the button click to the add_vlan slot
    add_vlan_button.clicked.connect(add_vlan)

    # This function is used by the New Route dialog to reference the config for the data dictionary
    def create_add_route_handler(vlan_name, routes_groupbox):
        print('vlan_name='+ vlan_name)
        return lambda: add_route(config, routes_groupbox, vlan_name)
    # Slot function to update the VLAN key name
    def update_vlan_name(old_name, new_name, vlan_groupbox):
        if new_name and new_name != old_name:
            # Update the key in the config.vlans dictionary
            config.vlans[new_name] = config.vlans.pop(old_name)
            # Update the QGroupBox title
            vlan_groupbox.setTitle(new_name)
            globals.unsaved_changes = True  # Mark as unsaved changes

    # Create a new Groupbox for each VLAN
    for name, vlan in config.vlans.items():
        
        vlan_group = QWidget()
        # Create a QGroupBox with the VLAN name
        vlan_groupbox = QGroupBox(name)        
        # Set the font size and weight for the QGroupBox title
        vlan_groupbox.setStyleSheet("QGroupBox { font-size: 12pt; font-weight: bold; }")
        # Set the size policy to expanding
        vlan_groupbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        vlan_groupbox.setMinimumWidth(810) 

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

        # Add a QLineEdit for the VLAN name
        vlan_layout.addWidget(QLabel("VLAN Name:"), row, 0)
        vlan_name_edit = create_line_edit(name, vlan_groupbox)
        vlan_layout.addWidget(vlan_name_edit, row, 1)
        row += 1
        # Connect the editingFinished signal to the update_vlan_name slot
        vlan_name_edit.editingFinished.connect(lambda old_name=name, edit=vlan_name_edit, groupbox=vlan_groupbox: update_vlan_name(old_name, edit.text(), groupbox))

        
        # Check if acl_in is present and add it to the form if it has data
        if vlan.acl_in:
            # acl_in is deprecated, only show it if the file we read from has a value in it
            vlan_layout.addWidget(QLabel("ACL In:"), row, 0)
            vlan_layout.addWidget(QLineEdit(vlan.acl_in, vlan_groupbox), row, 1)
            row += 1
        
        # Add other VLAN details to the form

        vlan_layout.addWidget(QLabel("ACLs In:"), row, 0)
        acls_in_edit = create_line_edit(', '.join(vlan.acls_in), vlan_groupbox)
        vlan_layout.addWidget(acls_in_edit, row, 1)
        row += 1
        # Slot function to update user changes back to vlan.acls_in
        def update_acls_in(text):
            vlan.acls_in = text.split(', ')
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the textChanged signal to the slot function
        acls_in_edit.textChanged.connect(update_acls_in)

        vlan_layout.addWidget(QLabel("Description:"), row, 0)
        description_edit = QLineEdit(vlan.description, vlan_groupbox)
        vlan_layout.addWidget(description_edit, row, 1, 1, 3)
        row += 1
        # Slot function to update vlan.acls_in with the description
        def update_description(text):
            vlan.description = [text]
            globals.unsaved_changes = True  # Mark as unsaved changes
            print("Unsaved Changed=" + str(globals.unsaved_changes))
        description_edit.textChanged.connect(update_description)
        
        # Add a QCheckBox for dot1x_assigned
        vlan_layout.addWidget(QLabel("Dot1x Assigned:"), row, 0)
        dot1x_checkbox = QCheckBox(vlan_groupbox)
        dot1x_checkbox.setChecked(vlan.dot1x_assigned)
        vlan_layout.addWidget(dot1x_checkbox, row, 1)
        row += 1
        # Slot function to update vlan.dot1x_assigned
        def update_dot1x_assigned(state):
            vlan.dot1x_assigned = bool(state)
            globals.unsaved_changes = True  # Mark as unsaved changes
            print('dot1x=' + str(vlan.dot1x_assigned))
        # Connect the stateChanged signal to the slot function
        dot1x_checkbox.stateChanged.connect(update_dot1x_assigned)
        
        # Add Faucet VIPs and Faucet MAC 
        vlan_layout.addWidget(QLabel("Faucet VIPs:"), row, 0)
        faucet_vips_edit = QLineEdit(', '.join(vlan.faucet_vips), vlan_groupbox)
        vlan_layout.addWidget(faucet_vips_edit, row, 1, 1, 3)
        row += 1
        #
        vlan_layout.addWidget(QLabel("Faucet MAC:"), row, 0)
        faucet_mac_edit = QLineEdit(vlan.faucet_mac, vlan_groupbox)
        vlan_layout.addWidget(faucet_mac_edit, row, 1, 1, 3)
        row += 1
        # Slot function to update vlan.faucet_vips
        def update_faucet_vips(text):
            vlan.faucet_vips = text.split(', ')
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Slot function to update vlan.faucet_mac
        def update_faucet_mac(text):
            vlan.faucet_mac = text
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the textChanged signals to the slot functions
        faucet_vips_edit.textChanged.connect(update_faucet_vips)
        faucet_mac_edit.textChanged.connect(update_faucet_mac)
        
        # Add a QSpinBox for max_hosts
        vlan_layout.addWidget(QLabel("Max Hosts:"), row, 0)
        max_hosts_spinbox = QSpinBox(vlan_groupbox)
        max_hosts_spinbox.setRange(0, 9999)
        max_hosts_spinbox.setValue(vlan.max_hosts)
        max_hosts_spinbox.setFixedWidth(90)  # Set fixed width to accommodate 4 digits
        vlan_layout.addWidget(max_hosts_spinbox, row, 1)
        row += 1
        # Slot function to update vlan.max_hosts
        def update_max_hosts(value):
            vlan.max_hosts = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the valueChanged signal to the slot function
        max_hosts_spinbox.valueChanged.connect(update_max_hosts)
        
        # Add a QCheckBox for minimum_ip_size_check
        vlan_layout.addWidget(QLabel("Minimum IP Size Check:"), row, 0)
        minimum_ip_size_check_checkbox = QCheckBox(vlan_groupbox)
        minimum_ip_size_check_checkbox.setChecked(vlan.minimum_ip_size_check)
        vlan_layout.addWidget(minimum_ip_size_check_checkbox, row, 1)
        row += 1
        # Slot function to update vlan.minimum_ip_size_check
        def update_minimum_ip_size_check(state):
            vlan.minimum_ip_size_check = bool(state)
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the stateChanged signal to the slot function
        minimum_ip_size_check_checkbox.stateChanged.connect(update_minimum_ip_size_check)     
       
        # Add a QSpinBox for proactive_arp_limit
        vlan_layout.addWidget(QLabel("Proactive ARP Limit:"), row, 0)
        proactive_arp_limit_spinbox = QSpinBox(vlan_groupbox)
        proactive_arp_limit_spinbox.setRange(0, 9999)
        proactive_arp_limit_spinbox.setValue(vlan.proactive_arp_limit)
        vlan_layout.addWidget(proactive_arp_limit_spinbox, row, 1)
        row += 1
        # Add a QSpinBox for proactive_nd_limit
        vlan_layout.addWidget(QLabel("Proactive ND Limit:"), row, 0)
        proactive_nd_limit_spinbox = QSpinBox(vlan_groupbox)
        proactive_nd_limit_spinbox.setRange(0, 9999)
        proactive_nd_limit_spinbox.setValue(vlan.proactive_nd_limit)
        vlan_layout.addWidget(proactive_nd_limit_spinbox, row, 1)
        row += 1
        # Slot function to update vlan.proactive_arp_limit
        def update_proactive_arp_limit(value):
            vlan.proactive_arp_limit = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Slot function to update vlan.proactive_nd_limit
        def update_proactive_nd_limit(value):
            vlan.proactive_nd_limit = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the valueChanged signals to the slot functions
        proactive_arp_limit_spinbox.valueChanged.connect(update_proactive_arp_limit)
        proactive_nd_limit_spinbox.valueChanged.connect(update_proactive_nd_limit)
        
        # Add a QCheckBox for targeted_gw_resolution
        vlan_layout.addWidget(QLabel("Targeted GW Resolution:"), row, 0)
        targeted_gw_resolution_checkbox = QCheckBox(vlan_groupbox)
        targeted_gw_resolution_checkbox.setChecked(vlan.targeted_gw_resolution)
        vlan_layout.addWidget(targeted_gw_resolution_checkbox, row, 1)
        row += 1
        # Slot function to update vlan.targeted_gw_resolution
        def update_targeted_gw_resolution(state):
            vlan.targeted_gw_resolution = bool(state)
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the stateChanged signal to the slot function
        targeted_gw_resolution_checkbox.stateChanged.connect(update_targeted_gw_resolution)

        # Add a QCheckBox for unicast_flood
        vlan_layout.addWidget(QLabel("Unicast Flood:"), row, 0)
        unicast_flood_checkbox = QCheckBox(vlan_groupbox)
        unicast_flood_checkbox.setChecked(vlan.unicast_flood)
        vlan_layout.addWidget(unicast_flood_checkbox, row, 1)
        row += 1
        # Slot function to update vlan.unicast_flood
        def update_unicast_flood(state):
            vlan.unicast_flood = bool(state)
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the stateChanged signal to the slot function
        unicast_flood_checkbox.stateChanged.connect(update_unicast_flood)
        
        # Add a QSpinBox for vid
        vlan_layout.addWidget(QLabel("VID:"), row, 0)
        vid_spinbox = QSpinBox(vlan_groupbox)
        vid_spinbox.setRange(1, 4094)  # Assuming VLAN IDs range from 1 to 4094
        vid_spinbox.setValue(vlan.vid)
        vlan_layout.addWidget(vid_spinbox, row, 1)
        row += 1
        # Slot function to update vlan.vid
        def update_vid(value):
            vlan.vid = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the valueChanged signal to the slot function
        vid_spinbox.valueChanged.connect(update_vid)

        # Add Static Routes group box
        routes_groupbox = QGroupBox("Static Routes", vlan_groupbox)        
        # Set the font size and weight for the QGroupBox title
        routes_groupbox.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
        routes_layout = QGridLayout()
        routes_groupbox.setLayout(routes_layout)
        
        route_row = 0  # Initialize route row counter
        
        # Add "Add Route" button
        add_route_button = QPushButton("Add Route", routes_groupbox)
        routes_layout.addWidget(add_route_button, route_row, 1)
        #print('vlan.name=' + name)
        add_route_button.clicked.connect(lambda _, vlan_name=name, routes_groupbox=routes_groupbox: create_add_route_handler(vlan_name, routes_groupbox)())
        route_row += 1

        # Print the number of items in vlan.routes before populating widgets
        ####print(f"Number of routes in vlan.routes before populating widgets: {len(vlan.routes)}")

        # Slot functions to update vlan.routes
        def update_ip_dst(vlan, index, text):
            ####print('index=' + str(index))
            ####print(f"Number of routes in vlan.routes before update: {len(vlan.routes)}")
            vlan.routes[index]['ip_dst'] = text
            globals.unsaved_changes = True  # Mark as unsaved changes
            ####print(f"Number of routes in vlan.routes after update: {len(vlan.routes)}")

        def update_ip_gw(vlan, index, text):
            vlan.routes[index]['ip_gw'] = text
            globals.unsaved_changes = True  # Mark as unsaved changes

        for index, route in enumerate(vlan.routes):
            print('enumerate index=' + str(index))
            routes_layout.addWidget(QLabel(f"Destination:"), route_row, 0)
            ip_dst_edit = QLineEdit(route['ip_dst'], routes_groupbox)
            routes_layout.addWidget(ip_dst_edit, route_row, 1)
            ip_dst_edit.textChanged.connect(lambda text, idx=index, vlan=vlan: update_ip_dst(vlan, idx, text))

            routes_layout.addWidget(QLabel(f"Gateway:"), route_row, 2)
            ip_gw_edit = QLineEdit(route['ip_gw'], routes_groupbox)
            routes_layout.addWidget(ip_gw_edit, route_row, 3)
            ip_gw_edit.textChanged.connect(lambda text, idx=index, vlan=vlan: update_ip_gw(vlan, idx, text))

            route_row += 1

        ####print(f"Number of routes in vlan.routes after populating widgets: {len(vlan.routes)}")
        vlan_layout.addWidget(routes_groupbox, row, 0, 1, 4)
        row += 1

        # Add the "Remove VLAN" button
        remove_vlan_button = QPushButton("Remove VLAN")
        vlan_layout.addWidget(remove_vlan_button, row, 0, 1, 2)
        row += 1

        # Slot function to remove the VLAN
        def remove_vlan(vlan_name=name):
            reply = QMessageBox.question(vlan_groupbox, 'Remove VLAN', 'Are you sure you want to remove this VLAN?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                del config.vlans[vlan_name]
                globals.unsaved_changes = True  # Mark as unsaved changes
                refresh_vlans_tab(config, vlans_layout, scroll_area)

        # Connect the button click to the remove_vlan slot
        remove_vlan_button.clicked.connect(lambda _, vlan_name=name: remove_vlan(vlan_name))

        # Add the group box to the main layout
        vlans_layout.addWidget(vlan_groupbox)
        vlans_layout.setStretch(0, 1) # Ensures the QGroupBox expands horizontally

    # Set the layout for the VLANs tab
    vlans_tab.setLayout(vlans_layout)

    # Return the configured VLANs tab
    return vlans_tab