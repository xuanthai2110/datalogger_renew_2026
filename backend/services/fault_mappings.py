# backend/services/fault_mappings.py

UNIFIED_STATES = {
    1: "RUNNING", 2: "STANDBY", 3: "STARTING", 4: "STOPPED", 5: "FAULT",
    6: "ALARM_RUNNING", 7: "DERATING", 8: "DISPATCH_RUNNING", 9: "COMMUNICATION_FAULT",
    10: "EMERGENCY_STOP", 11: "KEY_STOP", 12: "INITIAL_STANDBY", 13: "GRID_DETECTING",
    14: "INSULATION_CHECK", 15: "SELF_CHECK", 16: "OFF_GRID_RUNNING", 17: "MAINTENANCE_MODE",
    18: "UPGRADING", 19: "SHUTTING_DOWN", 20: "POWER_LIMITED", 21: "GRID_FAULT_WAIT", 22: "SLEEP"
}

UNIFIED_FAULTS = {
    # GRID
    1001: "GRID_OVERVOLTAGE", 1002: "GRID_TRANSIENT_OVERVOLTAGE", 1003: "GRID_UNDERVOLTAGE",
    1004: "GRID_OVERCURRENT", 1005: "GRID_OVER_FREQUENCY", 1006: "GRID_UNDER_FREQUENCY",
    1007: "GRID_POWER_OUTAGE", 1008: "GRID_VOLTAGE_UNBALANCE", 1009: "GRID_PHASE_LOSS",
    1010: "GRID_ABNORMAL", 1011: "GRID_10MIN_OVERVOLTAGE", 1012: "GRID_IMPEDANCE_ABNORMAL",
    1013: "GRID_REVERSE_POWER", 1014: "GRID_CONNECTION_LOST", 1015: "GRID_PROTECTION_TRIGGERED",
    1016: "GRID_PHASE_CONFRONTATION", 
    
    # PV
    1101: "PV_REVERSE_CONNECTION", 1102: "PV_OVERVOLTAGE", 1103: "PV_CONFIGURATION_ERROR",
    1104: "PV_INPUT_ABNORMAL", 1105: "PV_STRING_FAULT", 1106: "PV_STRING_LOSS",
    1107: "PV_STRING_IMBALANCE", 1108: "PV_LOW_VOLTAGE", 1109: "PV_DC_BUS_OVERVOLTAGE",
    1110: "PV_DC_BUS_UNDERVOLTAGE",
    1111: "PV_STRING_REVERSE_ALARM", 

    # ELECTRICAL
    1201: "LEAKAGE_CURRENT", 1202: "LOW_INSULATION_RESISTANCE", 1203: "AC_OVERLOAD",
    1204: "AC_SHORT_CIRCUIT", 1205: "DC_OVER_CURRENT", 1206: "GROUND_FAULT",
    1207: "RESIDUAL_CURRENT_FAULT", 1208: "DC_COMPONENT_HIGH", 1209: "DC_INJECTION_HIGH",
    
    # TEMPERATURE
    1301: "DEVICE_OVER_TEMPERATURE", 1302: "AMBIENT_OVER_TEMPERATURE", 1303: "AMBIENT_LOW_TEMPERATURE",
    1304: "HEATSINK_OVER_TEMPERATURE", 1305: "MODULE_OVER_TEMPERATURE",
    
    # HARDWARE
    1401: "FAN_FAULT", 1402: "AC_SPD_FAULT", 1403: "DC_SPD_FAULT", 1404: "RELAY_FAULT",
    1405: "CONTACTOR_FAULT", 1406: "SENSOR_FAULT", 1407: "EEPROM_FAULT",
    1408: "INTERNAL_COMMUNICATION_FAULT", 1409: "CONTROL_BOARD_FAULT", 1410: "POWER_MODULE_FAULT",
    1411: "DC_BUS_CAPACITOR_FAULT", 
    
    # COMMUNICATION
    1501: "COMMUNICATION_FAULT", 1502: "METER_COMMUNICATION_FAULT", 1503: "RS485_COMMUNICATION_FAULT",
    1504: "MODBUS_COMMUNICATION_FAULT", 1505: "ETHERNET_COMMUNICATION_FAULT", 1506: "CLOUD_COMMUNICATION_FAULT",
    1507: "METER_CT_REVERSE_CONNECTION", 

    # SAFETY
    1601: "ARC_FAULT", 1602: "ARC_DETECTION_DISABLED", 1603: "RAPID_SHUTDOWN_TRIGGERED",
    1604: "FIRE_PROTECTION_TRIGGERED", 1605: "EMERGENCY_STOP_TRIGGERED",
    
    # SYSTEM
    1701: "DEVICE_ABNORMAL", 1702: "GRID_PROTECTION_SELF_CHECK_FAILURE", 1703: "SYSTEM_SELF_CHECK_FAILURE",
    1704: "SOFTWARE_EXCEPTION", 1705: "FIRMWARE_UPGRADE_FAILURE", 1706: "CONFIGURATION_ERROR",
    1707: "SYSTEM_ALARM", 

    # DERATING
    1801: "POWER_DERATING", 1802: "TEMPERATURE_DERATING", 1803: "GRID_LIMIT_DERATING",
    1804: "FREQUENCY_DERATING", 1805: "POWER_LIMIT_CONTROL",
}

