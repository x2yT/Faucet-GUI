class Bgp:
    def __init__(self, vlan='', as_number=0, port=0, routerid='', server_addresses=None, neighbor_addresses=None, neighbor_as=0):
        self.vlan = vlan
        self.as_number = as_number
        self.port = port
        self.routerid = routerid
        self.server_addresses = server_addresses if server_addresses is not None else []
        self.neighbor_addresses = neighbor_addresses if neighbor_addresses is not None else []
        self.neighbor_as = neighbor_as

class Router:
    def __init__(self, vlans=None, bgp=None):
        self.vlans = vlans if vlans is not None else []
        self.bgp = bgp  # bgp 是一个 Bgp 类的实例

    def print_details(self):
        print("Router Details:")
        print(f"  VLANs: {self.vlans}")
        if self.bgp:
            print("  BGP Details:")
            print(f"    VLAN: {self.bgp.vlan}")
            print(f"    AS Number: {self.bgp.as_number}")
            print(f"    Port: {self.bgp.port}")
            print(f"    Router ID: {self.bgp.routerid}")
            print(f"    Server Addresses: {', '.join(self.bgp.server_addresses)}")
            print(f"    Neighbor Addresses: {', '.join(self.bgp.neighbor_addresses)}")
            print(f"    Neighbor AS: {self.bgp.neighbor_as}")
        else:
            print("  BGP Details: None")