# dps_tab.py
from PyQt6.QtWidgets import QWidget, QDialog, QGroupBox, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QCheckBox, QSpinBox, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QDoubleSpinBox, QSpacerItem, QSizePolicy, QDialogButtonBox, QComboBox
from PyQt6.QtCore import Qt
from configfile.loader import new_config, ACL, Rule  # Assuming new_config is imported from loader.py
import globals
from models.dp import DP, Interface

DISPLAY_NAMES = {
    'acl_in': 'ACL In',
    'acls_in': 'ACLs In',
    'advertise_interval': 'Advertise Interval',
    'arp_neighbor_timeout': 'ARP Neighbour Timeout',
    'auth_acl': 'Auth ACL',
    'description': 'Description',
    'dot1x': 'Dot1x',
    'dot1x_acl': 'Dot1x ACL',
    'dot1x_assigned': 'Dotlx Assigned',
    'dot1x_mab': 'Dot1x Mab',
    'down_time_multiple': 'Downtime Multiple',
    'dp': 'DP',
    'dp_id': 'DP Id',
    'drop_broadcast_source_address': 'Drop Broadcast Source Address',
    'drop_spoofed_faucet_mac': 'Drop Spoofed Faucet MAC',
    'enable': 'Enable',
    'enabled': 'Enabled',
    'global_vlan': 'Global VLAN',
    'group_table': 'Group Table',
    'hairpin': 'Hairpin',
    'hardware': 'Hardware',
    'high_priority': 'High Priority',
    'highest_priority': 'Highest Priority',
    'ignore_learn_ins': 'Ignore Learn Ins',
    'info': 'Info',
    'learn_ban_timeout': 'Learn Ban Timeout',
    'loop_protect': 'Loop Protect',
    'loop_protect_external': 'Loop Protect External',
    'max_host_fib_retry_count': 'Max Hosr FIB Retry Count',
    'max_hosts': 'Max Hosts',
    'max_hosts_per_resolve_cycle': 'Max Hosts Per Resolve Cycle',
    'max_per_interval': 'Max Per Interval',
    'max_resolve_backoff_time': 'Max Resolve Backoff Seconds',
    'metrics_rate_limit_sec': 'Metric Rate Limit Seconds',
    'min_lacp_health': 'Mon LACP Health',
    'min_stack_health': 'Min Stack Health',
    'mirror': 'Mirror',
    'name': 'Name',
    'native_vlan': 'Native VLAN',
    'nfv_intf': 'NFV Intf',
    'nfv_sw_port': 'NFV SW Port',
    'noauth_acl': 'No Auth ACL',
    'number': 'Number',
    'ofchannel_log': 'Of Channel Log',
    'opstatus_reconf': 'OP Staus Reconf',
    'org_tlvs': 'Org TLVs',
    'oui': 'OUI',
    'output_only': 'Output Only',
    'packetin_pps': 'Packet In PPS',
    'permanent_learn': 'Permanent Learn',
    'port': 'Port',
    'port_descr': 'Port Description',
    'port_table_scale_factor': 'Port Table Scale Factor',
    'priority': 'Priority',
    'priority_offset': 'Priority Offset',
    'proactive_learn_v4': 'Proactive Learn V4',
    'proactive_learn_v6': 'Proactive Learn V6',
    'radius_ip': 'Radius IP',
    'radius_port': 'Radius Port',
    'radius_secret': 'Radius Secret',
    'restricted_bcast_arpnd': 'Restricted BCast ARPND',
    'send_interval': 'Send Interval',
    'slowpath_pps': 'Slowpath PPS',
    'subtype': 'Subtype',
    'system_name': 'System Name',
    'table_sizes': 'Table Sizes',  # Assuming table_sizes is a JSON string
    'tagged_vlans': 'Tagged VLANs',
    'timeout': 'Timeout',
    'unicast_flood': 'Unicast Flood',
    'use_idle_timeout': 'Use Idle Timeout'
}

# Refresh the tab with any changes in the dictionaries
def refresh_dps_tab(config, dps_layout):
    # Clear the existing layout
    #print('refresh_dps_tab ...')
    for i in reversed(range(dps_layout.count())):
        widget = dps_layout.itemAt(i).widget()
        if widget is not None:
            widget.setParent(None)
    # Recreate the DPS tab
    create_dps_tab(config, dps_layout)

# Add a new DP instance
def add_dp(config, dps_tab, dps_layout):
    dialog = QDialog()
    dialog.setWindowTitle("Add DP")
    dialog_layout = QVBoxLayout()
    form_layout = QGridLayout()

    fields = {
        'name': QLineEdit(),
        'advertise_interval': QSpinBox(),
        'arp_neighbor_timeout': QSpinBox(),
        'description': QLineEdit(),
        'dp_id': QSpinBox(),
        'drop_broadcast_source_address': QCheckBox(),
        'drop_spoofed_faucet_mac': QCheckBox(),
        'global_vlan': QSpinBox(),
        'group_table': QCheckBox(),
        'hardware': QLineEdit(),
        'high_priority': QSpinBox(),
        'highest_priority': QSpinBox(),
        'ignore_learn_ins': QSpinBox(),
        'learn_ban_timeout': QSpinBox(),
        'learn_jitter': QSpinBox(),
        'low_priority': QSpinBox(),
        'lowest_priority': QSpinBox(),
        'max_host_fib_retry_count': QSpinBox(),
        'max_hosts_per_resolve_cycle': QSpinBox(),
        'max_resolve_backoff_time': QSpinBox(),
        'metrics_rate_limit_sec': QSpinBox(),
        'ofchannel_log': QLineEdit(),
        'packetin_pps': QSpinBox(),
        'port_table_scale_factor': QDoubleSpinBox(),
        'priority_offset': QSpinBox(),
        'proactive_learn_v4': QCheckBox(),
        'proactive_learn_v6': QCheckBox(),
        'slowpath_pps': QSpinBox(),
        'table_sizes': QLineEdit(),  # Assuming table_sizes is a JSON string
        'timeout': QSpinBox(),
        'use_idle_timeout': QCheckBox()
    }

    # Add the fields to the dialog
    row = 1
    col = 0
    for field, widget in fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(widget, row, col + 1)
        col += 2
        if col == 4:
            col = 0
            row += 1

    dialog_layout.addLayout(form_layout)

    # Add OK and Cancel buttons
    button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    dialog_layout.addWidget(button_box)
    dialog.setLayout(dialog_layout)

    # Handle OK button click
    def on_ok():
        dp_data = {}
        for field, widget in fields.items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                if widget.value() != 0:  # Only add if value is not zero
                    dp_data[field] = widget.value()
            elif isinstance(widget, QCheckBox):
                if widget.isChecked():  # Only add if checkbox is checked
                    dp_data[field] = widget.isChecked()
            else:
                if widget.text():  # Only add if text is not empty
                    dp_data[field] = widget.text()
        dp_data['interfaces'] = {}
        new_dp = DP(**dp_data)
        config.dps[new_dp.name] = new_dp
        globals.unsaved_changes = True
        refresh_dps_tab(config, dps_layout)
        dialog.accept()

        # Show a dialog indicating the new ACL has been created
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Scroll to the bottom of the page to view the new DP")
        msg_box.setWindowTitle("New DP created")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    button_box.accepted.connect(on_ok)
    button_box.rejected.connect(dialog.reject)
    dialog.exec()

