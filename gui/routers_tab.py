# routers_tab.py

from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox
from configfile.loader import new_config, Router, Bgp  # Assuming new_config is imported from loader.py
import globals

# Define a dialog class for adding routes
class AddVlanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Vlan")
        self.setModal(True)
        
        layout = QVBoxLayout()

        # Input fields for vlan
        self.vlan_edit = QLineEdit(self)
        
        # Input fields for vlan
        layout.addWidget(QLabel("vlan:"))
        layout.addWidget(self.vlan_edit)
        
        # # OK and Cancel buttons
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
        
    def get_value(self):
        return self.vlan_edit.text()
    
# Function to add a new route
def add_vlan(config, vlans_groupbox, router_name):
    # Check the route exists
    router = config.routers.get(router_name)
    if router is None:
        print(f"ROUTER {router_name} not found in config.")
        return
    
    dialog = AddVlanDialog(vlans_groupbox)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print('accepted')
        vlan = dialog.get_value()
        if vlan:
            print('vlan=' + vlan)   
            
            # Ensure route.routes is initialized
            if not hasattr(vlan, 'vlans'):
                vlan.vlans = []
            
            print(*vlan.vlans, sep=", ")
            # Add the new route to the ROUTER's routes
            vlan.vlans.append({'vlan': vlan})
            print(*vlan.vlans, sep=", ")

            # Update the routes_groupbox UI
            vlans_row = vlans_groupbox.layout().rowCount()
            vlans_groupbox.layout().addWidget(QLabel(f"Vlan:"), vlans_row, 0)
            vlans_groupbox.layout().addWidget(QLineEdit(vlan, vlans_groupbox), vlans_row, 1)
#________________________________________________________________________________________________

# Function to refresh the ROUTER tab
def refresh_routers_tab(config, routers_layout, scroll_area):
    # Clear the existing layout
    for i in reversed(range(routers_layout.count())):
        widget = routers_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    # Recreate the ROUTER tab
    create_routers_tab(config, routers_layout, scroll_area)

