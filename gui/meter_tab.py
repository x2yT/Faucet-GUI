from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class MetersTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Pass in the configuration dictionary
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()  # Ensure layout is correctly initialized

        self.meter_name_input = QLineEdit(self)
        self.meter_rate_input = QLineEdit(self)
        self.meter_burst_size_input = QLineEdit(self)

        layout.addRow("Meter Name:", self.meter_name_input)
        layout.addRow("Rate (bps):", self.meter_rate_input)
        layout.addRow("Burst Size:", self.meter_burst_size_input)

        save_button = QPushButton("Save Meter", self)
        save_button.clicked.connect(self.save_meter)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_meter(self):
        meter_name = self.meter_name_input.text()
        meter_rate = self.meter_rate_input.text()
        meter_burst_size = self.meter_burst_size_input.text()

        print(f"Saving meter: {meter_name}, Rate: {meter_rate}, Burst Size: {meter_burst_size}")

        if 'meters' not in self.config:
            self.config['meters'] = {}
        self.config['meters'][meter_name] = {
            'rate': meter_rate,
            'burst_size': meter_burst_size
        }

        import globals
        globals.unsaved_changes = True

        # Optional: You can set a flag indicating unsaved changes
        import globals
        globals.unsaved_changes = True
