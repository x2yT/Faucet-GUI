# models/meter.py

class Meter:
    def __init__(self, meter_id, bands=None, unit="kbps"):
        self.meter_id = meter_id
        self.bands = bands or []
        self.unit = unit

    @classmethod
    def from_dict(cls, data):
        meter_id = data.get('meter_id', None)
        bands = data.get('bands', [])
        unit = data.get('unit', "kbps")
        return cls(meter_id=meter_id, bands=bands, unit=unit)

    def to_dict(self):
        return {
            'meter_id': self.meter_id,
            'bands': self.bands,
            'unit': self.unit
        }

class Band:
    def __init__(self, rate, burst_size=None, action=None):
        self.rate = rate
        self.burst_size = burst_size
        self.action = action

    def to_dict(self):
        return {
            'rate': self.rate,
            'burst_size': self.burst_size,
            'action': self.action
        }