# Edit the current DP showing all possible settings
def edit_dp(config, dp, dps_layout):
    dialog = QDialog()
    dialog.setWindowTitle("Edit DP")
    dialog_layout = QVBoxLayout()
    form_layout = QGridLayout()

    fields = {
        'name': QLineEdit(),
        'advertise_interval': QSpinBox(),
        'arp_neighbor_timeout': QSpinBox(),
        'description': QLineEdit(),
        'dp_id': QSpinBox(),
        'drop_broadcast_source_address': QCheckBox(),
        'drop_spoofed_faucet_mac': QCheckBox(),
        'global_vlan': QSpinBox(),
        'group_table': QCheckBox(),
        'hardware': QLineEdit(),
        'high_priority': QSpinBox(),
        'highest_priority': QSpinBox(),
        'ignore_learn_ins': QSpinBox(),
        'learn_ban_timeout': QSpinBox(),
        'learn_jitter': QSpinBox(),
        'low_priority': QSpinBox(),
        'lowest_priority': QSpinBox(),
        'max_host_fib_retry_count': QSpinBox(),
        'max_hosts_per_resolve_cycle': QSpinBox(),
        'max_resolve_backoff_time': QSpinBox(),
        'metrics_rate_limit_sec': QSpinBox(),
        'ofchannel_log': QLineEdit(),
        'packetin_pps': QSpinBox(),
        'port_table_scale_factor': QDoubleSpinBox(),
        'priority_offset': QSpinBox(),
        'proactive_learn_v4': QCheckBox(),
        'proactive_learn_v6': QCheckBox(),
        'slowpath_pps': QSpinBox(),
        'table_sizes': QLineEdit(),  # Assuming table_sizes is a JSON string
        'timeout': QSpinBox(),
        'use_idle_timeout': QCheckBox()
    }

    # Populate the fields with the current DP values
    for field, widget in fields.items():
        if hasattr(dp, field):
            value = getattr(dp, field)
            if value is None:
                if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                    value = 0
                elif isinstance(widget, QCheckBox):
                    value = False
                else:
                    value = ""

            if isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)


    # Add the fields to the dialog
    row = 1
    col = 0
    for field, widget in fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(widget, row, col + 1)
        col += 2
        if col >= 4:  # Move to next row after 2 attributes
            col = 0
            row += 1

    # Initialize dot1x dictionary if it doesn't exist
    if not hasattr(dp, 'dot1x') or not isinstance(dp.dot1x, dict):
        dp.dot1x = {
            'nfv_intf': '',
            'nfv_sw_port': 0,
            'radius_ip': '',
            'radius_port': 0,
            'radius_secret': '',
            'noauth_acl': '',
            'auth_acl': '',
            'dot1x_assigned': False
        }

    # Create dot1x group box and layout
    dot1x_group_box = QGroupBox("Dot1x")
    dot1x_layout = QGridLayout()
    dot1x_fields = {
        'nfv_intf': QLineEdit(),
        'nfv_sw_port': QSpinBox(),
        'radius_ip': QLineEdit(),
        'radius_port': QSpinBox(),
        'radius_secret': QLineEdit(),
        'noauth_acl': QLineEdit(),
        'auth_acl': QLineEdit(),
        'dot1x_assigned': QCheckBox()
    }

    # Populate the dot1x fields with the current DP values
    dot1x = dp.dot1x
    for field, widget in dot1x_fields.items():
        if field in dot1x:
            value = dot1x[field]
            if value is None:
                if isinstance(widget, QSpinBox):
                    value = 0
                elif isinstance(widget, QCheckBox):
                    value = False
                else:
                    value = ""

            if isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)

    # Add the dot1x fields to the dot1x layout
    row+=1
    dot1x_row = 0
    dot1x_col = 0
    for field, widget in dot1x_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        dot1x_layout.addWidget(label, dot1x_row, dot1x_col)
        dot1x_layout.addWidget(widget, dot1x_row, dot1x_col + 1)
        dot1x_col += 2
        if dot1x_col >= 4:  # Move to next row after 2 attributes
            dot1x_col = 0
            dot1x_row += 1

    dot1x_group_box.setLayout(dot1x_layout)
    form_layout.addWidget(dot1x_group_box, row, 0, 1, 4)

    dialog_layout.addLayout(form_layout)

    # Initialize lldp_beacon dictionary if it doesn't exist
    if not hasattr(dp, 'lldp_beacon') or not isinstance(dp.lldp_beacon, dict):
        dp.lldp_beacon = {
            'system_name': '',
            'send_interval': 0,
            'max_per_interval': 0
        }

    # Create lldp group box and layout
    lldp_group_box = QGroupBox("lldp")
    lldp_layout = QGridLayout()
    lldp_fields = {
        'system_name': QLineEdit(),
        'send_interval': QSpinBox(),
        'max_per_interval': QSpinBox()
    }

    # Populate the lldp fields with the current DP values
    lldp_beacon = dp.lldp_beacon
    for field, widget in lldp_fields.items():
        if field in lldp_beacon:
            value = lldp_beacon[field]
            if value is None:
                if isinstance(widget, QSpinBox):
                    widget.setRange(0, 9999)
                    value = 0
                else:
                    value = ""

            if isinstance(widget, QLineEdit):
                widget.setText(str(value))
                widget.setMaximumWidth(200)
            elif isinstance(widget, QSpinBox):
                widget.setRange(0, 9999)
                widget.setValue(value)

    # Add the lldp fields to the lldp layout
    row += 1
    lldp_row = 0
    lldp_col = 0
    for field, widget in lldp_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        lldp_layout.addWidget(label, lldp_row, lldp_col)
        lldp_layout.addWidget(widget, lldp_row, lldp_col + 1)
        lldp_col += 2
        if lldp_col >= 4:  # Move to next row after 2 attributes
            lldp_col = 0
            lldp_row += 1

    lldp_group_box.setLayout(lldp_layout)
    form_layout.addWidget(lldp_group_box, row + 1, 0, 1, 4)
    row += 1
    dialog_layout.addLayout(form_layout)

    # Initialize stack dictionary if it doesn't exist
    if not hasattr(dp, 'stack') or not isinstance(dp.stack, dict):
        dp.stack = {
            'priority': 0,
            'down_time_multiple': 0,
            'min_stack_health': 0.0,
            'min_lacp_health': 0.0
        }

    # Create stack group box and layout
    stack_group_box = QGroupBox("stack")
    stack_layout = QGridLayout()
    stack_fields = {
        'priority': QSpinBox(),
        'down_time_multiple': QSpinBox(),
        'min_stack_health': QDoubleSpinBox(),
        'min_lacp_health': QDoubleSpinBox()
    }

    # Populate the stack fields with the current DP values
    stack = dp.stack
    for field, widget in stack_fields.items():
        if field in stack:
            value = stack[field]
            if value is None:
                if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                    value = 0
                else:
                    value = ""

            if isinstance(widget, QLineEdit):
                widget.setMaximumWidth(200)
                widget.setText(str(value))
            elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                widget.setRange(0, 9999)
                widget.setValue(value)

    # Add the stack fields to the stack layout
    row += 5
    stack_row = 0
    stack_col = 0
    for field, widget in stack_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        stack_layout.addWidget(label, stack_row, stack_col)
        stack_layout.addWidget(widget, stack_row, stack_col + 1)
        stack_col += 2
        if stack_col >= 4:  # Move to next row after 2 attributes
            stack_col = 0
            stack_row += 1

    stack_group_box.setLayout(stack_layout)
    form_layout.addWidget(stack_group_box, row, 0, 1, 4)

    dialog_layout.addLayout(form_layout)

    # Add OK and Cancel buttons
    button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    button_box.accepted.connect(lambda: save_dp_changes(dialog, fields, dot1x_fields, lldp_fields, stack_fields, dp, config, dps_layout))
    button_box.rejected.connect(dialog.reject)
    dialog_layout.addWidget(button_box)

    dialog.setLayout(dialog_layout)
    dialog.exec()

