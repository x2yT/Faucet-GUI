# saver.py

# Import the yaml module for handling YAML files
import yaml

# Define a function to save the configuration to a YAML file
def save_config(config, yaml_file):
    # Create a dictionary with the configuration data
    data = {
        'vlans': config.vlans,  # Access the vlans attribute of the config object
        'routers': config.routers,  # Access the routers attribute of the config object
        'dps': config.dps  # Access the dps attribute of the config object
    }
    # Open the specified YAML file in write mode
    with open(yaml_file, 'w') as file:
        # Dump the configuration data to the YAML file
        yaml.safe_dump(data, file)