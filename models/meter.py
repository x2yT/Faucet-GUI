class Meter:
    def __init__(self, meter_id, name, rate, burst_size, flags=None, bands=None):
        self.meter_id = meter_id
        self.name = name
        self.rate = rate
        self.burst_size = burst_size
        self.flags = flags if flags else []
        self.bands = bands if bands else []

    def to_dict(self):
        """Converts the meter object to a dictionary suitable for saving to YAML."""
        return {
            'meter_id': self.meter_id,
            'entry': {
                'flags': self.flags,
                'bands': self.bands
            },
            'rate': self.rate,
            'burst_size': self.burst_size
        }

    @staticmethod
    def from_dict(name, data):
        """Creates a Meter object from a dictionary loaded from YAML."""
        meter_id = data.get('meter_id', 0)
        rate = data['rate']
        burst_size = data.get('burst_size', 0)
        flags = data['entry'].get('flags', [])
        bands = data['entry'].get('bands', [])

        return Meter(meter_id, name, rate, burst_size, flags, bands)