SUNGROW_FAULT_MAP = {
    # --- GRID FAULTS ---
    2: {"id_sungrow": 2, "id_unified": 1001, "name": "GRID_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage and transformer tap setting."},
    3: {"id_sungrow": 3, "id_unified": 1001, "name": "GRID_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage and transformer tap setting."},
    14: {"id_sungrow": 14, "id_unified": 1001, "name": "GRID_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage at AC terminals."},
    15: {"id_sungrow": 15, "id_unified": 1001, "name": "GRID_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage at AC terminals."},
    4: {"id_sungrow": 4, "id_unified": 1003, "name": "GRID_UNDERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage level and AC connection."},
    5: {"id_sungrow": 5, "id_unified": 1003, "name": "GRID_UNDERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage level and AC connection."},
    8: {"id_sungrow": 8, "id_unified": 1005, "name": "GRID_OVER_FREQUENCY", "severity": "ERROR", "repair_instruction": "Check grid frequency stability."},
    9: {"id_sungrow": 9, "id_unified": 1006, "name": "GRID_UNDER_FREQUENCY", "severity": "ERROR", "repair_instruction": "Check utility grid frequency."},
    10: {"id_sungrow": 10, "id_unified": 1007, "name": "GRID_POWER_OUTAGE", "severity": "ERROR", "repair_instruction": "Check AC circuit breaker and grid status."},
    12: {"id_sungrow": 12, "id_unified": 1201, "name": "EXCESS_LEAKAGE_CURRENT", "severity": "ERROR", "repair_instruction": "Check insulation of PV strings and AC cables."},
    13: {"id_sungrow": 13, "id_unified": 1010, "name": "GRID_ABNORMAL", "severity": "ERROR", "repair_instruction": "Check grid stability and connection status."},
    17: {"id_sungrow": 17, "id_unified": 1008, "name": "GRID_VOLTAGE_UNBALANCE", "severity": "ERROR", "repair_instruction": "Check three-phase grid voltage balance."},
    323: {"id_sungrow": 323, "id_unified": 1016, "name": "GRID_PHASE_CONFRONTATION", "severity": "ERROR", "repair_instruction": "Check grid connection and phase sequence."},

    # --- PV & DC FAULTS (Bao gồm các dải mã 448-479, 532-595, 264-283) ---
    28: {"id_sungrow": 28, "id_unified": 1101, "name": "PV_REVERSE_CONNECTION", "severity": "ERROR", "repair_instruction": "Check PV string polarity."},
    29: {"id_sungrow": 29, "id_unified": 1101, "name": "PV_REVERSE_CONNECTION", "severity": "ERROR", "repair_instruction": "Check PV string polarity."},
    208: {"id_sungrow": 208, "id_unified": 1101, "name": "PV_REVERSE_CONNECTION", "severity": "ERROR", "repair_instruction": "Check PV string polarity."},
    
    # PV Reserve Connection (Dải 448-479)
    **{i: {"id_sungrow": i, "id_unified": 1101, "name": "PV_REVERSE_CONNECTION", "severity": "ERROR", "repair_instruction": "Check PV string polarity."} for i in range(448, 480)},
    
    # PV Reverse Connection Alarm (Dải 532-547 và 564-579)
    **{i: {"id_sungrow": i, "id_unified": 1111, "name": "PV_STRING_REVERSE_ALARM", "severity": "WARNING", "repair_instruction": "Check PV string polarity."} for i in range(532, 548)},
    **{i: {"id_sungrow": i, "id_unified": 1111, "name": "PV_STRING_REVERSE_ALARM", "severity": "WARNING", "repair_instruction": "Check PV string polarity."} for i in range(564, 580)},

    # PV Abnormal Alarm (Dải 548-563 và 580-595)
    **{i: {"id_sungrow": i, "id_unified": 1104, "name": "PV_INPUT_ABNORMAL", "severity": "WARNING", "repair_instruction": "Inspect PV string status."} for i in range(548, 564)},
    **{i: {"id_sungrow": i, "id_unified": 1104, "name": "PV_INPUT_ABNORMAL", "severity": "WARNING", "repair_instruction": "Inspect PV string status."} for i in range(580, 596)},

    # MPPT Reverse Connection (Dải 264-283)
    **{i: {"id_sungrow": i, "id_unified": 1101, "name": "MPPT_REVERSE_CONNECTION", "severity": "ERROR", "repair_instruction": "Check MPPT input wiring."} for i in range(264, 284)},

    # String Current Reflux (Dải 1548-1579)
    **{i: {"id_sungrow": i, "id_unified": 1105, "name": "PV_STRING_FAULT", "severity": "WARNING", "repair_instruction": "Check for current reflux in PV strings."} for i in range(1548, 1580)},

    # PV Grounding Fault (Dải 1600-1611)
    **{i: {"id_sungrow": i, "id_unified": 1206, "name": "PV_GROUND_FAULT", "severity": "ERROR", "repair_instruction": "Inspect PV DC grounding system."} for i in range(1600, 1612)},

    # --- ELECTRICAL & SAFETY ---
    39: {"id_sungrow": 39, "id_unified": 1202, "name": "LOW_INSULATION_RESISTANCE", "severity": "ERROR", "repair_instruction": "Check insulation resistance of DC cables."},
    106: {"id_sungrow": 106, "id_unified": 1206, "name": "GROUNDING_CABLE_FAULT", "severity": "ERROR", "repair_instruction": "Check grounding cable connection."},
    88: {"id_sungrow": 88, "id_unified": 1601, "name": "ARC_FAULT", "severity": "ERROR", "repair_instruction": "Inspect DC cables for arc fault."},
    84: {"id_sungrow": 84, "id_unified": 1507, "name": "METER_CT_REVERSE_CONNECTION", "severity": "WARNING", "repair_instruction": "Check Meter/CT wiring polarity."},
    514: {"id_sungrow": 514, "id_unified": 1502, "name": "METER_COMM_FAULT", "severity": "DISCONNECT", "repair_instruction": "Check communication cable to Smart Meter."},
    75: {"id_sungrow": 75, "id_unified": 1501, "name": "PARALLEL_COMM_ALARM", "severity": "WARNING", "repair_instruction": "Check parallel communication cables."},

    # --- TEMPERATURE ---
    37: {"id_sungrow": 37, "id_unified": 1302, "name": "HIGH_AMBIENT_TEMPERATURE", "severity": "ERROR", "repair_instruction": "Improve ventilation and cooling surroundings."},
    43: {"id_sungrow": 43, "id_unified": 1303, "name": "LOW_AMBIENT_TEMPERATURE", "severity": "WARNING", "repair_instruction": "Ensure ambient temperature is within range."},

    # --- HARDWARE & CAPACITORS ---
    # Boost Capacitor Overvoltage Alarm (332-363)
    **{i: {"id_sungrow": i, "id_unified": 1411, "name": "DC_BUS_CAPACITOR_FAULT", "severity": "WARNING", "repair_instruction": "Internal capacitor warning. Monitor device."} for i in range(332, 364)},
    # Boost Capacitor Overvoltage Fault (364-395)
    **{i: {"id_sungrow": i, "id_unified": 1411, "name": "DC_BUS_CAPACITOR_FAULT", "severity": "ERROR", "repair_instruction": "Internal hardware fault. Contact service."} for i in range(364, 396)},
    
    1616: {"id_sungrow": 1616, "id_unified": 1409, "name": "SYSTEM_HARDWARE_FAULT", "severity": "ERROR", "repair_instruction": "Contact technical support for board inspection."},

    # --- SYSTEM FAULT (Dải mã lớn nhất 7 - 1122) ---
    # Bao gồm các mã lẻ và dải mã trong tài liệu: 19-25, 30-34, 40-42, 44-50, 52-58, 60-68...
    **{i: {"id_sungrow": i, "id_unified": 1701, "name": "SYSTEM_FAULT", "severity": "ERROR", "repair_instruction": "Internal system error. Restart inverter."} 
       for i in (
           [7, 11, 16, 36, 38, 85, 87, 92, 93, 605, 608, 612, 616, 620, 622, 623, 624, 800, 802, 804, 807] +
           [x for r in [(19,25), (30,34), (40,42), (44,50), (52,58), (60,68), (100,105), (107,114), (116,124), (200,211), (248,255), (300,322), (324,326), (401,412), (600,603), (1096, 1122)] for x in range(r[0], r[1] + 1)]
       )},

    # --- SYSTEM ALARM (Các mã cảnh báo hệ thống) ---
    **{i: {"id_sungrow": i, "id_unified": 1707, "name": "SYSTEM_ALARM", "severity": "WARNING", "repair_instruction": "Internal system warning. Monitor performance."}
       for i in (
           [59, 74, 76, 82, 83, 89, 900, 901, 910, 911, 635, 636, 637, 638] +
           [x for r in [(70,72), (77,81), (216,218), (220,231), (432,434), (500,513), (515,518)] for x in range(r[0], r[1] + 1)]
       )}
}

