# drivers/huawei_smartlogger.py

from typing import Dict, Any
from backend.drivers.base import BaseDriver


class SmartLoggerHuawei(BaseDriver):

    def __init__(self, transport, slave_id=0):
        self.transport = transport
        self.slave_id = slave_id

    # =========================================================
    # ================= LOW LEVEL =============================
    # =========================================================

    def _read_u16(self, addr):
        res = self.transport.read_holding_registers(
            address=addr,
            count=1,
            slave=self.slave_id
        )
        if res.isError():
            raise Exception(f"Read error at {addr}")
        return res.registers[0]

    def _read_u32(self, addr):
        res = self.transport.read_holding_registers(
            address=addr,
            count=2,
            slave=self.slave_id
        )
        if res.isError():
            raise Exception(f"Read error at {addr}")
        return (res.registers[0] << 16) + res.registers[1]

    def _write_u16(self, addr, value):
        res = self.transport.write_register(
            address=addr,
            value=value,
            slave=self.slave_id
        )
        if res.isError():
            raise Exception(f"Write error at {addr}")
        return True

    def _write_u32(self, addr, value):
        high = (value >> 16) & 0xFFFF
        low = value & 0xFFFF

        res = self.transport.write_multiple_registers(
            address=addr,
            values=[high, low],
            slave=self.slave_id
        )
        if res.isError():
            raise Exception(f"Write error at {addr}")
        return True

    # =========================================================
    # ================= CONTROL STATUS ========================
    # =========================================================

    def control_status(self) -> Dict[str, Any]:
        """
        Detect trạng thái điều khiển công suất
        """

        try:
            plant_status = self._read_u16(40543)
            control_mode = self._read_u16(40737)
            setpoint_kw = self._read_u32(40738) / 10
            percent = self._read_u32(40802)

            is_limited = (
                plant_status == 2 or
                control_mode != 0 or
                percent < 100
            )

            return {
                "plant_status": plant_status,
                "control_mode": control_mode,
                "setpoint_kw": setpoint_kw,
                "percent": percent,
                "is_limited": is_limited
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================
    # ================= CONTROL P =============================
    # =========================================================

    def control_P(self, kw: float) -> bool:
        """
        Điều khiển công suất tổng (kW)
        -> register 40420
        gain = 10
        """

        value = int(kw * 10)

        return self._write_u32(40420, value)

    # =========================================================
    # ================= CONTROL % =============================
    # =========================================================

    def control_percent(self, percent: float) -> bool:
        """
        Điều khiển theo %
        -> register 40428
        gain = 10
        """

        value = int(percent * 10)

        return self._write_u16(40428, value)

    # =========================================================
    # ================= READ ACTUAL ===========================
    # =========================================================

    def read_actual_power(self) -> float:
        """
        Công suất thực tế toàn plant (kW)
        -> 40525
        """

        value = self._read_u32(40525)

        # signed
        if value > 0x7FFFFFFF:
            value -= 0x100000000

        return value / 1000