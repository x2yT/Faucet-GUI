from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QDoubleSpinBox, QSpacerItem, QSizePolicy, QDialogButtonBox
from PyQt6.QtCore import Qt
from configfile.loader import new_config, ACL, Rule  # Assuming new_config is imported from loader.py
import globals

# Function to refresh the ACLS tab
def refresh_acls_tab(config, acls_layout, scroll_area):
    # Clear the existing layout
    print('refresh_acls_tab ...')
    for i in reversed(range(acls_layout.count())):
        widget = acls_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    # Recreate the ACLS tab
    create_acls_tab(config, acls_layout, scroll_area)

# Create the ACLS tab
def create_acls_tab(config, acls_layout=None, scroll_area=None):
    if acls_layout is None:
        print('layout is none')
        acls_tab = QWidget()
        acls_layout = QVBoxLayout()
        acls_tab.setLayout(acls_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(acls_tab)
    else:
        print('using parent widget')
        acls_tab = acls_layout.parentWidget()

    # Button to add a new ACL
    add_acl_button = QPushButton("Add ACL")
    acls_layout.addWidget(add_acl_button)
    
    # Slot function to add a new ACL
    def add_acl():
        # Create a new ACL dictionary with initial values
        new_acl_name = "new acl"
        new_acl = ACL(
            name=new_acl_name,
            rules={}
        )
        config.acls[new_acl_name] = new_acl
        # Refresh the ACLS tab
        refresh_acls_tab(config, acls_layout, scroll_area)
        # Scroll to the bottom
        scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())
        globals.unsaved_changes = True  # Mark as unsaved changes

        # Show a dialog indicating the new ACL has been created
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Scroll to the bottom of the page to view the new ACL")
        msg_box.setWindowTitle("New ACL created")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    # Connect the button click to the add_acl slot
    add_acl_button.clicked.connect(add_acl)

    # Function to create a QLineEdit with fixed width
    def create_line_edit(text, parent, width=200):
        line_edit = QLineEdit(text, parent)
        line_edit.setFixedWidth(width)  # Set fixed width
        return line_edit
    
    # Slot function to add a new rule
    def add_rule(acl_name, acl_rules_edit):
        print('Adding rule to ACL: ' + acl_name)
        print(f'Number of rules before new: {len(acl_rules_edit)}')
        dialog = QDialog()
        dialog.setWindowTitle("Add Rule")
        dialog_layout = QVBoxLayout()
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel('Enter the match rule values below'))

        # Create edit fields for each attribute in the Rule class
        fields = {}
        attributes = [
            ('actset_output', int), ('arp_op', int), ('arp_sha', str), ('arp_spa', str), ('arp_tpa', str),
            ('arp_tha', str), ('dl_dst', str), ('dl_src', str), ('dl_type', int), ('dl_vlan', int),
            ('dl_vlan_pcp', int), ('eth_dst', str), ('eth_src', str), ('eth_type', int), ('icmpv4_code', int),
            ('icmpv4_type', int), ('icmpv6_code', int), ('icmpv6_type', int), ('in_phy_port', int), ('in_port', int),
            ('ip_dscp', int), ('ip_ecn', int), ('ip_proto', int), ('ipv4_dst', str), ('ipv4_src', str),
            ('ipv6_dst', str), ('ipv6_exthdr', str), ('ipv6_flabel', int), ('ipv6_nd_sll', str), ('ipv6_nd_target', str),
            ('ipv6_nd_tll', str), ('ipv6_src', str), ('metadata', str), ('mpls_bos', int), ('mpls_label', int),
            ('mpls_tc', int), ('nw_proto', int), ('nw_src', str), ('nw_dst', str), ('nw_tos', int),
            ('packet_type', int), ('pbb_isid', str), ('pbb_uca', int), ('sctp_dst', int), ('sctp_src', int),
            ('tcp_dst', int), ('tcp_flags', int), ('tcp_src', int), ('tp_dst', int), ('tp_src', int),
            ('tunnel_id', str), ('udp_dst', int), ('udp_src', int), ('vlan_pcp', int), ('vlan_vid', int)
]
        # Add the fields to the dialog
        row = 1
        col = 0
        for attr, attr_type in attributes:
            label = QLabel(attr)
            form_layout.addWidget(label, row, col)
            col +=1
            if attr_type == int:
                field = QSpinBox()
                field.setRange(0, 999999)
            else:
                field = QLineEdit()
            form_layout.addWidget(field, row, col)
            col += 1
            fields[attr] = field
            if col == 8:
                col = 0
                row += 1

        dialog_layout.addLayout(form_layout)

        # Add OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        dialog_layout.addWidget(button_box)
        dialog.setLayout(dialog_layout)

        # Handle OK button click
        def on_ok(rules):
            print('OK pressed....')
            rule_data = {}
            for attr, field in fields.items():
                if isinstance(field, QSpinBox):
                    value = field.value()
                else:
                    value = field.text()
                if value:
                    print('attr=' + attr + ' value=' + str(value))
                    rule_data[attr] = value
            
            print(f'Number of rules before adding: {len(rules)}')
            new_rule = Rule(rule_data)
            rules.append(new_rule)
            print(f'Number of rules after adding: {len(rules)}')
            refresh_acls_tab(config, acls_layout, scroll_area)
            dialog.accept()

        button_box.accepted.connect(lambda: on_ok(acl_rules_edit))
        button_box.rejected.connect(dialog.reject)
        print('dialog.exec')
        dialog.exec()
    #_____________________________________________________________________________________________

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
        acl_name_label = QLabel("ACL Name:")
        acl_name_label.setStyleSheet("font-weight: bold;")
        acl_layout.addWidget(acl_name_label, row, 0)
        acl_name_edit = create_line_edit(acl_name, acl_groupbox)
        acl_layout.addWidget(acl_name_edit, row, 1)
        
        # Add 'Add Rule' button next to 'ACL Name' edit field
        add_rule_button = QPushButton("Add Rule")
        acl_layout.addWidget(add_rule_button, row, 2)

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
               
        # Connect the 'Add Rule' button to the add_rule slot
        if not hasattr(acl, 'rules'):
            print('ACL=' + acl_name + ' does not have rules')
        else:
            print('ACL=' + acl_name + ' does have rules')
        if not isinstance(acl, dict):
            print(f"ACL {acl_name} is not a valid ACL dictionary")
        elif 'rules' not in acl: 
            print("ACL {acl_name} does not contain rules: {acl}")
        else:
            print(f"ACL {acl_name} contains rules: {acl['rules']}")
        
        add_rule_button.clicked.connect(lambda _, acl_name=acl_name, rules=acl.rules: add_rule(acl_name, rules))

        #print(f'ACL Name: {acl_name}, Type of acl: {type(acl)}')
        print(f"ACL Name: {acl_name}, ACL Value: {acl}, Type of acl.ruiles: {type(acl.rules)}")

        #add_rule_button.clicked.connect(lambda acl=acl: add_rule(acl.rules))

        rule_cnt = 0
        # Add ACL rules to the form________________________________________________________________________
        for rule in acl.rules:
            rule_cnt += 1
            rule_label = QLabel("Rule " + str(rule_cnt) + ":", alignment=Qt.AlignmentFlag.AlignTop)
            rule_label.setStyleSheet("font-weight: bold;")
            rule_label.setFixedWidth(70)
            acl_layout.addWidget(rule_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)

            rule_groupbox = QGroupBox(acl_groupbox)
            rule_layout = QGridLayout()
            rule_groupbox.setLayout(rule_layout)

            # Ensure the rule_groupbox is aligned to the top-left corner
            acl_layout.addWidget(rule_groupbox, row, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
           
            rule_row = 0  # Initialize rule row counter

            for key, value in rule.__dict__.items():
                if value is not None:
                    # Add the actions on the right of the groupbox
                    if key == 'actions':
                        action_row = 0 # Row to display the action on
                        #rule_layout.addWidget(QLabel(f"{key}:"), 0, 4)
                        item_label = QLabel(f"{key}:")
                        item_label.setStyleSheet("font-weight: bold;")
                        item_label.setFixedWidth(90)
                        rule_layout.addWidget(item_label, action_row, 3)
                        action_row += 1
                        #print(f"actions: {value}")

                        # Display the actions details
                        for ak, av in value.items():
                            if ak == 'allow':
                                value_checkbox = QCheckBox('allow', rule_groupbox)
                                value_checkbox.setChecked(av)
                                rule_layout.addWidget(value_checkbox, action_row, 4)   
                            elif ak == 'force_port_vlan':
                                value_checkbox = QCheckBox('force_port_vlan', rule_groupbox)
                                value_checkbox.setChecked(av)
                                rule_layout.addWidget(value_checkbox, action_row, 4)     
                            elif ak == 'cookie':
                                item_label = QLabel('cookie', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, action_row, 3)
                                value_spinkbox = QSpinBox('cookie', rule_groupbox)
                                value_spinkbox.setRange(0, 999999)
                                value_spinkbox.setValue(av)
                                value_spinkbox.setFixedWidth(90)    
                                rule_layout.addWidget(value_spinkbox, action_row, 4)     
                            elif ak == 'meter':
                                item_label = QLabel('meter', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, action_row, 3)
                                value_edit = QLineEdit(str(av), rule_groupbox)
                                value_edit.setFixedWidth(140)
                                rule_layout.addWidget(value_edit, action_row, 4)      
                            elif ak == 'mirror':
                                item_label = QLabel('mirror', rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, action_row, 3)
                                value_edit = QLineEdit(str(av), rule_groupbox)
                                value_edit.setFixedWidth(140)
                                rule_layout.addWidget(value_edit, action_row, 4)     
                            # Output and ct actions are disctionaries of settings
                            elif isinstance(av, dict):
                                item_label = QLabel(ak, rule_groupbox)
                                item_label.setFixedWidth(90)
                                rule_layout.addWidget(item_label, action_row, 3)
                                # Iterate the settings in the dictionary
                                for ok, ov in av.items():
                                    # Check if the setting is a list
                                    if isinstance(ov, list):
                                        item_label = QLabel(ok, rule_groupbox)
                                        item_label.setFixedWidth(90)
                                        rule_layout.addWidget(item_label, action_row, 4)
                                        for lv in ov:
                                            if isinstance(lv, dict):
                                                for sfk, sfv in lv.items():
                                                    item_label = QLabel(sfk, rule_groupbox)
                                                    item_label.setFixedWidth(90)
                                                    rule_layout.addWidget(item_label, action_row, 5)
                                                    value_edit = QLineEdit(str(sfv), rule_groupbox)
                                                    value_edit.setFixedWidth(120)
                                                    rule_layout.addWidget(value_edit, action_row, 6)    
                                                    action_row += 1
                                            else:                                                
                                                value_edit = QLineEdit(str(lv), rule_groupbox)
                                                value_edit.setFixedWidth(90)
                                                rule_layout.addWidget(value_edit, action_row, 5)     
                                                action_row += 1                                        
                                    else:
                                        item_label = QLabel(ok, rule_groupbox)
                                        item_label.setFixedWidth(90)
                                        rule_layout.addWidget(item_label, action_row, 4)
                                        value_edit = QLineEdit(str(ov), rule_groupbox)
                                        value_edit.setFixedWidth(90)
                                        rule_layout.addWidget(value_edit, action_row, 5)     
                                        action_row += 1                                                  
                    else:
                        item_label = QLabel(f"{key}:", rule_groupbox)
                        item_label.setFixedWidth(90)
                        rule_layout.addWidget(item_label, rule_row, 0)
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

                        # Slot function to update the rule value
                        def update_rule_value(key, edit, rule_edited):
                            if isinstance(edit, QSpinBox) or isinstance(edit, QDoubleSpinBox):
                                #print('update rule key=' + str(key) + ' value=' + str(edit.value()))
                                setattr(rule_edited, key, edit.value())
                            elif isinstance(edit, QCheckBox):
                                setattr(rule_edited, key, edit.isChecked())
                            else:
                                setattr(rule_edited, key, edit.text())
                            globals.unsaved_changes = True  # Mark as unsaved changes

                        # Connect the appropriate signal to the update_rule_value slot
                        if isinstance(value_edit, QSpinBox) or isinstance(value_edit, QDoubleSpinBox):
                            #print('isinstance check key=' + str(key))
                            value_edit.valueChanged.connect(lambda _, key=key, edit=value_edit, rule=rule: update_rule_value(key, edit, rule))
                        elif isinstance(value_edit, QCheckBox):
                            value_edit.stateChanged.connect(lambda _, key=key, edit=value_edit, rule=rule: update_rule_value(key, edit, rule))
                        else:
                            value_edit.textChanged.connect(lambda _, key=key, edit=value_edit, rule=rule: update_rule_value(key, edit, rule))

                    if rule_row == 0:
                        rule_row = 3

            #print('row=' + str(row) + ' rule_row=' + str(rule_row))
            acl_layout.addWidget(rule_groupbox, row, 1, rule_row, 4)
            row += rule_row

        # Add the ACL groupbox to the ACLs layout
        acls_layout.addWidget(acl_groupbox)

    #_____________________________________________________________________________________
    # Add a spacer to push the groupboxes to the top
    acls_layout.addStretch()
    acls_tab.setLayout(acls_layout)
    
    return acls_tab