SUNGROW_STATE_MAP = {
    0: {"id_sungrow": 0, "id_unified": 2, "name": "STANDBY", "severity": "STABLE", "description": "Standby"},
    1: {"id_sungrow": 1, "id_unified": 3, "name": "STARTING", "severity": "WARNING", "description": "Starting"},
    2: {"id_sungrow": 2, "id_unified": 1, "name": "RUNNING", "severity": "STABLE", "description": "Running normally"},
    3: {"id_sungrow": 3, "id_unified": 6, "name": "ALARM_RUNNING", "severity": "WARNING", "description": "Running with alarm"},
    4: {"id_sungrow": 4, "id_unified": 7, "name": "DERATING", "severity": "WARNING", "description": "Derating"},
    5: {"id_sungrow": 5, "id_unified": 8, "name": "DISPATCH_RUNNING", "severity": "WARNING", "description": "Dispatch running"},
    6: {"id_sungrow": 6, "id_unified": 4, "name": "STOPPED", "severity": "ERROR", "description": "Stopped"},
    7: {"id_sungrow": 7, "id_unified": 5, "name": "FAULT", "severity": "ERROR", "description": "Fault"},
    8: {"id_sungrow": 8, "id_unified": 10, "name": "EMERGENCY_STOP", "severity": "ERROR", "description": "Emergency stop"},
    9: {"id_sungrow": 9, "id_unified": 11, "name": "KEY_STOP", "severity": "ERROR", "description": "Key stop"},
    10: {"id_sungrow": 10, "id_unified": 20, "name": "POWER_LIMITED", "severity": "WARNING", "description": "Power limited"},
}

