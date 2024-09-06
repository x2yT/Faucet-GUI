import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget, QScrollArea, QVBoxLayout, QWidget, QMessageBox
from configfile.loader import load_config, new_config
from configfile.saver import save_config
from gui.vlans_tab import create_vlans_tab
from gui.routers_tab import create_routers_tab
from gui.dps_tab import create_dps_tab
from gui.acls_tab import create_acls_tab

import globals  # Import any global variables

# Define the main window class for the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Faucet Configuration File - Graphical User Interface")
        # Set the window geometry (position and size)
        self.setGeometry(100, 100, 900, 800)
        
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)
        
        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        # Create a tab widget to hold different configuration tabs
        self.tabs = QTabWidget()
        self.scroll_area.setWidget(self.tabs)
        
        # Initialize the configuration attribute
        self.config = None
        
        # Create the menu bar
        self.create_menu()
        
    # Method to create the menu bar
    def create_menu(self):
        # Add a "File" menu to the menu bar
        menu = self.menuBar().addMenu("File")
        
        # Add "New" action to the "File" menu
        new_action = menu.addAction("New")
        new_action.triggered.connect(self.new_file)
        
        # Add "Open" action to the "File" menu
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        
        # Add "Save" action to the "File" menu
        save_action = menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        
    # Method to create a new configuration file
    def new_file(self):
        # Open a file dialog to get the file name for the new YAML file
        file_name, _ = QFileDialog.getSaveFileName(self, "Create New YAML File", "", "YAML Files (*.yaml)")
        if file_name:
            # Create a new configuration
            self.config = new_config()  # Call the function to get the config dictionary
            # Save the default config to the specified file
            ######## needs to be fixed ... save_config(self.config, file_name)
            # Populate the tabs with the new configuration
            self.populate_tabs()
            # Update the window title with the new file name
            self.setWindowTitle("Faucet GUI - " + file_name)
        
    # Method to open an existing configuration file
    def open_file(self):
        # Open a file dialog to get the file name of the YAML file to open
        config_file_name, _ = QFileDialog.getOpenFileName(self, "Open YAML File", "", "YAML Files (*.yaml)")
        if config_file_name:
            # Load the configuration from the specified file
            self.config = load_config(config_file_name)
            # Populate the tabs with the loaded configuration
            self.populate_tabs()
            # Update the window title with the opened file name
            self.setWindowTitle("Faucet GUI - " + config_file_name)
            
    # Method to save the current configuration to a file
    def save_file(self):
        if self.config:
            # Open a file dialog to get the file name to save the YAML file
            file_name, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml)")
            if file_name:
                # Save the current configuration to the specified file
                # Note: Adjust the parameters as needed to save specific parts of the configuration
                save_config(self.config, file_name, save_vlans=False, save_routers=False, save_dps=False, save_acls=True)
                # Reset the unsaved changes flag
                globals.unsaved_changes = False
                
    # Method to populate the tabs with the current configuration
    def populate_tabs(self):
        # Clear any existing tabs
        self.tabs.clear()

        # Create and add the VLANs tab
        vlans_tab = create_vlans_tab(self.config)
        self.tabs.addTab(vlans_tab, "VLANs")

        # Create and add the Routers tab
        routers_tab = create_routers_tab(self.config)
        self.tabs.addTab(routers_tab, "Routers")

        # Create and add the DPS tab
        dps_tab = create_dps_tab(self.config)
        self.tabs.addTab(dps_tab, "DPS")  

        # Create and add the ACLS tab
        acls_tab = create_acls_tab(self.config)
        self.tabs.addTab(acls_tab, "ACLS")  

    def closeEvent(self, event):
        # Check if any changes have been made and not saved
        print("Unsaved Changes-" + str(globals.unsaved_changes))
        if globals.unsaved_changes:
            reply = QMessageBox.question(self, 'Unsaved Changes', 'You have unsaved changes. Are you sure you want to exit without saving?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        event.accept()