from pymodbus.client import ModbusTcpClient

class ModbusTCP:
    def __init__(self, host, port=502):
        self.client = ModbusTcpClient(host, port=port)

    def read_holding(self, address, count, unit=1):
        self.client.connect()
        result = self.client.read_holding_registers(address, count, unit=unit)
        self.client.close()
        return result.registers if result else None