HUAWEI_FAULT_MAP = {
    200: {"id_huawei": 200, "id_unified": 0, "name": "RUNNING", "severity": "STABLE", "repair_instruction": "Normal."},
    201: {"id_huawei": 201, "id_unified": 1001, "name": "GRID_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage."},
    202: {"id_huawei": 202, "id_unified": 1003, "name": "GRID_UNDERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check grid voltage."},
    203: {"id_huawei": 203, "id_unified": 1005, "name": "GRID_OVERFREQUENCY", "severity": "ERROR", "repair_instruction": "Check frequency."},
    204: {"id_huawei": 204, "id_unified": 1006, "name": "GRID_UNDERFREQUENCY", "severity": "ERROR", "repair_instruction": "Check frequency."},
    205: {"id_huawei": 205, "id_unified": 1007, "name": "GRID_LOSS", "severity": "ERROR", "repair_instruction": "Check AC breaker."},
    206: {"id_huawei": 206, "id_unified": 1009, "name": "GRID_PHASE_FAULT", "severity": "ERROR", "repair_instruction": "Check phase sequence."},
    2011: {"id_huawei": 2011, "id_unified": 1102, "name": "DC_OVERVOLTAGE", "severity": "ERROR", "repair_instruction": "Check PV voltage."},
    2012: {"id_huawei": 2012, "id_unified": 1202, "name": "DC_INSULATION_FAULT", "severity": "ERROR", "repair_instruction": "Check insulation."},
    2013: {"id_huawei": 2013, "id_unified": 1206, "name": "GROUND_FAULT", "severity": "ERROR", "repair_instruction": "Check grounding."},
    2014: {"id_huawei": 2014, "id_unified": 1201, "name": "LEAKAGE_CURRENT", "severity": "ERROR", "repair_instruction": "Check leakage."},
    2015: {"id_huawei": 2015, "id_unified": 1105, "name": "STRING_FAULT", "severity": "WARNING", "repair_instruction": "Check connectors."},
    2021: {"id_huawei": 2021, "id_unified": 1301, "name": "OVER_TEMPERATURE", "severity": "ERROR", "repair_instruction": "Check ventilation."},
    2022: {"id_huawei": 2022, "id_unified": 1401, "name": "FAN_FAULT", "severity": "WARNING", "repair_instruction": "Check fan."},
}

