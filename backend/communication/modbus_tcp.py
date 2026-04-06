"""
communication/modbus_tcp.py
Modbus TCP Transport Layer
Compatible with pymodbus 2.x and 3.x
"""

import logging

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

from backend.communication.modbus_arbiter import ModbusBusArbiter


logger = logging.getLogger(__name__)


class ModbusTCP:
    def __init__(
        self,
        host: str,
        port: int = 502,
        timeout: float = 3.0,
        retries: int = 1,
    ):
        self.host = host
        self.port = port
        self.retries = retries
        self.arbiter = ModbusBusArbiter(f"tcp://{host}:{port}")

        self.client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout,
        )

    def connect(self) -> bool:
        try:
            if not self.client.connect():
                logger.error(f"[TCP] Cannot connect to {self.host}:{self.port}")
                return False
            logger.info(f"[TCP] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"[TCP] Connect error {self.host}:{self.port} -> {e}")
            return False

    def close(self):
        try:
            self.client.close()
            logger.info(f"[TCP] Connection closed {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"[TCP] Close error: {e}")

    def _retry(self, func, *args, **kwargs):
        last_error = None

        self.arbiter.acquire()
        try:
            for attempt in range(1, self.retries + 1):
                try:
                    if not self.client.connected:
                        self.client.connect()

                    response = func(*args, **kwargs)

                    if isinstance(response, ModbusIOException):
                        last_error = response
                        logger.warning(
                            f"[TCP] Attempt {attempt}/{self.retries} failed: {response}"
                        )
                        continue

                    return response

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"[TCP] Attempt {attempt}/{self.retries} exception: {e}"
                    )
        finally:
            self.arbiter.release()

        raise ConnectionError(
            f"[TCP] Communication failed after {self.retries} retries: {last_error}"
        )

    def read_input_registers(self, address: int, count: int, slave: int = 1):
        try:
            return self._retry(
                self.client.read_input_registers,
                address,
                count,
                slave=slave,
            )
        except TypeError:
            return self._retry(
                self.client.read_input_registers,
                address,
                count,
                unit=slave,
            )

    def read_holding_registers(self, address: int, count: int, slave: int = 1):
        try:
            return self._retry(
                self.client.read_holding_registers,
                address,
                count,
                slave=slave,
            )
        except TypeError:
            return self._retry(
                self.client.read_holding_registers,
                address,
                count,
                unit=slave,
            )

    def write_single_register(self, address: int, value: int, slave: int = 1):
        value = int(value) & 0xFFFF

        try:
            return self._retry(
                self.client.write_register,
                address,
                value,
                slave=slave,
            )
        except TypeError:
            return self._retry(
                self.client.write_register,
                address,
                value,
                unit=slave,
            )

    def write_multiple_registers(self, address: int, values, slave: int = 1):
        try:
            return self._retry(
                self.client.write_registers,
                address,
                values,
                slave=slave,
            )
        except TypeError:
            return self._retry(
                self.client.write_registers,
                address,
                values,
                unit=slave,
            )

    def write_register(self, address: int, value: int, slave: int = 1):
        return self.write_single_register(address, value, slave=slave)
