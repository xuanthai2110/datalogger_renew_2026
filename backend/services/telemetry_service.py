import logging
import json
from datetime import datetime
from typing import Any, List
from backend.db_manager import CacheDB

logger = logging.getLogger(__name__)

class TelemetryService:
    """Xây dựng telemetry payload từ CacheDB (RAM) để gửi lên server."""
    def __init__(self, realtime_db):
        self.realtime_db = realtime_db

    def build_payload_from_cache(self, project_id: int, server_id: int, inverters_meta: list, cache_db: CacheDB) -> list:
        now = datetime.now()
        ts_str = now.isoformat()
        
        # 1. Project Summary from RealtimeDB (Latest snapshot)
        proj_latest = self.realtime_db.get_latest_project_realtime(project_id)
        project_json = {
            "Temp_C": proj_latest.Temp_C if proj_latest else 0.0,
            "P_ac": proj_latest.P_ac if proj_latest else 0.0,
            "P_dc": proj_latest.P_dc if proj_latest else 0.0,
            "E_daily": proj_latest.E_daily if proj_latest else 0.0,
            "E_monthly": proj_latest.E_monthly if proj_latest else 0.0,
            "E_total": proj_latest.E_total if proj_latest else 0.0,
            "severity": proj_latest.severity if proj_latest else "UNKNOWN",
            "created_at": ts_str
        }

        # 2. Inverters Data
        inverters_json = []
        for inv in inverters_meta:
            inv_id = inv.id
            
            # AC Data (from Cache)
            ac = cache_db.get_latest_realtime(inv_id) # ac_cache
            if not ac: continue
            
            # MPPT & Strings (from Cache)
            mppts_cache = cache_db.get_mppt_cache_by_inverter(inv_id)
            strings_cache = cache_db.get_string_cache_by_inverter(inv_id)
            
            # Map strings to MPPTs
            mppt_list = []
            for m in mppts_cache:
                m_idx = m["mppt_index"]
                m_strings = [
                    {
                        "string_index": s["string_id"],
                        "I_mppt": s["I_string"],
                        "Max_I": s["max_I"],
                        "created_at": self._format_ts(s.get("updated_at"))
                    }
                    for s in strings_cache if s["mppt_id"] == m["id"] # Check mapping logic
                ]
                # If mapping by mppt_id fails (ID vs Index), fallback or adjust
                # In CacheDB, mppt_id is the auto-inc ID of the MPPT row.
                
                mppt_list.append({
                    "mppt_index": m_idx,
                    "string_on_mppt": m["string_on_mppt"],
                    "V_mppt": m["V_mppt"],
                    "I_mppt": m["I_mppt"],
                    "P_mppt": m["P_mppt"],
                    "Max_I": m["Max_I"],
                    "Max_V": m["Max_V"],
                    "Max_P": m["Max_P"],
                    "created_at": self._format_ts(m.get("updated_at")),
                    "strings": m_strings
                })

            # Error Payload
            err_row = cache_db.get_error_cache(inv_id)
            errors = []
            if err_row:
                # Use fault_json if exists, else build from status/fault codes
                if err_row.get("fault_json"):
                    errors = json.loads(err_row["fault_json"])
                else:
                    # Minimal error object to match structure
                    errors = [{
                        "fault_code": err_row.get("fault_code", 0),
                        "fault_description": "STATUS: " + str(err_row.get("status_code", 0)),
                        "repair_instruction": "",
                        "severity": "STABLE",
                        "created_at": ts_str
                    }]
            
            inv_data = {
                "serial_number": inv.serial_number,
                "ac": {
                    "IR": ac.get("IR", 0.0),
                    "Temp_C": ac.get("Temp_C", 0.0),
                    "P_ac": ac.get("P_ac", 0.0),
                    "Q_ac": ac.get("Q_ac", 0.0),
                    "V_a": ac.get("V_a", 0.0),
                    "V_b": ac.get("V_b", 0.0),
                    "V_c": ac.get("V_c", 0.0),
                    "I_a": ac.get("I_a", 0.0),
                    "I_b": ac.get("I_b", 0.0),
                    "I_c": ac.get("I_c", 0.0),
                    "PF": ac.get("PF", 0.0),
                    "H": ac.get("H", 0.0),
                    "E_daily": ac.get("E_daily", 0.0),
                    "E_monthly": ac.get("E_monthly", 0.0),
                    "E_total": ac.get("E_total", 0.0),
                    "created_at": self._format_ts(ac.get("updated_at"))
                },
                "mppts": mppt_list,
                "errors": errors
            }
            inverters_json.append(inv_data)
            
        if not inverters_json: return []
            
        payload = {
            "project": project_json,
            "inverters": inverters_json
        }
        return [self._normalize_payload(payload)]

    def _normalize_payload(self, data: Any) -> Any:
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, float): data[k] = round(v, 2)
                elif isinstance(v, (dict, list)): self._normalize_payload(v)
        elif isinstance(data, list):
            for item in data: self._normalize_payload(item)
        return data

    @staticmethod
    def _format_ts(ts: str) -> str:
        if not ts: return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") + "+07:00"
        if "T" not in ts: ts = ts.replace(" ", "T")
        if "+" not in ts and not ts.endswith("Z"): ts += "+07:00"
        return ts
