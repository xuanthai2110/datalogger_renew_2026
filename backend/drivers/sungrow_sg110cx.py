from typing import Dict, Any
from backend.drivers.base import BaseDriver
import time


class SungrowSG110CXDriver(BaseDriver):

    def __init__(self, transport, slave_id=1):
        self.transport = transport
        self.slave_id = slave_id

    # =========================================================
    # ================= REGISTER MAP ==========================
    # =========================================================

    def register_map(self) -> Dict[str, Any]:
        return {

            "info": [
                {"name": "serial_number", "address": 4989, "length": 10, "type": "string", "scale": None},
                {"name": "rated_power", "address": 5000, "length": 1, "type": "uint16", "scale": 0.1},
            ],

            "ac": [
                {"name": "v_a", "address": 5018, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "v_b", "address": 5019, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "v_c", "address": 5020, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "i_a", "address": 5021, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "i_b", "address": 5022, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "i_c", "address": 5023, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "p_inv_w", "address": 5030, "length": 2, "type": "uint32", "scale": 1},
                {"name": "q_inv_var", "address": 5032, "length": 2, "type": "sint32", "scale": 1},

                {"name": "pf", "address": 5034, "length": 1, "type": "sint16", "scale": 0.001},
                {"name": "grid_hz", "address": 5035, "length": 1, "type": "uint16", "scale": 0.1},
            ],

            "dc": [
                {"name": "p_dc_w", "address": 5016, "length": 2, "type": "uint32", "scale": 1},
                {"name": "mppt_1_voltage", "address": 5010, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_1_current", "address": 5011, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_2_voltage", "address": 5012, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_2_current", "address": 5013, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_3_voltage", "address": 5014, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_3_current", "address": 5015, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_4_voltage", "address": 5114, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_4_current", "address": 5115, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_5_voltage", "address": 5116, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_5_current", "address": 5117, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_6_voltage", "address": 5118, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_6_current", "address": 5119, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_7_voltage", "address": 5120, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_7_current", "address": 5121, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_8_voltage", "address": 5122, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_8_current", "address": 5123, "length": 1, "type": "uint16", "scale": 0.1},

                {"name": "mppt_9_voltage", "address": 5129, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "mppt_9_current", "address": 5130, "length": 1, "type": "uint16", "scale": 0.1},
            ],

            "string": [
                {
                    "name": f"string_{i}_current",
                    "address": 7012 + i,   # 7013–7030
                    "length": 1,
                    "type": "uint16",
                    "scale": 0.01,
                }
                for i in range(1, 19)
            ],

            "stat": [
                {"name": "temp_c", "address": 5007, "length": 1, "type": "sint16", "scale": 0.1},
                {"name": "e_daily", "address": 5002, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "e_total", "address": 5003, "length": 2, "type": "uint32", "scale": 1},
                {"name": "work_state", "address": 5037, "length": 2, "type": "uint16", "scale": 1},
                {"name": "fault_code", "address": 5045, "length": 2, "type": "uint16", "scale": 1}
            ],

            "control": [
                {"name": "enable", "address": 5006, "length": 1, "type": "uint16", "scale": None},
                {"name": "p_set_percent", "address": 5007, "length": 1, "type": "uint16", "scale": 0.1},
                {"name": "q_set_var", "address": 5039, "length": 1, "type": "sint16", "scale": 0.1},
                {"name": "p_set_kw", "address": 5038, "length": 1, "type": "uint16", "scale": 0.1},
            ]

        }


    # =========================================================
    # ================= INTERNAL ==============================
    # =========================================================

    def _read_block(self, start, length):
        res = self.transport.read_input_registers(
            address=start,
            count=length,
            slave=self.slave_id
        )
        if res.isError():
            raise Exception("Modbus read error")
        return res.registers

    def _get_reg(self, name):
        for group in self.register_map().values():
            for r in group:
                if r["name"] == name:
                    return r
        raise Exception(f"Register {name} not found")

    # =========================================================
    # ================= CONVERT ===============================
    # =========================================================

    def _convert(self, regs, typ):

        if not regs:
            return None

        if typ == "uint16":
            v = regs[0]
            return None if v == 0xFFFF else v

        if typ == "sint16":
            v = regs[0]
            if v == 0x7FFF:
                return None
            if v & 0x8000:
                v -= 0x10000
            return v

        if typ == "uint32":
            low, high = regs[0], regs[1]
            v = (high << 16) | low
            return None if v == 0xFFFFFFFF else v

        if typ == "sint32":
            low, high = regs[0], regs[1]
            v = (high << 16) | low
            if v == 0x7FFFFFFF:
                return None
            if v & 0x80000000:
                v -= 0x100000000
            return v

        if typ == "string":
            raw = bytearray()
            for r in regs:
                raw.append((r >> 8) & 0xFF)
                raw.append(r & 0xFF)
            return raw.decode("utf-8", errors="ignore").strip("\x00").strip()

        return None

    def parse(self, raw, reg_list):
        res = {}
        offset = 0

        for r in reg_list:
            val = self._convert(raw[offset:offset+r["length"]], r["type"])

            if val is not None and r["scale"] is not None:
                val *= r["scale"]

            res[r["name"]] = val
            offset += r["length"]

        return res

    def _read_group(self, regs):
        start = min(r["address"] for r in regs)
        end = max(r["address"] + r["length"] - 1 for r in regs)

        raw = self._read_block(start, end - start + 1)

        ordered = []
        for r in regs:
            idx = r["address"] - start
            ordered.extend(raw[idx: idx + r["length"]])

        return self.parse(ordered, regs)

    # =========================================================
    # ================= READ ==============================
    # =========================================================

    def read_info(self):
        from datetime import datetime
        parsed = self._read_group(self.register_map()["info"])
        rated = parsed.get("rated_power", 110.0)

        return {
            "brand": "Sungrow",
            "model": "SG110CX",
            "serial_number": parsed.get("serial_number", ""),
            "capacity_kw": rated,
            "mppt_count": 9,
            "string_count": 18,
            "is_active": True,
            "slave_id": self.slave_id,
            "usage_start_at": datetime.now().isoformat()
        }

    def read_ac(self):
        return self._read_group(self.register_map()["ac"])

    def read_dc(self):
        return self._read_group(self.register_map()["dc"])

    def read_string(self):
        return self._read_group(self.register_map()["string"])

    def read_stat(self):
        return self._read_group(self.register_map()["stat"])

    def read_states_and_faults(self):
        self.read_stat()
        return {
            "state_id": state_id,
            "fault_code": fault_code
        }

    def read_all(self):
        data = {}
        data.update(self.read_info())
        data.update(self.read_ac())
        data.update(self.read_dc())
        data.update(self.read_string())

        try:
            data.update(self.read_stat())
        except:
            pass

        try:
            data.update(self.read_states_and_faults())
        except:
            pass

        return data

    # =========================================================
    # ================= WRITE ===============================
    # =========================================================

    def write_by_name(self, name, value):

        reg = self._get_reg(name)

        raw = int(value / (reg["scale"] or 1))

        res = self.transport.write_register(
            address=reg["address"],
            value=raw,
            slave=self.slave_id
        )

        if res.isError():
            raise Exception(f"Write failed: {name}")

        return True

    def set_power_kw(self, kw):
        self.write_by_name("enable", 0xAA)
        return self.write_by_name("p_set_kw", kw)

    def set_power_percent(self, percent):
        self.write_by_name("enable", 0xAA)
        return self.write_by_name("p_set_percent", percent)
    def read_power(self):
        """
        Đọc công suất tác dụng tổng từ inverter Sungrow qua mapping 'p_inv_w'.
        """
        reg = self._get_reg("p_inv_w")
        raw = self._read_block(reg["address"], reg["length"])
        value = self._convert(raw, reg["type"])
        if value is not None and reg["scale"] is not None:
            value *= reg["scale"]
        return value