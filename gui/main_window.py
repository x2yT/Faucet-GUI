import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget, QWidget, QVBoxLayout, QLabel
from configfile.loader import load_config
from configfile.saver import save_config
from models.vlan import Vlan  # Import the Vlan class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Faucet Configuration File - Graphical User Interface")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.config = None
        
        self.create_menu()
        
    def create_menu(self):
        menu = self.menuBar().addMenu("File")
        
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        
        save_action = menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open YAML File", "", "YAML Files (*.yaml)")
        if file_name:
            self.config = load_config(file_name)
            self.populate_tabs()
            
    def save_file(self):
        if self.config:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml)")
            if file_name:
                save_config(self.config, file_name)
                
    def populate_tabs(self):
        self.tabs.clear()
        
        include_tab = QWidget()
        include_layout = QVBoxLayout()
        include_layout.addWidget(QLabel(f"Include: {', '.join(self.config.include)}"))
        include_tab.setLayout(include_layout)
        self.tabs.addTab(include_tab, "Include")
        
        vlans_tab = QWidget()
        vlans_layout = QVBoxLayout()
        for name, vlan in self.config.vlans.items():
            vlan_group = QWidget()
            vlan_layout = QVBoxLayout()
            vlan_layout.addWidget(QLabel(f"VLAN Name: {name}"))
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
        self.tabs.addTab(vlans_tab, "VLANs")
        
        routers_tab = QWidget()
        routers_layout = QVBoxLayout()
        for name, router in self.config.routers.items():
            routers_layout.addWidget(QLabel(f"Router {name}: {router.__dict__}"))
        routers_tab.setLayout(routers_layout)
        self.tabs.addTab(routers_tab, "Routers")
        
        dps_tab = QWidget()
        dps_layout = QVBoxLayout()
        for name, dp in self.config.dps.items():
            dps_layout.addWidget(QLabel(f"DP {name}: {dp.__dict__}"))
        dps_tab.setLayout(dps_layout)
        self.tabs.addTab(dps_tab, "DPs")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())