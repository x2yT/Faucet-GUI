import yaml

def save_config(config, yaml_file):
    data = {
        #'include': config.include,
        'vlans': {k: v.__dict__ for k, v in config.vlans.items()},
        'routers': {k: v.__dict__ for k, v in config.routers.items()},
        'dps': {k: v.__dict__ for k, v in config.dps.items()}
    }
    with open(yaml_file, 'w') as file:
        yaml.safe_dump(data, file)