# 
# Key = Decimal value of the official Huawei hex state code (e.g. 0x0200 = 512)
# Retrieved from Modbus register 32089 (uint16)
HUAWEI_STATE_MAP = {
    # Standby & khởi động
    0:    {"id_huawei": 0,    "id_unified": 12, "name": "INITIAL_STANDBY", "severity": "STABLE",  "description": "Inverter initialized and waiting"},
    1:    {"id_huawei": 1,    "id_unified": 13, "name": "GRID_DETECTING",  "severity": "STABLE", "description": "Detecting grid parameters"},
    2:    {"id_huawei": 2,    "id_unified": 14, "name": "INSULATION_CHECK","severity": "STABLE", "description": "Performing insulation resistance test"},
    3:    {"id_huawei": 3,    "id_unified": 15, "name": "SELF_CHECK",      "severity": "STABLE", "description": "Self check before startup"},
    256:  {"id_huawei": 256,  "id_unified": 3,  "name": "STARTING",        "severity": "STABLE", "description": "Inverter starting"},

    # Vận hành
    512:  {"id_huawei": 512,  "id_unified": 1,  "name": "RUNNING",         "severity": "STABLE",  "description": "Inverter running normally"},
    513:  {"id_huawei": 513,  "id_unified": 7,  "name": "DERATING",        "severity": "WARNING", "description": "Running with power derating"},
    514:  {"id_huawei": 514,  "id_unified": 20, "name": "POWER_LIMITED",   "severity": "WARNING", "description": "Grid connection power limited"},
    515:  {"id_huawei": 515,  "id_unified": 16, "name": "OFF_GRID_RUNNING","severity": "WARNING",  "description": "Off-grid running mode"},
    2560: {"id_huawei": 2560, "id_unified": 8,  "name": "DISPATCH_RUNNING","severity": "WARNING",  "description": "Off-grid charging / dispatch running"},

    # Shutdown
    768:  {"id_huawei": 768,  "id_unified": 5,  "name": "FAULT",           "severity": "ERROR",   "description": "Fault condition detected"},
    769:  {"id_huawei": 769,  "id_unified": 19, "name": "SHUTTING_DOWN",   "severity": "WARNING", "description": "Shutdown in progress"},
    770:  {"id_huawei": 770,  "id_unified": 9,  "name": "COMMUNICATION_FAULT","severity": "ERROR","description": "Communication disconnected"},
    771:  {"id_huawei": 771,  "id_unified": 10, "name": "EMERGENCY_STOP",  "severity": "ERROR",   "description": "Emergency stop triggered"},
    772:  {"id_huawei": 772,  "id_unified": 20, "name": "POWER_LIMITED",   "severity": "WARNING", "description": "Shutdown due to power limit"},
    773:  {"id_huawei": 773,  "id_unified": 11, "name": "KEY_STOP",        "severity": "ERROR",   "description": "Manual key stop"},
    774:  {"id_huawei": 774,  "id_unified": 4,  "name": "STOPPED",         "severity": "ERROR",   "description": "DC switches disconnected"},
    775:  {"id_huawei": 775,  "id_unified": 19, "name": "SHUTTING_DOWN",   "severity": "WARNING", "description": "Rapid cutoff"},
    776:  {"id_huawei": 776,  "id_unified": 5,  "name": "FAULT",           "severity": "ERROR",   "description": "Input underpower"},

    # Grid scheduling
    1025: {"id_huawei": 1025, "id_unified": 23, "name": "GRID_SCHEDULING_COSPHI_P", "severity": "STABLE", "description": "cosφ–P curve scheduling"},
    1026: {"id_huawei": 1026, "id_unified": 24, "name": "GRID_SCHEDULING_Q_U",      "severity": "STABLE", "description": "Q–U curve scheduling"},
    1027: {"id_huawei": 1027, "id_unified": 25, "name": "GRID_SCHEDULING_PF_U",     "severity": "STABLE", "description": "PF–U curve scheduling"},
    1028: {"id_huawei": 1028, "id_unified": 26, "name": "GRID_SCHEDULING_DRY_CONTACT","severity":"STABLE","description": "Dry contact scheduling"},
    1029: {"id_huawei": 1029, "id_unified": 27, "name": "GRID_SCHEDULING_Q_P",      "severity": "STABLE", "description": "Q–P curve scheduling"},

    # Kiểm tra & chẩn đoán
    1280: {"id_huawei": 1280, "id_unified": 28, "name": "SPOT_CHECK_READY", "severity": "STABLE",  "description": "Ready for spot check"},
    1281: {"id_huawei": 1281, "id_unified": 29, "name": "SPOT_CHECKING",    "severity": "WARNING", "description": "Performing spot check"},
    1536: {"id_huawei": 1536, "id_unified": 30, "name": "INSPECTING",       "severity": "WARNING", "description": "Inspection in progress"},
    1792: {"id_huawei": 1792, "id_unified": 31, "name": "AFCI_SELF_CHECK",  "severity": "WARNING", "description": "Arc fault circuit interrupter self check"},
    2048: {"id_huawei": 2048, "id_unified": 32, "name": "IV_SCANNING",      "severity": "WARNING", "description": "I-V curve scanning"},
    2304: {"id_huawei": 2304, "id_unified": 33, "name": "DC_INPUT_DETECTION","severity":"WARNING", "description": "DC input detection"},

    # Standby khác
    40960:{"id_huawei": 40960,"id_unified": 22, "name": "SLEEP",            "severity": "DISCONNECT",  "description": "No irradiation, inverter sleeping"}
}


