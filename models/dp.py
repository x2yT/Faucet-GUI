<<<<<<< HEAD
class Interface:
    def __init__(self, name, description, native_vlan, tagged_vlans, acls_in):
        self.name = name
        self.description = description
        self.native_vlan = native_vlan
        self.tagged_vlans = tagged_vlans
        self.acls_in = acls_in

class DP:
    def __init__(self, dp_id, hardware, interfaces):
        self.dp_id = dp_id
        self.hardware = hardware
=======
class Interface:
    def __init__(self, name, description, native_vlan, tagged_vlans, acls_in):
        self.name = name
        self.description = description
        self.native_vlan = native_vlan
        self.tagged_vlans = tagged_vlans
        self.acls_in = acls_in

class DP:
    def __init__(self, dp_id, hardware, interfaces):
        self.dp_id = dp_id
        self.hardware = hardware
>>>>>>> 3508a699cb3b3084ed8ee2b733643c54a21b8047
        self.interfaces = interfaces