# Save any changes made on the DP edit form
def save_dp_changes(dialog, fields, dot1x_fields, lldp_fields, stack_fields, dp, config, dps_layout):
    changes_made = False

    for field, widget in fields.items():
        if isinstance(widget, QLineEdit):
            new_value = widget.text()
            if getattr(dp, field) is not None and getattr(dp, field) != new_value:
                setattr(dp, field, new_value)
                changes_made = True
            elif getattr(dp, field) is None and new_value:
                setattr(dp, field, new_value)
                changes_made = True
        elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
            new_value = widget.value()
            if getattr(dp, field) is not None and new_value != 0 and getattr(dp, field) != new_value:
                setattr(dp, field, new_value)
                changes_made = True
            elif getattr(dp, field) is None and new_value > 0:
                setattr(dp, field, new_value)
                changes_made = True
        elif isinstance(widget, QCheckBox):
            new_value = widget.isChecked()
            if getattr(dp, field) is not None and getattr(dp, field) != new_value:
                setattr(dp, field, new_value)
                changes_made = True
            elif getattr(dp, field) is None and new_value == 1:
                #print(field + 'Boolean new_value=' + str(new_value))
                setattr(dp, field, new_value)
                changes_made = True

    # Save changes for dot1x fields
    if hasattr(dp, 'dot1x') and isinstance(dp.dot1x, dict):
        dot1x = dp.dot1x
        for field, widget in dot1x_fields.items():
            if isinstance(widget, QLineEdit):
                new_value = widget.text()
                if field in dot1x and dot1x[field] is not None and new_value and dot1x[field] != new_value:
                    dot1x[field] = new_value
                    changes_made = True
                elif (field not in dot1x or dot1x[field] is None) and new_value:
                    dot1x[field] = new_value
                    changes_made = True
            elif isinstance(widget, QSpinBox):
                new_value = widget.value()
                if field in dot1x and dot1x[field] is not None and new_value and dot1x[field] != new_value:
                    dot1x[field] = new_value
                    changes_made = True
                elif (field not in dot1x or dot1x[field] is None)  and new_value > 0:
                    dot1x[field] = new_value
                    changes_made = True
            elif isinstance(widget, QCheckBox):
                new_value = widget.isChecked()
                if field in dot1x and dot1x[field] is not None and dot1x[field] != new_value:
                    dot1x[field] = new_value
                    changes_made = True
                elif (field not in dot1x or dot1x[field] is None)  and new_value == 1:
                    dot1x[field] = new_value
                    changes_made = True

    # Save changes for lldp fields
    if hasattr(dp, 'lldp_beacon') and isinstance(dp.lldp_beacon, dict):
        lldp = dp.lldp_beacon
        for field, widget in lldp_fields.items():
            if isinstance(widget, QLineEdit):
                new_value = widget.text()
                if field in lldp and lldp[field] is not None and new_value and lldp[field] != new_value:
                    lldp[field] = new_value
                    changes_made = True
                elif (field not in lldp or lldp[field] is None) and new_value:
                    lldp[field] = new_value
                    changes_made = True
            elif isinstance(widget, QSpinBox):
                new_value = widget.value()
                if field in lldp and lldp[field] is not None and new_value and lldp[field] != new_value:
                    lldp[field] = new_value
                    changes_made = True
                elif (field not in lldp or lldp[field] is None)  and new_value > 0:
                    lldp[field] = new_value
                    changes_made = True
            elif isinstance(widget, QCheckBox):
                new_value = widget.isChecked()
                if field in lldp and lldp[field] is not None and lldp[field] != new_value:
                    lldp[field] = new_value
                    changes_made = True
                elif (field not in lldp or lldp[field] is None)  and new_value == 1:
                    lldp[field] = new_value
                    changes_made = True

    # Save changes for stack fields
    if hasattr(dp, 'stack') and isinstance(dp.stack, dict):
        stack = dp.stack
        for field, widget in stack_fields.items():
            if isinstance(widget, QLineEdit):
                new_value = widget.text()
                if field in stack and stack[field] is not None and new_value and stack[field] != new_value:
                    stack[field] = new_value
                    changes_made = True
                elif (field not in stack or stack[field] is None) and new_value:
                    stack[field] = new_value
                    changes_made = True
            elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                new_value = widget.value()
                if field in stack and stack[field] is not None and new_value and stack[field] != new_value:
                    stack[field] = new_value
                    changes_made = True
                elif (field not in stack or stack[field] is None) and new_value > 0:
                    stack[field] = new_value
                    changes_made = True

    if changes_made:
        globals.unsaved_changes = True

    dialog.accept()
    refresh_dps_tab(config, dps_layout)

