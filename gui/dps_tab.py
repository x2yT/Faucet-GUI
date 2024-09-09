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
                    row += 1
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
                                elif isinstance(iface_value, dict) and iface_attr == 'lldp_beacon':
                                    lldp_label = QLabel("lldp")
                                    iface_layout.addWidget(lldp_label, iface_row, 0)
                                    lldp_group_box = QGroupBox()
                                    lldp_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                                    lldp_layout = QGridLayout()
                                    lldp_row = 0
                                    lldp_col = 0
                                    for lldp_attr, lldp_value in iface_value.items():
                                        lldp_attr_label = QLabel(lldp_attr)
                                        if isinstance(lldp_value, bool):
                                            lldp_widget = QCheckBox()
                                            lldp_widget.setChecked(lldp_value)
                                        elif isinstance(lldp_value, int):
                                            lldp_widget = QSpinBox()
                                            lldp_widget.setValue(lldp_value)
                                        elif isinstance(lldp_value, float):
                                            lldp_widget = QDoubleSpinBox()
                                            lldp_widget.setValue(lldp_value)
                                        elif isinstance(lldp_value, str):
                                            lldp_widget = QLineEdit()
                                            lldp_widget.setText(lldp_value)
                                            lldp_widget.setFixedWidth(200)
                                        elif isinstance(lldp_value, list):
                                            # add the list item on its own row
                                            if lldp_col > 0:
                                                lldp_col = 0
                                                lldp_row += 1                                                
                                            lldp_widget = QLineEdit()
                                            lldp_widget.setText(", ".join(map(str, lldp_value)))  # Convert list to comma-separated string
                                            lldp_widget.setFixedWidth(400)
                                        else:
                                            lldp_widget = QLabel(str(lldp_value))  # Fallback for other types

                                        lldp_layout.addWidget(lldp_attr_label, lldp_row, lldp_col)
                                        lldp_layout.addWidget(lldp_widget, lldp_row, lldp_col + 1)
                                        lldp_col += 2
                                        if lldp_col >= 4:  # Move to next row after 2 attributes
                                            lldp_col = 0
                                            lldp_row += 1

                                    lldp_group_box.setLayout(lldp_layout)
                                    iface_layout.addWidget(lldp_group_box, iface_row, 1, 1, 3)
                                    iface_row += 1
                                    continue  # Skip adding the lldp_beacon as a regular attribute
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
                elif attr == 'dot1x' and isinstance(value, dict):
                    print('dot1x')
                    row += 1
                    dot1x_label = QLabel("dot1x")
                    dot1x_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(dot1x_label, row, 0, 1, 2)
                    dot1x_group_box = QGroupBox() 
                    dot1x_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    #dot1x_group_box.setFixedWidth(750)
                    dot1x_layout = QGridLayout()
                    print(f'value={value}')
                    dot1x_row = 0
                    dot1x_col = 0                       
                    for dot1x_attr, dot1x_value in value.items():

                        dot1x_label = QLabel(dot1x_attr)
                        if isinstance(dot1x_value, bool):
                            dot1x_widget = QCheckBox()
                            dot1x_widget.setChecked(dot1x_value)
                        elif isinstance(dot1x_value, int):
                            dot1x_widget = QSpinBox()
                            dot1x_widget.setValue(dot1x_value)
                        elif isinstance(dot1x_value, float):
                            dot1x_widget = QDoubleSpinBox()
                            dot1x_widget.setValue(dot1x_value)
                        elif isinstance(dot1x_value, str):
                            dot1x_widget = QLineEdit()
                            dot1x_widget.setText(dot1x_value)
                            dot1x_widget.setFixedWidth(200)
                        elif isinstance(dot1x_value, list):
                            dot1x_widget = QLineEdit()
                            dot1x_widget.setText(", ".join(map(str, dot1x_value)))  # Convert list to comma-separated string
                            dot1x_widget.setFixedWidth(200)
                        else:
                            dot1x_widget = QLabel(str(dot1x_value))  # Fallback for other types

                        dot1x_layout.addWidget(dot1x_label, dot1x_row, dot1x_col)
                        dot1x_layout.addWidget(dot1x_widget, dot1x_row, dot1x_col + 1)
                        dot1x_col += 2
                        if dot1x_col >= 4:  # Move to next row after 2 attributes
                            dot1x_col = 0
                            dot1x_row += 1

                        dot1x_group_box.setLayout(dot1x_layout)
                        grid_layout.addWidget(dot1x_group_box, row, 1, 1, 3)
                elif attr == 'lldp_beacon' and isinstance(value, dict):
                    print('lldp_beacon')
                    row += 1
                    lldp_label = QLabel("lldp")
                    lldp_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(lldp_label, row, 0, 1, 2)
                    lldp_group_box = QGroupBox() 
                    lldp_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    #lldp_group_box.setFixedWidth(750)
                    lldp_layout = QGridLayout()
                    print(f'value={value}')
                    lldp_row = 0
                    lldp_col = 0                       
                    for lldp_attr, lldp_value in value.items():

                        lldp_label = QLabel(lldp_attr)
                        if isinstance(lldp_value, bool):
                            lldp_widget = QCheckBox()
                            lldp_widget.setChecked(lldp_value)
                        elif isinstance(lldp_value, int):
                            lldp_widget = QSpinBox()
                            lldp_widget.setValue(lldp_value)
                        elif isinstance(lldp_value, float):
                            lldp_widget = QDoubleSpinBox()
                            lldp_widget.setValue(lldp_value)
                        elif isinstance(lldp_value, str):
                            lldp_widget = QLineEdit()
                            lldp_widget.setText(lldp_value)
                            lldp_widget.setFixedWidth(200)
                        elif isinstance(lldp_value, list):
                            print('List for=' + lldp_attr)
                            lldp_widget = QLineEdit()
                            lldp_widget.setText(", ".join(map(str, lldp_value)))  # Convert list to comma-separated string
                            lldp_widget.setFixedWidth(200)
                        else:
                            lldp_widget = QLabel(str(lldp_value))  # Fallback for other types

                        lldp_layout.addWidget(lldp_label, lldp_row, lldp_col)
                        lldp_layout.addWidget(lldp_widget, lldp_row, lldp_col + 1)
                        lldp_col += 2
                        if lldp_col >= 4:  # Move to next row after 2 attributes
                            lldp_col = 0
                            lldp_row += 1

                        lldp_group_box.setLayout(lldp_layout)
                        grid_layout.addWidget(lldp_group_box, row, 1, 1, 3)
                elif attr == 'stack' and isinstance(value, dict):
                    print('Stack')
                    row += 1
                    stack_label = QLabel("stack")
                    stack_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(stack_label, row, 0, 1, 2)
                    stack_group_box = QGroupBox() 
                    stack_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    #stack_group_box.setFixedWidth(750)
                    stack_layout = QGridLayout()
                    print(f'value={value}')
                    stack_row = 0
                    stack_col = 0                       
                    for stack_attr, stack_value in value.items():

                        stack_label = QLabel(stack_attr)
                        if isinstance(stack_value, bool):
                            stack_widget = QCheckBox()
                            stack_widget.setChecked(stack_value)
                        elif isinstance(stack_value, int):
                            stack_widget = QSpinBox()
                            stack_widget.setValue(stack_value)
                        elif isinstance(stack_value, float):
                            stack_widget = QDoubleSpinBox()
                            stack_widget.setValue(stack_value)
                        elif isinstance(stack_value, str):
                            stack_widget = QLineEdit()
                            stack_widget.setText(stack_value)
                            stack_widget.setFixedWidth(200)
                        elif isinstance(stack_value, list):
                            print('List for=' + stack_attr)
                            stack_widget = QLineEdit()
                            stack_widget.setText(", ".join(map(str, stack_value)))  # Convert list to comma-separated string
                            stack_widget.setFixedWidth(200)
                        else:
                            stack_widget = QLabel(str(stack_value))  # Fallback for other types

                        stack_layout.addWidget(stack_label, stack_row, stack_col)
                        stack_layout.addWidget(stack_widget, stack_row, stack_col + 1)
                        stack_col += 2
                        if stack_col >= 4:  # Move to next row after 2 attributes
                            stack_col = 0
                            stack_row += 1

                        stack_group_box.setLayout(stack_layout)
                        grid_layout.addWidget(stack_group_box, row, 1, 1, 3)
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