# Create the ROUTER tab
def create_routers_tab(config, routers_layout=None, scroll_area=None):
    print(config.routers)
    if routers_layout is None:
        routers_tab = QWidget()
        routers_layout = QVBoxLayout()
        routers_tab.setLayout(routers_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(routers_tab)
    else:
        routers_tab = routers_layout.parentWidget()

    # Button to add a new Router
    add_router_button = QPushButton("Add Router")
    routers_layout.addWidget(add_router_button)
    
    # Slot function to add a new Router
    def add_router():
        # Create a new Router object with initial values
        new_router_name = "New Router"
        new_bgp = Bgp()
        new_vlan = []
        new_router = Router(new_bgp, new_vlan)
        config.routers[new_router_name] = new_router

        # Refresh the Router tab
        refresh_routers_tab(config, routers_layout, scroll_area)
        # Scroll to the bottom
        scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())
        globals.unsaved_changes = True  # Mark as unsaved changes
    # Connect the button click to the add_router slot
    add_router_button.clicked.connect(add_router)

    # This function is used by the New Route dialog to reference the config for the data dictionary
    def create_add_vlan_handler(router_name, vlans_groupbox):
        print('router_name='+ router_name)
        return lambda: add_vlan(config, vlans_groupbox, router_name)
    
    # Slot function to update the ROUTER key name
    def update_router_name(old_name, new_name, router_groupbox):
        if new_name and new_name != old_name:
            # Update the key in the config.routers dictionary
            config.routers[new_name] = config.routers.pop(old_name)
            # Update the QGroupBox title
            router_groupbox.setTitle(new_name)
            globals.unsaved_changes = True  # Mark as unsaved changes

    # Create a new Groupbox for each ROUTER
    for name, route in config.routers.items():
        
        router_group = QWidget()
        # Create a QGroupBox with the ROUTER name
        router_groupbox = QGroupBox(name)        
        # Set the font size and weight for the QGroupBox title
        router_groupbox.setStyleSheet("QGroupBox { font-size: 12pt; font-weight: bold; }")

        # Create a QGridLayout for the ROUTER details
        router_layout = QGridLayout()
        
        # Set the layout for the group box
        router_groupbox.setLayout(router_layout)
        
        row = 0  # Initialize row counter
        
        # Function to create a QLineEdit with fixed width
        def create_line_edit(text, parent, width=200):
            line_edit = QLineEdit(text, parent)
            line_edit.setFixedWidth(width)  # Set fixed width
            return line_edit
        
        # Add other VLAN details to the form
        router_layout.addWidget(QLabel("Vlans:"), row, 0)
        vlans_edit = create_line_edit(', '.join(route.vlans), router_groupbox)
        router_layout.addWidget(vlans_edit, row, 1)
        row += 1
        # Slot function to update user changes back to route.vlans
        def update_vlans(text):
            route.vlans = text.split(', ')
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the textChanged signal to the slot function
        vlans_edit.textChanged.connect(update_vlans)

        # Add Static Routes group box
        vlans_groupbox = QGroupBox("Bgp", router_groupbox)        
        # Set the font size and weight for the QGroupBox title
        vlans_groupbox.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
        vlans_layout = QGridLayout()
        vlans_groupbox.setLayout(vlans_layout)
        
        route_row = 0  # Initialize route row counter

        # Add a as for bgp
        vlans_layout.addWidget(QLabel("As:"), route_row, 0)
        as_spinbox = QSpinBox(vlans_groupbox)
        as_spinbox.setRange(1, 4094)  # Assuming VLAN IDs range from 1 to 4094
        as_spinbox.setValue(route.bgp.as_number)
        vlans_layout.addWidget(as_spinbox, route_row, 1)
        route_row += 1
        # Slot function to update route.bgp.as_number
        def update_as(value):
            route.bgp.as_number = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the valueChanged signal to the slot function
        as_spinbox.valueChanged.connect(update_as)

        # Add a as for Neighbor as
        vlans_layout.addWidget(QLabel("Neighbor As:"), route_row, 0)
        neighbor_as_spinbox = QSpinBox(vlans_groupbox)
        neighbor_as_spinbox.setRange(1, 4094)  # Assuming VLAN IDs range from 1 to 4094
        neighbor_as_spinbox.setValue(route.bgp.neighbor_as)
        vlans_layout.addWidget(neighbor_as_spinbox, route_row, 1)
        route_row += 1
        # Slot function to update route.bgp.neighbor_as
        def update_neighbor_as(value):
            route.bgp.neighbor_as = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        # Connect the valueChanged signal to the slot function
        neighbor_as_spinbox.valueChanged.connect(update_neighbor_as)

        # Add a routerid for bgp
        vlans_layout.addWidget(QLabel("Router ID:"), route_row, 0)
        routerid_edit = QLineEdit(route.bgp.routerid, vlans_groupbox)
        vlans_layout.addWidget(routerid_edit, route_row, 1, 1, 3)
        route_row += 1
        # Slot function to update route.bgp.routerid with the description
        def update_routerid(text):
            route.bgp.routerid = [text]
            globals.unsaved_changes = True  # Mark as unsaved changes
            print("Unsaved Changed=" + str(globals.unsaved_changes))
        routerid_edit.textChanged.connect(update_routerid)

        # Add server and neighbor addr 
        vlans_layout.addWidget(QLabel("Server Addresses:"), route_row, 0)
        server_addr_edit = QLineEdit(', '.join(route.bgp.server_addresses), vlans_groupbox)
        vlans_layout.addWidget(server_addr_edit, route_row, 1, 1, 3)
        route_row += 1
        def update_server_addrs(text):
            route.bgp.server_addresses = text.split(', ')
            globals.unsaved_changes = True  # Mark as unsaved changes
        server_addr_edit.textChanged.connect(update_server_addrs)

        vlans_layout.addWidget(QLabel("Neighbor Addresses:"), route_row, 0)
        neighbor_addr_edit = QLineEdit(', '.join(route.bgp.neighbor_addresses), vlans_groupbox)
        vlans_layout.addWidget(neighbor_addr_edit, route_row, 1, 1, 3)
        route_row += 1
        def update_neighbor_addrs(text):
            route.bgp.neighbor_addresses = text.split(', ')
            globals.unsaved_changes = True  # Mark as unsaved changes
        neighbor_addr_edit.textChanged.connect(update_neighbor_addrs)

        # Add a vlan for bgp
        vlans_layout.addWidget(QLabel("Vlan:"), route_row, 0)
        vlan_edit = QLineEdit(route.bgp.vlan, vlans_groupbox)
        vlans_layout.addWidget(vlan_edit, route_row, 1, 1, 3)
        route_row += 1
        # Slot function to update route.bgp.routerid with the description
        def update_vlan(text):
            route.bgp.vlan = [text]
            globals.unsaved_changes = True  # Mark as unsaved changes
            print("Unsaved Changed=" + str(globals.unsaved_changes))
        vlan_edit.textChanged.connect(update_vlan)

        # Add a as for bgp
        vlans_layout.addWidget(QLabel("Port:"), route_row, 0)
        port_spinbox = QSpinBox(vlans_groupbox)
        port_spinbox.setRange(1, 65535)  # Assuming VLAN IDs range from 1 to 4094
        port_spinbox.setValue(route.bgp.port)
        vlans_layout.addWidget(port_spinbox, route_row, 1)
        route_row += 1
        def update_port(value):
            route.bgp.port = value
            globals.unsaved_changes = True  # Mark as unsaved changes
        port_spinbox.valueChanged.connect(update_port)

        router_layout.addWidget(vlans_groupbox, row, 0, 1, 4)
        row += 1
        
        # Add the "Remove Router" button
        remove_router_button = QPushButton("Remove Router")
        router_layout.addWidget(remove_router_button, row, 0, 1, 2)
        row += 1

        # Slot function to remove the VLAN
        def remove_router(router_name=name):
            reply = QMessageBox.question(vlans_groupbox, 'Remove Router', 'Are you sure you want to remove this Router?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                del config.routers[router_name]
                globals.unsaved_changes = True  # Mark as unsaved changes
                refresh_routers_tab(config, router_layout, scroll_area)

        # Connect the button click to the remove_vlan slot
        remove_router_button.clicked.connect(lambda _, router_name=name: remove_router(router_name))

        # Add the group box to the main layout
        routers_layout.addWidget(router_groupbox)

    # Set the layout for the VLANs tab
    routers_tab.setLayout(routers_layout)

    # Return the configured VLANs tab
    return routers_tab