# Edit an existing Interface definition
def show_edit_interface_dialog(config, dp, dps_layout, interface):
    dialog = QDialog()
    dialog.setWindowTitle("Edit Interface")
    dialog_layout = QVBoxLayout()

    form_layout = QGridLayout()

    fields = {
        #'acl_in': QLineEdit(),
        'name': QLineEdit(),
        'description': QLineEdit(),
        'acls_in': QLineEdit(),
        'dot1x': QCheckBox(),
        'dot1x_acl': QCheckBox(),
        'dot1x_mab': QCheckBox(),
        'enabled': QCheckBox(),
        'hairpin': QCheckBox(),
        'loop_protect': QCheckBox(),
        'loop_protect_external': QCheckBox(),
        'max_hosts': QSpinBox(),
        'mirror': QLineEdit(),
        'native_vlan': QLineEdit(),
        'number': QSpinBox(),
        'opstatus_reconf': QCheckBox(),
        'output_only': QCheckBox(),
        'permanent_learn': QCheckBox(),
        'tagged_vlans': QLineEdit(),
        'unicast_flood': QCheckBox(),
        'restricted_bcast_arpnd': QCheckBox()
    }

    row = 2
    col = 0
    for field, widget in fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        form_layout.addWidget(label, row, col)

        #print('Field=' + field)
        if isinstance(widget, QLineEdit):
            value = getattr(interface, field, "")
            if isinstance(value, list):
                # If its a list comma separate it
                value = ", ".join(map(str, value))
            widget.setText(value)
            if field == 'acls_in' or field == 'description':
                widget.setMinimumWidth(200)
        elif isinstance(widget, QCheckBox):
            value = getattr(interface, field, 0)            
            widget.setChecked(False)
            # if value == "" or value == "0":
            #     widget.setChecked(False)
            # else:
            #     widget.setChecked(True)
        elif isinstance(widget, QSpinBox):
            value = getattr(interface, field, 0)
            if value is None:
                value = 0
            widget.setValue(value)
            
        form_layout.addWidget(widget, row, col + 1)
        col += 2
        if col >= 4 or field == 'acls_in' or field == 'description':
            col = 0
            row += 1
    row += 1
    # Create lldp_beacon group box and layout
    lldp_beacon_group_box = QGroupBox("LLDP")
    lldp_beacon_layout = QGridLayout()
    lldp_beacon_fields = {
        'enable': QCheckBox(),
        #'org_tlvs': QLineEdit(),
        'port_descr': QLineEdit(),
        'system_name': QLineEdit()
    }

    lldp_row = 0
    lldp_col = 0
    for field, widget in lldp_beacon_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        lldp_beacon_layout.addWidget(label, lldp_row, lldp_col)

        # Populate the widget from the interface.lldp_beacon field
        lldp_beacon = getattr(interface, 'lldp_beacon', {})
        if field in lldp_beacon:
            value = lldp_beacon[field]
            
            if isinstance(widget, QLineEdit):
                widget.setText(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)

        lldp_beacon_layout.addWidget(widget, lldp_row, lldp_col + 1)
        lldp_col += 2
        if lldp_col >= 4:
            lldp_col = 0
            lldp_row += 1

    lldp_beacon_group_box.setLayout(lldp_beacon_layout)
    form_layout.addWidget(lldp_beacon_group_box, row, 0, 1, 4)

    # Create org_tlvs group box and layout
    lldp_beacon = getattr(interface, 'lldp_beacon', {})
    org_tlvs_list = lldp_beacon.get('org_tlvs', None)

    if org_tlvs_list is None:
        # Display a single TLV group box if org_tlvs is None
        org_tlvs_group_box = QGroupBox("TLV")
        org_tlvs_layout = QGridLayout()
        org_tlvs_fields = {
            'info': QLineEdit(),
            'oui': QSpinBox(),
            'subtype': QSpinBox()
        }

        org_tlvs_row = 0
        org_tlvs_col = 0
        for field, widget in org_tlvs_fields.items():
            # Lookup display name for the attribute
            display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
            label = QLabel(display_name)
            org_tlvs_layout.addWidget(label, org_tlvs_row, org_tlvs_col)
            org_tlvs_layout.addWidget(widget, org_tlvs_row, org_tlvs_col + 1)
            if isinstance(widget, QLineEdit):
                widget.setMaximumWidth(120)
            elif isinstance(widget, QSpinBox):
                widget.setRange(0, 9999)
            org_tlvs_col += 2

        org_tlvs_group_box.setLayout(org_tlvs_layout)
        lldp_row += 1
        lldp_beacon_layout.addWidget(org_tlvs_group_box, lldp_row, 0, 1, 4)
    else:
        # Create a TLV group box for each item in the org_tlvs list
        for tlv in org_tlvs_list:
            org_tlvs_group_box = QGroupBox("TLV")
            org_tlvs_layout = QGridLayout()
            org_tlvs_fields = {
                'info': QLineEdit(),
                'oui': QSpinBox(),
                'subtype': QSpinBox()
            }

            org_tlvs_row = 0
            org_tlvs_col = 0
            for field, widget in org_tlvs_fields.items():
                # Lookup display name for the attribute
                display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
                label = QLabel(display_name)
                org_tlvs_layout.addWidget(label, org_tlvs_row, org_tlvs_col)
                
                if isinstance(widget, QLineEdit):
                    widget.setMaximumWidth(120)
                elif isinstance(widget, QSpinBox):
                    widget.setRange(0, 9999)

                if field in tlv:
                    value = tlv[field]
                    if isinstance(widget, QLineEdit):
                        widget.setText(value)
                    elif isinstance(widget, QSpinBox):
                        widget.setValue(value)
                org_tlvs_layout.addWidget(widget, org_tlvs_row, org_tlvs_col + 1)
                org_tlvs_col += 2

            org_tlvs_group_box.setLayout(org_tlvs_layout)
            lldp_row += 1
            lldp_beacon_layout.addWidget(org_tlvs_group_box, lldp_row, 0, 1, 4)
            lldp_row += 1

    # Create stack group box and layout
    stack_group_box = QGroupBox("stack")
    stack_layout = QGridLayout()
    stack_fields = {
        'dp': QLineEdit(),
        'port': QLineEdit()
    }

    stack_row = 0
    stack_col = 0
    for field, widget in stack_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        stack_layout.addWidget(label, stack_row, stack_col)
        stack_layout.addWidget(widget, stack_row, stack_col + 1)
        stack_col += 2
        if stack_col >= 4:
            stack_col = 0
            stack_row += 1

    stack_group_box.setLayout(stack_layout)
    form_layout.addWidget(stack_group_box, row + 1, 0, 1, 4)

    dialog_layout.addLayout(form_layout)

    # Add OK and Cancel buttons
    button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    button_box.accepted.connect(lambda: save_interface_changes(dialog, dp, fields, lldp_beacon_fields, org_tlvs_fields, stack_fields, config, dps_layout, interface))
    button_box.rejected.connect(dialog.reject)
    dialog_layout.addWidget(button_box)

    dialog.setLayout(dialog_layout)
    dialog.exec()

# Add an new Interface definition
def show_add_interface_dialog(config, dp, dps_layout):
    dialog = QDialog()
    dialog.setWindowTitle("Add Interface")
    dialog_layout = QVBoxLayout()

    form_layout = QGridLayout()

    fields = {
        #'acl_in': QLineEdit(),
        'acls_in': QLineEdit(),
        'description': QLineEdit(),
        'dot1x': QCheckBox(),
        'dot1x_acl': QCheckBox(),
        'dot1x_mab': QCheckBox(),
        'enabled': QCheckBox(),
        'hairpin': QCheckBox(),
        'loop_protect': QCheckBox(),
        'loop_protect_external': QCheckBox(),
        'max_hosts': QSpinBox(),
        'mirror': QLineEdit(),
        'name': QLineEdit(),
        'native_vlan': QLineEdit(),
        'number': QSpinBox(),
        'opstatus_reconf': QCheckBox(),
        'output_only': QCheckBox(),
        'permanent_learn': QCheckBox(),
        'tagged_vlans': QLineEdit(),
        'unicast_flood': QCheckBox(),
        'restricted_bcast_arpnd': QCheckBox()
    }

    row = 2
    col = 0
    for field, widget in fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(widget, row, col + 1)
        col += 2
        if col >= 4:
            col = 0
            row += 1
    row += 1
    # Create lldp_beacon group box and layout
    lldp_beacon_group_box = QGroupBox("lldp_beacon")
    lldp_beacon_layout = QGridLayout()
    lldp_beacon_fields = {
        'enable': QCheckBox(),
        'org_tlvs': QLineEdit(),
        'port_descr': QLineEdit(),
        'system_name': QLineEdit()
    }

    lldp_row = 0
    lldp_col = 0
    for field, widget in lldp_beacon_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        lldp_beacon_layout.addWidget(label, lldp_row, lldp_col)
        lldp_beacon_layout.addWidget(widget, lldp_row, lldp_col + 1)
        lldp_col += 2
        if lldp_col >= 4:
            lldp_col = 0
            lldp_row += 1

    lldp_beacon_group_box.setLayout(lldp_beacon_layout)
    form_layout.addWidget(lldp_beacon_group_box, row, 0, 1, 4)

    # Create org_tlvs group box and layout
    org_tlvs_group_box = QGroupBox("org_tlvs")
    org_tlvs_layout = QGridLayout()
    org_tlvs_fields = {
        'info': QLineEdit(),
        'oui': QSpinBox(),
        'subtype': QSpinBox()
    }

    org_tlvs_row = 0
    org_tlvs_col = 0
    for field, widget in org_tlvs_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        org_tlvs_layout.addWidget(label, org_tlvs_row, org_tlvs_col)
        org_tlvs_layout.addWidget(widget, org_tlvs_row, org_tlvs_col + 1)
        if isinstance(widget, QLineEdit):
            widget.setMaximumWidth(200)
        elif isinstance(widget, QSpinBox):
            widget.setRange(0, 9999)
        org_tlvs_col += 2
        if org_tlvs_col >= 4:
            org_tlvs_col = 0
            org_tlvs_row += 1

    org_tlvs_group_box.setLayout(org_tlvs_layout)
    lldp_beacon_layout.addWidget(org_tlvs_group_box, lldp_row, 0, 1, 4)

    # Create stack group box and layout
    stack_group_box = QGroupBox("stack")
    stack_layout = QGridLayout()
    stack_fields = {
        'dp': QLineEdit(),
        'port': QLineEdit()
    }

    stack_row = 0
    stack_col = 0
    for field, widget in stack_fields.items():
        # Lookup display name for the attribute
        display_name = DISPLAY_NAMES.get(field, field)  # Fallback to attr if not found
        label = QLabel(display_name)
        stack_layout.addWidget(label, stack_row, stack_col)
        stack_layout.addWidget(widget, stack_row, stack_col + 1)
        stack_col += 2
        if stack_col >= 4:
            stack_col = 0
            stack_row += 1

    stack_group_box.setLayout(stack_layout)
    form_layout.addWidget(stack_group_box, row + 1, 0, 1, 4)

    dialog_layout.addLayout(form_layout)

    # Add OK and Cancel buttons
    button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    button_box.accepted.connect(lambda: save_interface_changes(dialog, dp, fields, lldp_beacon_fields, org_tlvs_fields, stack_fields, config, dps_layout))
    button_box.rejected.connect(dialog.reject)
    dialog_layout.addWidget(button_box)

    dialog.setLayout(dialog_layout)
    dialog.exec()

