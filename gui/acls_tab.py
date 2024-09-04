from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QDoubleSpinBox, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import globals

def create_acls_tab(config):
    # Create the main widget for the acls_tab
    acls_tab = QWidget()
    acls_layout = QVBoxLayout(acls_tab)
    # Create a new layout for the ACLs tab
    #acls_layout = QVBoxLayout()
    #acls_tab.setLayout(acls_layout)

    # Function to create a QLineEdit with fixed width
    def create_line_edit(text, parent, width=200):
        line_edit = QLineEdit(text, parent)
        line_edit.setFixedWidth(width)  # Set fixed width
        return line_edit

    # Iterate over the ACLs in the configuration
    for acl_name, acl in config.acls.items():
        # Create a new QGroupBox with the ACL name
        acl_groupbox = QGroupBox(acl_name)
        acl_groupbox.setStyleSheet("QGroupBox { font-size: 12pt; font-weight: bold; }")

        # Create a QGridLayout for the ACL details
        acl_layout = QGridLayout()
        acl_groupbox.setLayout(acl_layout)

        row = 0  # Initialize row counter

        # Add a QLineEdit for the ACL name
        acl_layout.addWidget(QLabel("ACL Name:"), row, 0)
        acl_name_edit = create_line_edit(acl_name, acl_groupbox)
        acl_layout.addWidget(acl_name_edit, row, 1)
        row += 1

        # Slot function to update the ACL name
        def update_acl_name(old_name, new_name, acl_groupbox):
            if new_name and new_name != old_name:
                # Update the key in the config.acls dictionary
                config.acls[new_name] = config.acls.pop(old_name)
                # Update the QGroupBox title
                acl_groupbox.setTitle(new_name)
                globals.unsaved_changes = True  # Mark as unsaved changes

        # Connect the editingFinished signal to the update_acl_name slot
        acl_name_edit.editingFinished.connect(lambda old_name=acl_name, edit=acl_name_edit, groupbox=acl_groupbox: update_acl_name(old_name, edit.text(), groupbox))

        # Add ACL rules to the form
        for rule in acl.rules:
            rule_label = QLabel("Rule:", alignment=Qt.AlignmentFlag.AlignTop)
            rule_label.setFixedWidth(70)
            acl_layout.addWidget(rule_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)

            rule_groupbox = QGroupBox(acl_groupbox)
            rule_layout = QGridLayout()
            rule_groupbox.setLayout(rule_layout)

            rule_row = 0  # Initialize rule row counter

            for key, value in rule.__dict__.items():
                if value is not None:
                    if key == 'actions':
                        #rule_layout.addWidget(QLabel(f"{key}:"), 0, 4)
                        item_label = QLabel(f"{key}:")
                        item_label.setFixedWidth(90)
                        rule_layout.addWidget(item_label, 0, 3)
                        #rule_layout.addWidget(QLineEdit(str(value), rule_groupbox), 0, 4)
                        print(f"actions: {value}")
                        for ak, av in value.items():
                            if ak == 'allow':
                                value_checkbox = QCheckBox('allow', rule_groupbox)
                                value_checkbox.setChecked(av)
                                rule_layout.addWidget(value_checkbox, 1, 4)   
                            elif ak == 'force_port_vlan':
                                value_checkbox = QCheckBox('force_port_vlan', rule_groupbox)
                                value_checkbox.setChecked(av)
                                rule_layout.addWidget(value_checkbox, 1, 4)     
                            elif ak == 'cookie':
                                item_label = QLabel('cookie', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, 1, 3)
                                value_spinkbox = QSpinBox('cookie', rule_groupbox)
                                value_spinkbox.setRange(0, 999999)
                                value_spinkbox.setValue(av)
                                value_spinkbox.setFixedWidth(90)    
                                rule_layout.addWidget(value_spinkbox, 1, 4)     
                            elif ak == 'meter':
                                item_label = QLabel('meter', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, 1, 3)
                                value_edit = QLineEdit(str(av), rule_groupbox)
                                value_edit.setFixedWidth(140)
                                rule_layout.addWidget(value_edit, 1, 4)      
                            elif ak == 'mirror':
                                item_label = QLabel('mirror', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, 1, 3)
                                value_edit = QLineEdit(str(av), rule_groupbox)
                                value_edit.setFixedWidth(140)
                                rule_layout.addWidget(value_edit, 1, 4)     
                    else:
                        item_label = QLabel(f"{key}:", rule_groupbox)
                        item_label.setFixedWidth(90)
                        rule_layout.addWidget(item_label, rule_row, 0)
                        #rule_layout.addWidget(QLabel(f"{key}:"), rule_row, 0)
                        if isinstance(value, int):
                            value_edit = QSpinBox(rule_groupbox)
                            value_edit.setRange(0, 999999)
                            value_edit.setValue(value)
                            value_edit.setFixedWidth(90)
                        elif isinstance(value, float):
                            value_edit = QDoubleSpinBox(rule_groupbox)
                            value_edit.setValue(value)
                            value_edit.setMaximum(999999.99)  # Set a reasonable maximum value
                            value_edit.setFixedWidth(90)
                        elif isinstance(value, bool):
                            value_edit = QCheckBox(rule_groupbox)
                            value_edit.setChecked(value)
                            value_edit.setFixedWidth(90)
                        else:
                            value_edit = QLineEdit(str(value), rule_groupbox)
                            value_edit.setFixedWidth(140)

                        rule_layout.addWidget(value_edit, rule_row, 1)
                        rule_row += 1

                    if rule_row == 0:
                        rule_row = 3

                    # Add a spacer item between columns 1 and 2
                    # spacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                    # rule_layout.addItem(spacer, 0, 2, rule_row, 1)

                    # Slot function to update the rule value
                    # def update_rule_value(key, edit):
                    #     if isinstance(edit, QSpinBox) or isinstance(edit, QDoubleSpinBox):
                    #         setattr(rule, key, edit.value())
                    #     elif isinstance(edit, QCheckBox):
                    #         setattr(rule, key, edit.isChecked())
                    #     else:
                    #         setattr(rule, key, edit.text())
                    #     globals.unsaved_changes = True  # Mark as unsaved changes

                    # Connect the appropriate signal to the update_rule_value slot
                    # if isinstance(value_edit, QSpinBox) or isinstance(value_edit, QDoubleSpinBox):
                    #     value_edit.valueChanged.connect(lambda key=key, edit=value_edit: update_rule_value(key, edit))
                    # elif isinstance(value_edit, QCheckBox):
                    #     value_edit.stateChanged.connect(lambda key=key, edit=value_edit: update_rule_value(key, edit))
                    # else:
                    #     value_edit.textChanged.connect(lambda key=key, edit=value_edit: update_rule_value(key, edit))

            print('row=' + str(row) + ' rule_row=' + str(rule_row))
            acl_layout.addWidget(rule_groupbox, row, 1, rule_row, 4)
            row += rule_row

        # Add the ACL groupbox to the ACLs layout
        acls_layout.addWidget(acl_groupbox)

    # Add a spacer to push the groupboxes to the top
    #acls_layout.addStretch()
    acls_tab.setLayout(acls_layout)
    
    return acls_tab