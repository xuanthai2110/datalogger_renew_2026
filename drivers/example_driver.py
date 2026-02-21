import random
from drivers.base import BaseDriver

class ExampleDriver(BaseDriver):
    def read_data(self):
        return {
            "inverter_id": "INV001",
            "pv_power": random.uniform(1000, 5000),
            "grid_power": random.uniform(500, 2000),
            "daily_energy": random.uniform(10, 50),
            "total_energy": random.uniform(1000, 5000),
            "temperature": random.uniform(25, 45)
        }