# Save the new interface created or update the edits of an existing
def save_interface_changes(dialog, dp, fields, lldp_beacon_fields, org_tlvs_fields, stack_fields, config, dps_layout, existing_interface=None):
    if existing_interface:
        interface = existing_interface
    else:
        next_key = str(max(dp.interfaces.keys(), default=0) + 1)
        interface = Interface(name=next_key)
    
    for field, widget in fields.items():
        if isinstance(widget, QLineEdit):
            if widget.text():
                setattr(interface, field, widget.text())
        elif isinstance(widget, QSpinBox):
            if widget.value() > 0:
                setattr(interface, field, widget.value())
        elif isinstance(widget, QCheckBox):
            if widget.isChecked() == True:
                setattr(interface, field, widget.isChecked())

    interface.lldp_beacon = {}
    for field, widget in lldp_beacon_fields.items():
        if isinstance(widget, QLineEdit):
            if widget.text():
                interface.lldp_beacon[field] = widget.text()
        elif isinstance(widget, QCheckBox):
            if widget.isChecked() == True:
                interface.lldp_beacon[field] = widget.isChecked()

    org_tlv = {}
    add_org_tlvs = False
    for field, widget in org_tlvs_fields.items():
        if isinstance(widget, QLineEdit):
            if widget.text():
                org_tlv[field] = widget.text()
                add_org_tlvs = True
        elif isinstance(widget, QSpinBox):
            if widget.value() > 0:
                org_tlv[field] = widget.value()
                add_org_tlvs = True
    if add_org_tlvs:
        interface.lldp_beacon['org_tlvs'] = [org_tlv]

    interface.stack = {}
    for field, widget in stack_fields.items():
        if isinstance(widget, QLineEdit):
            if widget.text():
                interface.stack[field] = widget.text()

    if not hasattr(dp, 'interfaces'):
        dp.interfaces = {}

    # If this is a new interface
    if not existing_interface:
        # Find the next available integer key for the new interface
        #next_key = max(dp.interfaces.keys(), default=0) + 1
        dp.interfaces[next_key] = interface

    globals.unsaved_changes = True
    refresh_dps_tab(config, dps_layout)
    dialog.accept()

# Delete the selected DP
def show_delete_dialog(config, dp_name, dps_layout):
    delete_dialog = QDialog()
    delete_dialog.setWindowTitle("Delete DP")
    delete_layout = QVBoxLayout()
    delete_label = QLabel("Press OK to delete DP")
    delete_layout.addWidget(delete_label)

    button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    button_box.accepted.connect(lambda: delete_dp(config, dp_name, dps_layout, delete_dialog))
    button_box.rejected.connect(delete_dialog.reject)
    delete_layout.addWidget(button_box)

    delete_dialog.setLayout(delete_layout)
    delete_dialog.exec()

def delete_dp(config, dp_name, dps_layout, delete_dialog):
    if dp_name in config.dps:
        del config.dps[dp_name]
        globals.unsaved_changes = True
        refresh_dps_tab(config, dps_layout)
    delete_dialog.accept()

# Delete the current inrterface
def delete_interface(config, dp, iface_key, dps_layout):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Delete Interface")
    msg_box.setText("Press OK to delete this interface")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)

    ret = msg_box.exec()
    if ret == QMessageBox.StandardButton.Ok:
        del dp.interfaces[iface_key]
        globals.unsaved_changes = True
        refresh_dps_tab(config, dps_layout)        

# Function to add a new TLV
def add_tlv(lldp_beacon, config, dps_layout):
    dialog = QDialog()
    dialog.setWindowTitle("Add TLV")
    layout = QVBoxLayout()

    # Info field
    info_label = QLabel("Info:")
    info_input = QLineEdit()
    layout.addWidget(info_label)
    layout.addWidget(info_input)

    # OUI field
    oui_label = QLabel("OUI:")
    oui_input = QSpinBox()
    oui_input.setRange(0, 999999)
    layout.addWidget(oui_label)
    layout.addWidget(oui_input)

    # Subtype field
    subtype_label = QLabel("Subtype:")
    subtype_input = QSpinBox()
    subtype_input.setRange(0, 255)
    layout.addWidget(subtype_label)
    layout.addWidget(subtype_input)

    # OK and Cancel buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    dialog.setLayout(layout)

    def on_ok():
        new_tlv = {
            "info": info_input.text(),
            "oui": oui_input.value(),
            "subtype": subtype_input.value()
        }
        #print(f'lldp_beacon={lldp_beacon}')
        lldp_beacon['org_tlvs'].append(new_tlv)
        dialog.accept()
        refresh_dps_tab(config, dps_layout)

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(dialog.reject)

    dialog.exec()

