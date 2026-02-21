from pymodbus.client import ModbusSerialClient

class ModbusRTU:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.client = ModbusSerialClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            timeout=2
        )

    def read_holding(self, address, count, unit=1):
        self.client.connect()
        result = self.client.read_holding_registers(address, count, unit=unit)
        self.client.close()
        return result.registers if result else None