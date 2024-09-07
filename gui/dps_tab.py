# dps_tab.py
from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QDoubleSpinBox, QSpacerItem, QSizePolicy, QDialogButtonBox, QComboBox
from PyQt6.QtCore import Qt
from configfile.loader import new_config, ACL, Rule  # Assuming new_config is imported from loader.py
import globals

def create_dps_tab(config):
    dps_tab = QWidget()
    dps_layout = QVBoxLayout()

    for name, dp in config.dps.items():
        group_box = QGroupBox(f"{name}")
        group_box.setStyleSheet("QGroupBox { font-size: 12pt; font-weight: bold; }")
        group_box.setFixedWidth(800)  # Set a fixed width for the group box
        grid_layout = QGridLayout()

        # Add QLineEdit for DP name
        name_label = QLabel("DP Name")
        name_label.setStyleSheet("font-weight: bold;")
        name_label.setFixedWidth(150)
        name_edit = QLineEdit(name)
        name_edit.setFixedWidth(200)
        name_edit.textChanged.connect(lambda text, gb=group_box: gb.setTitle(text))
        grid_layout.addWidget(name_label, 0, 0)
        grid_layout.addWidget(name_edit, 0, 1)

        row = 1
        col = 0
        for attr, value in dp.__dict__.items():
            if value is not None and value != [] and value != {}:
                print('attr=' + attr, type(value))
                if attr == 'interfaces' and isinstance(value, dict):
                    interfaces_label = QLabel("Interfaces")
                    interfaces_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(interfaces_label, row, 0, 1, 2)
                    #row += 1
                    print(f'value={value}')
                    for iface_name, iface in value.items():
                        iface_group_box = QGroupBox(str(iface_name)) 
                        iface_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                        #iface_group_box.setFixedWidth(750)
                        iface_layout = QGridLayout()
                        iface_row = 0
                        iface_col = 0
                        for iface_attr, iface_value in iface.__dict__.items():
                            # Exclude empty items
                            if iface_value is not None and iface_value != [] and iface_value != {}:
                                iface_label = QLabel(iface_attr)
                                if isinstance(iface_value, bool):
                                    iface_widget = QCheckBox()
                                    iface_widget.setChecked(iface_value)
                                elif isinstance(iface_value, int):
                                    iface_widget = QSpinBox()
                                    iface_widget.setValue(iface_value)
                                elif isinstance(iface_value, float):
                                    iface_widget = QDoubleSpinBox()
                                    iface_widget.setValue(iface_value)
                                elif isinstance(iface_value, str):
                                    iface_widget = QLineEdit()
                                    iface_widget.setText(iface_value)
                                    iface_widget.setFixedWidth(200)
                                elif isinstance(iface_value, list):
                                    iface_widget = QLineEdit()
                                    iface_widget.setText(", ".join(map(str, iface_value)))  # Convert list to comma-separated string
                                    iface_widget.setFixedWidth(200)
                                else:
                                    iface_widget = QLabel(str(iface_value))  # Fallback for other types

                                iface_layout.addWidget(iface_label, iface_row, iface_col)
                                iface_layout.addWidget(iface_widget, iface_row, iface_col + 1)
                                iface_col += 2
                                if iface_col >= 4:  # Move to next row after 2 attributes
                                    iface_col = 0
                                    iface_row += 1

                        iface_group_box.setLayout(iface_layout)
                        grid_layout.addWidget(iface_group_box, row, 1, 1, 3)
                        row += 1
                else:
                    label = QLabel(attr)
                    label.setFixedWidth(150)
                    if isinstance(value, bool):
                        widget = QCheckBox()
                        widget.setChecked(value)
                    elif isinstance(value, int):
                        widget = QSpinBox()
                        widget.setValue(value)
                    elif isinstance(value, float):
                        widget = QDoubleSpinBox()
                        widget.setValue(value)
                        widget.setMaximumWidth(200)
                    elif isinstance(value, str):
                        widget = QLineEdit()
                        widget.setText(value)
                        widget.setFixedWidth(200)
                    else:
                        widget = QLabel(str(value))  # Fallback for other types

                    grid_layout.addWidget(label, row, col)
                    grid_layout.addWidget(widget, row, col + 1)
                    col += 2
                    if col >= 4:  # Move to next row after 2 attributes
                        col = 0
                        row += 1

        group_box.setLayout(grid_layout)
        dps_layout.addWidget(group_box)

    dps_tab.setLayout(dps_layout)
    return dps_tab