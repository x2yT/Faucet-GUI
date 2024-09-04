from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout

def create_acls_tab(config):
    # Create the main widget for the tab
    tab = QWidget()
    
    # Create a vertical layout to hold all the form layouts
    main_layout = QVBoxLayout()
    
    # Iterate over the ACLs in the config
    for acl_name, acl in config.acls.items():
        # Create a form layout for each ACL
        form_layout = QFormLayout()
        
        # Add a label for the ACL name
        form_layout.addRow(QLabel(f"ACL: {acl_name}"))
        
        # Iterate over the rules in the ACL
        for rule in acl.rules:
            # Add a label for the rule
            form_layout.addRow(QLabel("Rule"))
            
            # Access the attributes of the Rule object directly
            for key in vars(rule):
                print('rule key=' + key)
                value = getattr(rule, key)
                if value != None:
                    print('value=' + str(value))
                    if isinstance(value, dict):
                        # Handle nested dictionaries (like actions)
                        print("subkey")
                        for sub_key, sub_value in value.items():
                            line_edit = QLineEdit(str(sub_value))
                            form_layout.addRow(QLabel(f"{key} - {sub_key}"), line_edit)
                    else:
                        # Display each match as a label and editable field
                        print('Not isinstance1')
                        line_edit = QLineEdit(str(value))
                        form_layout.addRow(QLabel(key), line_edit)
        
        # Add the form layout to the main layout
        main_layout.addLayout(form_layout)
    
    # Set the main layout for the tab
    tab.setLayout(main_layout)
    
    return tab