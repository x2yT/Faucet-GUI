from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox,
    QComboBox, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QSpinBox, QCheckBox, QHeaderView, QGroupBox, QLabel, QListWidget
)


class MetersTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # Meter ID input
        self.meter_id_input = QLineEdit(self)
        layout.addRow("Meter ID:", self.meter_id_input)

        # Meter Name input
        self.meter_name_input = QLineEdit(self)
        layout.addRow("Meter Name:", self.meter_name_input)

        # Rate input
        self.meter_rate_input = QLineEdit(self)
        layout.addRow("Rate (bps):", self.meter_rate_input)

        # Burst Size input
        self.meter_burst_size_input = QLineEdit(self)
        layout.addRow("Burst Size:", self.meter_burst_size_input)

        # Flags dropdown
        self.flags_input = QComboBox(self)
        self.flags_input.setEditable(True)
        self.flags_input.addItems(['KBPS', 'PKTPS', 'BURST', 'STATS'])
        layout.addRow("Flags (comma separated):", self.flags_input)

        # Bands group
        self.bands_group = QGroupBox("Bands")
        bands_layout = QVBoxLayout()
        self.add_band_button = QPushButton("Add Band")
        self.add_band_button.clicked.connect(self.add_band_row)
        bands_layout.addWidget(self.add_band_button)

        # Bands table
        self.bands_table = QTableWidget(0, 4)
        self.bands_table.setHorizontalHeaderLabels(["Type", "Rate", "Burst Size", "Precedence Level"])
        self.bands_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        bands_layout.addWidget(self.bands_table)
        self.bands_group.setLayout(bands_layout)
        layout.addWidget(self.bands_group)

        # Save button
        save_button = QPushButton("Save Meter", self)
        save_button.clicked.connect(self.save_meter)
        layout.addWidget(save_button)

        # List widget to display saved meters
        self.meter_list_widget = QListWidget()
        self.meter_list_widget.currentItemChanged.connect(self.load_meter_details)
        layout.addWidget(QLabel("Saved Meters:"))
        layout.addWidget(self.meter_list_widget)

        # Delete button
        delete_button = QPushButton("Delete Meter", self)
        delete_button.clicked.connect(self.delete_meter)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def add_band_row(self):
        """Add a new row for the band entry."""
        row_position = self.bands_table.rowCount()
        self.bands_table.insertRow(row_position)

        # Add dropdowns and spinboxes
        type_dropdown = QComboBox()
        type_dropdown.addItems(['DROP', 'DSCP_REMARK'])
        self.bands_table.setCellWidget(row_position, 0, type_dropdown)

        rate_input = QSpinBox()
        rate_input.setRange(1, 1000000)
        self.bands_table.setCellWidget(row_position, 1, rate_input)

        burst_size_input = QSpinBox()
        burst_size_input.setRange(1, 100000)
        self.bands_table.setCellWidget(row_position, 2, burst_size_input)

        precedence_input = QSpinBox()
        precedence_input.setRange(0, 7)
        self.bands_table.setCellWidget(row_position, 3, precedence_input)

    def save_meter(self):
        """Save the meter configuration."""
        meter_id = self.meter_id_input.text().strip()
        meter_name = self.meter_name_input.text().strip()
        meter_rate_text = self.meter_rate_input.text().strip()
        meter_burst_size_text = self.meter_burst_size_input.text().strip()
        selected_flags = self.flags_input.currentText().strip().split(',')

        try:
            meter_id = int(meter_id)
            meter_rate = int(meter_rate_text)
            meter_burst_size = int(meter_burst_size_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Meter ID, Rate and Burst Size must be integers.")
            return

        if not meter_id or not meter_name:
            QMessageBox.warning(self, "Invalid Input", "Meter ID and Name cannot be empty.")
            return

        # Prepare band information
        bands = []
        for row in range(self.bands_table.rowCount()):
            band_type = self.bands_table.cellWidget(row, 0).currentText()
            band_rate = self.bands_table.cellWidget(row, 1).value()
            band_burst_size = self.bands_table.cellWidget(row, 2).value()
            band_precedence = self.bands_table.cellWidget(row, 3).value()
            bands.append({
                'type': band_type,
                'rate': band_rate,
                'burst_size': band_burst_size,
                'prec_level': band_precedence
            })

        # Check if 'meters' attribute exists
        if self.config.meters is None:
            self.config.meters = {}

        # Add or update the meter in the config
        self.config.meters[meter_name] = {
            'meter_id': int(meter_id),
            'rate': meter_rate,
            'burst_size': meter_burst_size,
            'flags': selected_flags,
            'bands': bands
        }

        # Refresh meter list display
        self.update_meter_list()

        QMessageBox.information(self, "Success", "Meter saved successfully!")

        # Clear input fields after saving
        self.clear_input_fields()

    def update_meter_list(self):
        """Update the list of saved meters in the QListWidget."""
        self.meter_list_widget.clear()
        for meter_name in self.config.meters.keys():
            self.meter_list_widget.addItem(meter_name)

    def load_meter_details(self, current_item):
        """Load the selected meter's details into the input fields."""
        if current_item is None:
            return

        meter_name = current_item.text()
        meter_data = self.config.meters[meter_name]



        self.meter_id_input.setText(str(meter_data['meter_id']))
        self.meter_name_input.setText(meter_name)
        self.meter_rate_input.setText(str(meter_data['rate']))
        self.meter_burst_size_input.setText(str(meter_data['burst_size']))
        self.flags_input.setCurrentText(', '.join(meter_data['flags']))

            # Clear existing rows in the bands table
        self.bands_table.setRowCount(0)
            # Load bands data
        for band in meter_data['bands']:
                self.add_band_row()
                row_position = self.bands_table.rowCount() - 1
                self.bands_table.cellWidget(row_position, 0).setCurrentText(band['type'])
                self.bands_table.cellWidget(row_position, 1).setValue(band['rate'])
                self.bands_table.cellWidget(row_position, 2).setValue(band['burst_size'])
                self.bands_table.cellWidget(row_position, 3).setValue(band['prec_level'])



    def delete_meter(self):
        """Delete the selected meter from the config."""
        current_item = self.meter_list_widget.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Delete Meter", "No meter selected to delete.")
            return

        meter_name = current_item.text()
        del self.config.meters[meter_name]
        self.update_meter_list()
        self.clear_input_fields()
        QMessageBox.information(self, "Success", "Meter deleted successfully!")

    def clear_input_fields(self):
        """Clear input fields for new entry."""
        self.meter_id_input.clear()
        self.meter_name_input.clear()
        self.meter_rate_input.clear()
        self.meter_burst_size_input.clear()
        self.bands_table.setRowCount(0)  # Clear the bands table