SUNGROW_STATE_MAP = {

    0: {
    "id_sungrow": 0,
    "id_unified": 2,
    "name": "STANDBY",
    "severity": "STABLE",
    "description": "Standby state waiting for solar input"
    },

    1: {
    "id_sungrow": 1,
    "id_unified": 3,
    "name": "STARTING",
    "severity": "WARNING",
    "description": "System starting"
    },

    2: {
    "id_sungrow": 2,
    "id_unified": 1,
    "name": "RUNNING",
    "severity": "STABLE",
    "description": "Inverter running normally"
    },

    3: {
    "id_sungrow": 3,
    "id_unified": 6,
    "name": "ALARM_RUNNING",
    "severity": "WARNING",
    "description": "Running with warning"
    },

    4: {
    "id_sungrow": 4,
    "id_unified": 7,
    "name": "DERATING",
    "severity": "WARNING",
    "description": "Power derating active"
    },

    5: {
    "id_sungrow": 5,
    "id_unified": 8,
    "name": "DISPATCH_RUNNING",
    "severity": "WARNING",
    "description": "Power dispatch or remote control"
    },

    6: {
    "id_sungrow": 6,
    "id_unified": 4,
    "name": "STOPPED",
    "severity": "ERROR",
    "description": "Inverter stopped"
    },

    7: {
    "id_sungrow": 7,
    "id_unified": 5,
    "name": "FAULT",
    "severity": "ERROR",
    "description": "Fault state"
    },

    8: {
    "id_sungrow": 8,
    "id_unified": 10,
    "name": "EMERGENCY_STOP",
    "severity": "ERROR",
    "description": "Emergency stop triggered"
    },

    9: {
    "id_sungrow": 9,
    "id_unified": 11,
    "name": "KEY_STOP",
    "severity": "ERROR",
    "description": "Manual stop via key"
    },

    10: {
    "id_sungrow": 10,
    "id_unified": 20,
    "name": "POWER_LIMITED",
    "severity": "WARNING",
    "description": "Power limited by grid dispatch"
    }
}


