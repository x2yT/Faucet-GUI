class Meter:
    def __init__(self, meter_id, name, flags=None, bands=None):
        self.meter_id = meter_id
        self.name = name
        # Remove the rate and burst size attributes
        # self.rate = rate
        # self.burst_size = burst_size

        self.flags = flags if flags else []
        self.bands = bands if bands else []

    def to_dict(self):
        """Converts the meter object to a dictionary suitable for saving to YAML."""
        return {
            'meter_id': self.meter_id,
            #'rate': self.rate,
            #'burst_size': self.burst_size,
            'flags': self.flags,
            'bands': self.bands,
        }

    @staticmethod
    def from_dict(name, data):
        """Creates a Meter object from a dictionary loaded from YAML."""
        meter_id = data.get('meter_id', 0)  # Default to 0 if not provided
        #rate = data.get('rate', 0)  # Ensure rate is retrieved with a default
        #burst_size = data.get('burst_size', 0)  # Default to 0 if not provided
        flags = data.get('flags', [])  # Access flags correctly
        bands = data.get('bands', [])  # Access bands correctly

        return Meter(meter_id, name, flags, bands)

