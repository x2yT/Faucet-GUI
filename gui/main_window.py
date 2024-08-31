import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget
from configfile.loader import load_config
from configfile.saver import save_config
from gui.vlans_tab import create_vlans_tab
from gui.routers_tab import create_routers_tab
from gui.dps_tab import create_dps_tab
#from models.vlan import Vlan  # Import the Vlan class

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
        config_file_name, _ = QFileDialog.getOpenFileName(self, "Open YAML File", "", "YAML Files (*.yaml)")
        if config_file_name:
            self.config = load_config(config_file_name)
            self.populate_tabs()
            self.setWindowTitle("Faucet GUI - " + config_file_name)
            
    def save_file(self):
        if self.config:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml)")
            if file_name:
                save_config(self.config, file_name)
                
    def populate_tabs(self):
        self.tabs.clear()


        vlans_tab = create_vlans_tab(self.config)
        self.tabs.addTab(vlans_tab, "VLANs")

        routers_tab = create_routers_tab(self.config)
        self.tabs.addTab(routers_tab, "Routers")

        dps_tab = create_dps_tab(self.config)
        self.tabs.addTab(dps_tab, "DPS")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())