class FaultStateService:
    def __init__(self):
        self.state_maps = {
            "HUAWEI": HUAWEI_STATE_MAP,
            "SUNGROW": SUNGROW_STATE_MAP
            }
        self.fault_maps = {
            "HUAWEI": HUAWEI_FAULT_MAP,
            "SUNGROW": SUNGROW_FAULT_MAP
            }


# ============================================================
# ALIASES — dùng cho fault_service.py
# ============================================================

# Dict theo brand: FAULT_MAPS["HUAWEI"] -> HUAWEI_FAULT_MAP
FAULT_MAPS = {
    "HUAWEI": HUAWEI_FAULT_MAP,
    "SUNGROW": SUNGROW_FAULT_MAP,
}

# Dict theo brand: STATE_MAPS["HUAWEI"] -> HUAWEI_STATE_MAP
STATE_MAPS = {
    "HUAWEI": HUAWEI_STATE_MAP,
    "SUNGROW": SUNGROW_STATE_MAP,
}

# Huawei Modbus: map raw status_code từ thanh ghi Modbus 
# sang id_unified (state code trong HUAWEI_STATE_MAP)
# Với Huawei SUN2000, thanh ghi 32089 trả về integer state trực tiếp
# (0=Standby, 1=Grid-connected, 2=Grid-connected normally, ...)
# map này convert về id Huawei state map (0-13)
HUAWEI_MODBUS_MAP = {
    0: 0,    # INITIAL_STANDBY
    1: 5,    # RUNNING
    2: 5,    # RUNNING (grid connected normally)
    3: 6,    # ALARM_RUNNING
    4: 7,    # DERATING
    5: 8,    # STOPPED
    6: 9,    # FAULT
    7: 10,   # UPGRADING
    8: 11,   # SHUTTING_DOWN
    9: 1,    # GRID_DETECTING
    10: 2,   # INSULATION_CHECK
    11: 3,   # SELF_CHECK
    12: 4,   # STARTING
    13: 12,  # GRID_FAULT_WAIT
    14: 13,  # MAINTENANCE_MODE
}
