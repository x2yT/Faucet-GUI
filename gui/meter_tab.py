from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox

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
        meter_name = self.meter_name_input.text().strip()
        meter_rate_text = self.meter_rate_input.text().strip()
        meter_burst_size_text = self.meter_burst_size_input.text().strip()

        try:
            meter_rate = int(meter_rate_text)
            meter_burst_size = int(meter_burst_size_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Rate and Burst Size must be integers.")
            return

        if not meter_name:
            QMessageBox.warning(self, "Invalid Input", "Meter Name cannot be empty.")
            return

        print(f"Saving meter: {meter_name}, Rate: {meter_rate}, Burst Size: {meter_burst_size}")

        # Check if 'meters' attribute exists, and if not, create it
        if self.config.meters is None:
            self.config.meters = {}

        # Add or update the meter in the config
        self.config.meters[meter_name] = {
            'rate': meter_rate,
            'burst_size': meter_burst_size



        }

        # Optional: You can set a flag indicating unsaved changes
        import globals
        globals.unsaved_changes = True

        QMessageBox.information(self, "Success", "Meter saved successfully!")

        # Clear input fields after saving
        self.meter_name_input.clear()
        self.meter_rate_input.clear()
        self.meter_burst_size_input.clear()