# Create the DPS tab.................
def create_dps_tab(config, dps_layout=None):
    if dps_layout is None:
        #print('layout is none')
        dps_tab = QWidget()
        dps_layout = QVBoxLayout()
        dps_tab.setLayout(dps_layout)
    else:
        #print('using parent widget')
        dps_tab = dps_layout.parentWidget()

    # For each DP in DPS
    for name, dp in config.dps.items():
        group_box = QGroupBox(f"{name}")
        group_box.setStyleSheet("QGroupBox { font-size: 12pt; font-weight: bold; }")
        group_box.setFixedWidth(800)  # Set a fixed width for the group box
        grid_layout = QGridLayout()

        # Add DP button
        add_dp_button = QPushButton("Add DP")
        add_dp_button.setFixedWidth(200)
        add_dp_button.clicked.connect(lambda: add_dp(config, dps_tab, dps_layout))
        dps_layout.addWidget(add_dp_button)

        # Add the edit_dp button
        edit_dp_button = QPushButton("Edit DP")
        edit_dp_button.clicked.connect(lambda _, dp=dp: edit_dp(config, dp, dps_layout))
        grid_layout.addWidget(edit_dp_button, 0, 0, 1, 1)  # Add the button to the top row
        
        # Add the add interface button
        add_interface_button = QPushButton("Add Interface")
        add_interface_button.clicked.connect(lambda _, dp=dp: show_add_interface_dialog(config, dp, dps_layout))
        grid_layout.addWidget(add_interface_button, 0, 1, 1, 1)  # Add the button to the top row

        # Add a button to delete the current DP
        delete_dp_button = QPushButton("Delete DP")
        delete_dp_button.clicked.connect(lambda _, dp_name=name: show_delete_dialog(config, dp_name, dps_layout))
        grid_layout.addWidget(delete_dp_button, 0, 3, 1, 1)  # Add the button to the top row

        # Add QLineEdit for DP name
        name_label = QLabel("DP Name")
        name_label.setStyleSheet("font-weight: bold;")
        name_label.setFixedWidth(150)
        name_edit = QLineEdit(name)
        name_edit.setFixedWidth(200)
        name_edit.textChanged.connect(lambda text, gb=group_box: gb.setTitle(text))
        grid_layout.addWidget(name_label, 1, 0)
        grid_layout.addWidget(name_edit, 1, 1)
        
        # Functions to update the DP dictionary if user makes an edit
        def update_dp_bool(dp, attr, state):
            dp.__dict__[attr] = bool(state)
            globals.unsaved_changes = True

        def update_dp_int(dp, attr, value):
            dp.__dict__[attr] = int(value)
            globals.unsaved_changes = True

        def update_dp_float(dp, attr, value):
            dp.__dict__[attr] = float(value)
            globals.unsaved_changes = True

        def update_dp_str(dp, attr, text):
            dp.__dict__[attr] = text
            globals.unsaved_changes = True

        row = 2
        col = 0        
        # For each attribute in the DP
        for attr, value in dp.__dict__.items():
            if value is not None and value != [] and value != {}:
                #print('attr=' + attr, type(value))
                # Handle the DP dictionary attributes in their own sub-groupboxes
                if attr == 'interfaces' and isinstance(value, dict):
                    row += 1
                    interfaces_label = QLabel("Interfaces")
                    interfaces_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(interfaces_label, row, 0, 1, 2)
                    #print(f'value={value}')
                    
                    for iface_name, iface in value.items():
                        iface_group_box = QGroupBox(str(iface_name)) 
                        iface_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                        #iface_group_box.setFixedWidth(750)
                        iface_layout = QGridLayout()                         

                        # Add Edit Interface button
                        edit_iface_button = QPushButton("Edit Interface")
                        iface_layout.addWidget(edit_iface_button, 0, 0, 1, 2)
                        edit_iface_button.clicked.connect(lambda _, dp=dp, iface=iface: show_edit_interface_dialog(config, dp, dps_layout, iface))                   

                        delete_iface_button = QPushButton("Delete Interface")
                        iface_layout.addWidget(delete_iface_button, 0, 2, 1, 2)
                        delete_iface_button.clicked.connect(lambda _, dp=dp, iface_key=iface_name: delete_interface(config, dp, iface_key, dps_layout))

                        iface_row = 1
                        iface_col = 0
                        for iface_attr, iface_value in iface.__dict__.items():
                            # Exclude empty items

                            if iface_value is not None and iface_value != [] and iface_value != {}:
                                # Lookup display name for the attribute
                                display_name = DISPLAY_NAMES.get(iface_attr, iface_attr)  # Fallback to attr if not found
                                iface_label = QLabel(display_name)
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
                                    iface_row += 1
                                    #print(f'lldp_beacon value={iface_value}')
                                    lldp_group_box = QGroupBox("LLDP")
                                    lldp_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                                    lldp_layout = QGridLayout()
                                    lldp_row = 0
                                    lldp_col = 0

                                    # Add "Add TLV" button
                                    add_tlv_button = QPushButton("Add TLV")
                                    add_tlv_button.clicked.connect(lambda _, lldp_beacon=iface_value, config=config, dps_layout=dps_layout: add_tlv(lldp_beacon, config, dps_layout))
                                    lldp_layout.addWidget(add_tlv_button, lldp_row, lldp_col, 1, 2)
                                    lldp_row += 1

                                    for lldp_attr, lldp_value in iface_value.items():
                                        #if lldp_attr == 'org_tlvs':
                                            # print(f'org_tlvs value={lldp_value}')
                                            # print('attr=' + lldp_attr, type(lldp_value))
                                        # Lookup display name for the attribute
                                        if lldp_attr != 'org_tlvs':
                                            display_name = DISPLAY_NAMES.get(lldp_attr, lldp_attr)  # Fallback to attr if not found
                                            lldp_attr_label = QLabel(display_name)
                                        if isinstance(lldp_value, bool):
                                            lldp_widget = QCheckBox()
                                            lldp_widget.setChecked(lldp_value)
                                            lldp_widget.stateChanged.connect(lambda state, iface_value=iface_value, a=lldp_attr: update_lldp_bool(iface_value, a, state))
                                        elif isinstance(lldp_value, int):
                                            lldp_widget = QSpinBox()
                                            lldp_widget.setRange(0,9999)
                                            lldp_widget.setValue(lldp_value)
                                            lldp_widget.valueChanged.connect(lambda val, iface_value=iface_value, a=lldp_attr: update_lldp_int(iface_value, a, val))
                                        elif isinstance(lldp_value, float):
                                            lldp_widget = QDoubleSpinBox()
                                            lldp_widget = QSpinBox()
                                            lldp_widget.setRange(0,9999)
                                            lldp_widget.setValue(lldp_value)
                                            lldp_widget.valueChanged.connect(lambda val, iface_value=iface_value, a=lldp_attr: update_lldp_float(iface_value, a, val))
                                        elif isinstance(lldp_value, str):
                                            lldp_widget = QLineEdit()
                                            lldp_widget.setText(lldp_value)
                                            lldp_widget.setFixedWidth(200)
                                            lldp_widget.textChanged.connect(lambda text, iface_value=iface_value, a=lldp_attr: update_lldp_str(iface_value, a, text))
                                        elif isinstance(lldp_value, list) and lldp_attr == 'org_tlvs':
                                            # print('Starting org_tlvs')
                                            for tlv_index, tlv in enumerate(lldp_value):
                                                if lldp_col > 0:
                                                    lldp_col = 0
                                                    lldp_row += 1
                                                tlv_group_box = QGroupBox("TLV")
                                                tlv_layout = QGridLayout()
                                                tlv_row = 0
                                                tlv_col = 0                                               

                                                # Function to delete TLV and refresh the tab
                                                def delete_tlv(lldp_value, tlv_index):
                                                    del lldp_value[tlv_index]                                
                                                    refresh_dps_tab(config, dps_layout)

                                                # Add Delete TLV button
                                                delete_button = QPushButton("Delete TLV")
                                                delete_button.clicked.connect(lambda _, f=lldp_value, i=tlv_index: delete_tlv(f, i))
                                                tlv_layout.addWidget(delete_button, tlv_row, tlv_col, 1, 2)
                                                tlv_row += 1

                                                for tlv_attr, tlv_value in tlv.items():
                                                    tlv_display_name = DISPLAY_NAMES.get(tlv_attr, tlv_attr)
                                                    tlv_attr_label = QLabel(tlv_display_name)
                                                    if isinstance(tlv_value, bool):
                                                        tlv_widget = QCheckBox()
                                                        tlv_widget.setChecked(tlv_value)
                                                        tlv_widget.stateChanged.connect(lambda state, iface_value=iface_value, a=tlv_attr, i=tlv_index: update_lldp_bool(iface_value['org_tlvs'][i], a, state))
                                                    elif isinstance(tlv_value, int):
                                                        tlv_widget = QSpinBox()
                                                        tlv_widget.setRange(0, 9999)
                                                        tlv_widget.setValue(tlv_value)
                                                        tlv_widget.setMinimumWidth(100)
                                                        tlv_widget.valueChanged.connect(lambda val, iface_value=iface_value, a=tlv_attr, i=tlv_index: update_lldp_int(iface_value['org_tlvs'][i], a, val))
                                                    elif isinstance(tlv_value, float):
                                                        tlv_widget = QDoubleSpinBox()
                                                        tlv_widget.setRange(0, 9999)
                                                        tlv_widget.setValue(tlv_value)
                                                        tlv_widget.valueChanged.connect(lambda val, iface_value=iface_value, a=tlv_attr, i=tlv_index: update_lldp_float(iface_value['org_tlvs'][i], a, val))
                                                    elif isinstance(tlv_value, str):
                                                        tlv_widget = QLineEdit()
                                                        tlv_widget.setText(tlv_value)
                                                        tlv_widget.setFixedWidth(140)
                                                        tlv_widget.textChanged.connect(lambda text, iface_value=iface_value, a=tlv_attr, i=tlv_index: update_lldp_str(iface_value['org_tlvs'][i], a, text))
                                                    else:
                                                        tlv_widget = QLabel(str(tlv_value))  # Fallback for other types

                                                    tlv_layout.addWidget(tlv_attr_label, tlv_row, tlv_col)
                                                    tlv_layout.addWidget(tlv_widget, tlv_row, tlv_col + 1)
                                                    tlv_col += 2                                         

                                                tlv_group_box.setLayout(tlv_layout)
                                                lldp_layout.addWidget(tlv_group_box, lldp_row, lldp_col, 1, 4)
                                                lldp_row += 1
                                        else:
                                            lldp_widget = QLabel(str(lldp_value))  # Fallback for other types

                                        if lldp_attr != 'org_tlvs':
                                            lldp_layout.addWidget(lldp_attr_label, lldp_row, lldp_col)
                                        lldp_layout.addWidget(lldp_widget, lldp_row, lldp_col + 1)
                                        lldp_col += 2
                                        if lldp_col >= 4:  # Move to next row after 2 attributes
                                            lldp_col = 0
                                            lldp_row += 1

                                    lldp_group_box.setLayout(lldp_layout)
                                    iface_layout.addWidget(lldp_group_box, iface_row, 0, 1, 4)
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

                                # Slot function to update the iface value
                                def update_iface_value(iface_attr, iface_widget, iface):
                                    # print('Updating=' + iface_attr)
                                    if isinstance(iface_widget, QSpinBox) or isinstance(iface_widget, QDoubleSpinBox):
                                        setattr(iface, iface_attr, iface_widget.value())
                                    elif isinstance(iface_widget, QCheckBox):
                                        setattr(iface, iface_attr, iface_widget.isChecked())
                                    else:
                                        setattr(iface, iface_attr, iface_widget.text())
                                    # print('Setting unsaved = True')
                                    globals.unsaved_changes = True  # Mark as unsaved changes

                                # Update functions for lldp attributes
                                def update_lldp_bool(lldp_dict, attr, state):
                                    lldp_dict[attr] = bool(state)
                                    globals.unsaved_changes = True

                                def update_lldp_int(lldp_dict, attr, value):
                                    lldp_dict[attr] = int(value)
                                    globals.unsaved_changes = True

                                def update_lldp_float(lldp_dict, attr, value):
                                    lldp_dict[attr] = float(value)
                                    globals.unsaved_changes = True

                                def update_lldp_str(lldp_dict, attr, text):
                                    lldp_dict[attr] = text
                                    globals.unsaved_changes = True

                                def update_lldp_list(lldp_dict, attr, text):
                                    lldp_dict[attr] = text.split(", ")
                                    globals.unsaved_changes = True

                                # Connect the appropriate signal to the update_iface_value slot
                                if isinstance(iface_widget, QSpinBox) or isinstance(iface_widget, QDoubleSpinBox):
                                    iface_widget.valueChanged.connect(lambda _, iface_attr=iface_attr, iface_widget=iface_widget, iface=iface: update_iface_value(iface_attr, iface_widget, iface))
                                elif isinstance(iface_widget, QCheckBox):
                                    iface_widget.stateChanged.connect(lambda _, iface_attr=iface_attr, iface_widget=iface_widget, iface=iface: update_iface_value(iface_attr, iface_widget, iface))
                                elif not isinstance(iface_widget, QLabel):
                                    iface_widget.textChanged.connect(lambda _, iface_attr=iface_attr, iface_widget=iface_widget, iface=iface: update_iface_value(iface_attr, iface_widget, iface))

                        iface_group_box.setLayout(iface_layout)
                        grid_layout.addWidget(iface_group_box, row, 1, 1, 3)
                        row += 1
                elif attr == 'dot1x' and isinstance(value, dict):
                    # print('dot1x')
                    row += 1
                    dot1x_label = QLabel("Dot1x")
                    dot1x_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(dot1x_label, row, 0, 1, 2)
                    dot1x_group_box = QGroupBox() 
                    dot1x_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    #dot1x_group_box.setFixedWidth(750)
                    dot1x_layout = QGridLayout()
                    # print(f'value={value}')
                    
                    def update_dot1x_bool(dot1x_dict, attr, state):
                        dot1x_dict[attr] = bool(state)
                        globals.unsaved_changes = True

                    def update_dot1x_int(dot1x_dict, attr, value):
                        dot1x_dict[attr] = int(value)
                        globals.unsaved_changes = True

                    def update_dot1x_float(dot1x_dict, attr, value):
                        dot1x_dict[attr] = float(value)
                        globals.unsaved_changes = True

                    def update_dot1x_str(dot1x_dict, attr, text):
                        dot1x_dict[attr] = text
                        globals.unsaved_changes = True

                    def update_dot1x_list(dot1x_dict, attr, text):
                        dot1x_dict[attr] = text.split(", ")
                        globals.unsaved_changes = True

                    dot1x_row = 0
                    dot1x_col = 0                       
                    for dot1x_attr, dot1x_value in value.items():
                        # Lookup display name for the attribute
                        display_name = DISPLAY_NAMES.get(dot1x_attr, dot1x_attr)  # Fallback to attr if not found
                        dot1x_label = QLabel(display_name)
                        if isinstance(dot1x_value, bool):
                            dot1x_widget = QCheckBox()
                            dot1x_widget.setChecked(dot1x_value)
                            dot1x_widget.stateChanged.connect(lambda state, value=value, a=dot1x_attr: update_dot1x_bool(value, a, state))
                        elif isinstance(dot1x_value, int):
                            dot1x_widget = QSpinBox()
                            dot1x_widget.setRange(0, 9999)
                            dot1x_widget.setValue(dot1x_value)
                            dot1x_widget.valueChanged.connect(lambda val, value=value, a=dot1x_attr: update_dot1x_int(value, a, val))
                        elif isinstance(dot1x_value, float):
                            dot1x_widget = QDoubleSpinBox()
                            dot1x_widget.setValue(dot1x_value)
                            dot1x_widget.valueChanged.connect(lambda val, value=value, a=dot1x_attr: update_dot1x_float(value, a, val))
                        elif isinstance(dot1x_value, str):
                            dot1x_widget = QLineEdit()
                            dot1x_widget.setText(dot1x_value)
                            dot1x_widget.setFixedWidth(200)
                            dot1x_widget.textChanged.connect(lambda text, value=value, a=dot1x_attr: update_dot1x_str(value, a, text))
                        elif isinstance(dot1x_value, list):
                            dot1x_widget = QLineEdit()
                            dot1x_widget.setText(", ".join(map(str, dot1x_value)))  # Convert list to comma-separated string
                            dot1x_widget.setFixedWidth(200)
                            dot1x_widget.textChanged.connect(lambda text, value=value, a=dot1x_attr: update_dot1x_list(value, a, text))
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
                    # print('lldp_beacon')
                    row += 1
                    lldp_label = QLabel("LLDP")
                    lldp_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(lldp_label, row, 0, 1, 2)
                    lldp_group_box = QGroupBox() 
                    lldp_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    #lldp_group_box.setFixedWidth(750)
                    lldp_layout = QGridLayout()
                    # print(f'value={value}')

                    def update_lldp_bool(lldp_dict, attr, state):
                        lldp_dict[attr] = bool(state)
                        globals.unsaved_changes = True

                    def update_lldp_int(lldp_dict, attr, value):
                        lldp_dict[attr] = int(value)
                        globals.unsaved_changes = True

                    def update_lldp_float(lldp_dict, attr, value):
                        lldp_dict[attr] = float(value)
                        globals.unsaved_changes = True

                    def update_lldp_str(lldp_dict, attr, text):
                        lldp_dict[attr] = text
                        globals.unsaved_changes = True

                    def update_lldp_list(lldp_dict, attr, text):
                        lldp_dict[attr] = text.split(", ")
                        globals.unsaved_changes = True

                    lldp_row = 0
                    lldp_col = 0                       
                    for lldp_attr, lldp_value in value.items():
                        # Lookup display name for the attribute
                        display_name = DISPLAY_NAMES.get(lldp_attr, lldp_attr)  # Fallback to attr if not found
                        lldp_label = QLabel(display_name)
                        if isinstance(lldp_value, bool):
                            lldp_widget = QCheckBox()
                            lldp_widget.setChecked(lldp_value)
                            lldp_widget.stateChanged.connect(lambda state, value=value, a=lldp_attr: update_lldp_bool(value, a, state))
                        elif isinstance(lldp_value, int):
                            lldp_widget = QSpinBox()
                            lldp_widget.setRange(0, 9999)
                            lldp_widget.setValue(lldp_value)
                            lldp_widget.valueChanged.connect(lambda val, value=value, a=lldp_attr: update_lldp_int(value, a, val))
                        elif isinstance(lldp_value, float):
                            lldp_widget = QDoubleSpinBox()
                            lldp_widget.setRange(0, 9999)
                            lldp_widget.setValue(lldp_value)
                            lldp_widget.valueChanged.connect(lambda val, value=value, a=lldp_attr: update_lldp_float(value, a, val))
                        elif isinstance(lldp_value, str):
                            lldp_widget = QLineEdit()
                            lldp_widget.setText(lldp_value)
                            lldp_widget.setFixedWidth(200)
                            lldp_widget.textChanged.connect(lambda text, value=value, a=lldp_attr: update_lldp_str(value, a, text))
                        elif isinstance(lldp_value, list):
                            # print('List for=' + lldp_attr)
                            lldp_widget = QLineEdit()
                            lldp_widget.setText(", ".join(map(str, lldp_value)))  # Convert list to comma-separated string
                            lldp_widget.setFixedWidth(200)
                            lldp_widget.textChanged.connect(lambda text, value=value, a=lldp_attr: update_lldp_list(value, a, text))
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
                    # print('Stack')
                    row += 1
                    stack_label = QLabel("Stack")
                    stack_label.setStyleSheet("font-weight: bold;")
                    grid_layout.addWidget(stack_label, row, 0, 1, 2)
                    stack_group_box = QGroupBox() 
                    stack_group_box.setStyleSheet("QGroupBox { font-size: 10pt; font-weight: bold; }")
                    stack_layout = QGridLayout()
                    #print(f'value={value}')

                    def update_stack_bool(stack_dict, attr, state):
                        stack_dict[attr] = bool(state)
                        globals.unsaved_changes = True

                    def update_stack_int(stack_dict, attr, value):
                        stack_dict[attr] = int(value)
                        globals.unsaved_changes = True

                    def update_stack_float(stack_dict, attr, value):
                        stack_dict[attr] = float(value)
                        globals.unsaved_changes = True

                    def update_stack_str(stack_dict, attr, text):
                        stack_dict[attr] = text
                        globals.unsaved_changes = True

                    def update_stack_list(stack_dict, attr, text):
                        stack_dict[attr] = text.split(", ")
                        globals.unsaved_changes = True

                    stack_row = 0
                    stack_col = 0                       
                    for stack_attr, stack_value in value.items():
                        # Lookup display name for the attribute
                        display_name = DISPLAY_NAMES.get(stack_attr, stack_attr)  # Fallback to attr if not found
                        stack_label = QLabel(display_name)
                        if isinstance(stack_value, bool):
                            stack_widget = QCheckBox()
                            stack_widget.setChecked(stack_value)
                            stack_widget.stateChanged.connect(lambda state, value=value, a=stack_attr: update_stack_bool(value, a, state))
                        elif isinstance(stack_value, int):
                            stack_widget = QSpinBox()
                            stack_widget.setRange(0, 9999)
                            stack_widget.setValue(stack_value)
                            stack_widget.valueChanged.connect(lambda val, value=value, a=stack_attr: update_stack_int(value, a, val))
                        elif isinstance(stack_value, float):
                            stack_widget = QDoubleSpinBox()
                            stack_widget.setRange(0, 9999)
                            stack_widget.setValue(stack_value)
                            stack_widget.valueChanged.connect(lambda val, value=value, a=stack_attr: update_stack_float(value, a, val))
                        elif isinstance(stack_value, str):
                            stack_widget = QLineEdit()
                            stack_widget.setText(stack_value)
                            stack_widget.setFixedWidth(200)
                            stack_widget.textChanged.connect(lambda text, value=value, a=stack_attr: update_stack_str(value, a, text))
                        elif isinstance(stack_value, list):
                            # print('List for=' + stack_attr)
                            stack_widget = QLineEdit()
                            stack_widget.setText(", ".join(map(str, stack_value)))  # Convert list to comma-separated string
                            stack_widget.setFixedWidth(200)
                            stack_widget.textChanged.connect(lambda text, value=value, a=stack_attr: update_stack_list(value, a, text))
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
                    # Lookup display name for the attribute
                    display_name = DISPLAY_NAMES.get(attr, attr)  # Fallback to attr if not found
                    label = QLabel(display_name)
                    label.setFixedWidth(150)
                    if isinstance(value, bool):
                        widget = QCheckBox()
                        widget.setChecked(value)
                        widget.stateChanged.connect(lambda state, dp=dp, a=attr: update_dp_bool(dp, a, state))
                    elif isinstance(value, int):
                        widget = QSpinBox()
                        widget.setValue(value)
                        widget.valueChanged.connect(lambda val, dp=dp, a=attr: update_dp_int(dp, a, val))
                    elif isinstance(value, float):
                        widget = QDoubleSpinBox()
                        widget.setValue(value)
                        widget.setMaximumWidth(200)
                        widget.valueChanged.connect(lambda val, dp=dp, a=attr: update_dp_float(dp, a, val))
                    elif isinstance(value, str):
                        widget = QLineEdit()
                        widget.setText(value)
                        widget.setFixedWidth(200)
                        widget.textChanged.connect(lambda text, dp=dp, a=attr: update_dp_str(dp, a, text))
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