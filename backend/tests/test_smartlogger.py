import os
import sys
import time
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from backend.communication.modbus_tcp import ModbusTCP
from backend.core import config
from backend.drivers.smartloggerHuawei import SmartLoggerHuawei


def test_smartlogger():
    transport = ModbusTCP(
        host=config.MODBUS_TCP_HOST,
        port=config.MODBUS_TCP_PORT,
        timeout=config.TIMEOUT,
        retries=max(1, config.RETRIES),
    )

    if not transport.connect():
        raise ConnectionError(
            f"Cannot connect to SmartLogger at {config.MODBUS_TCP_HOST}:{config.MODBUS_TCP_PORT}"
        )

    try:
        smartlogger = SmartLoggerHuawei(transport, slave_id=0)
        print("\n=== SMARTLOGGER CONTROL ===")
        smartlogger.control_P(880)
        print("Đã điều khiển công suất")
        time.sleep(5)

        print("=== SMARTLOGGER STATUS ===")
        status = smartlogger.control_status()
        print(status)
        time.sleep(10)

        print("\n=== SMARTLOGGER ACTUAL POWER ===")
        actual_power = smartlogger.read_actual_power()
        print(actual_power)
    finally:
        transport.close()


if __name__ == "__main__":
    test_smartlogger()
