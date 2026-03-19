"""
TEST: Đọc inverter từ MetadataDB -> Polling thực tế -> FaultStateService -> In kết quả mapping
Chạy: python backend/tests/test_fault_mapping.py
"""
import sys
import os
import json
import logging

# Thêm project root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sqlite_manager import MetadataDB
from services.fault_state_service import FaultStateService
from communication.modbus_tcp import ModbusTCP
from communication.modbus_rtu import ModbusRTU
from drivers.huawei_sun2000110KTL import HuaweiSUN2000
import config

# Tắt log modbus để output sạch
logging.getLogger("pymodbus").setLevel(logging.WARNING)

def get_transport(brand: str):
    if "Huawei" in brand:
        t = ModbusTCP(host=config.MODBUS_TCP_HOST, port=config.MODBUS_TCP_PORT)
        if t.connect():
            return t
    else:
        t = ModbusRTU(port=config.MODBUS_PORT, baudrate=config.MODBUS_BAUDRATE)
        if t.connect():
            return t
    return None

def get_driver(brand: str, transport, slave_id: int):
    if "Huawei" in brand:
        return HuaweiSUN2000(transport, slave_id=slave_id)
    # Thêm brand khác nếu cần
    return None

def run_live_test():
    metadata_db = MetadataDB(config.METADATA_DB)
    fault_service = FaultStateService()
    
    print("\n" + "="*70)
    print("  LIVE FAULT MAPPING TEST - Đọc từ Inverter thực tế")
    print("="*70)
    
    inverters = metadata_db.get_all_inverters()
    active_inverters = [inv for inv in inverters if inv.is_active]
    
    if not active_inverters:
        print("  [!] Không tìm thấy inverter active nào trong MetadataDB.")
        return

    # Gom nhóm theo brand để tối ưu transport
    brands = set(inv.brand for inv in active_inverters)
    transports = {}
    
    for brand in brands:
        print(f"\n📡 Đang kết nối tới brand: {brand}...")
        t = get_transport(brand)
        if t:
            transports[brand] = t
            print(f"  [OK] Đã kết nối.")
        else:
            print(f"  [FAIL] Không thể kết nối tới {brand}.")

    for inv in active_inverters:
        transport = transports.get(inv.brand)
        if not transport:
            continue
            
        print(f"\n--- [INV {inv.id}] SN: {inv.serial_number} | Slave ID: {inv.slave_id} ---")
        
        try:
            driver = get_driver(inv.brand, transport, inv.slave_id)
            if not driver:
                print(f"  [!] Không tìm thấy driver cho brand {inv.brand}")
                continue
                
            # Đọc registers trạng thái
            # Huawei: 32089 (State), 32090 (Fault)
            print(f"  🔍 Đang đọc data...")
            raw_data = driver.read_all()
            
            if not raw_data:
                print(f"  ❌ Lỗi: Không phản hồi.")
                continue
            
            raw_state = raw_data.get("state_id", 0)
            raw_fault = raw_data.get("fault_code", 0)
            
            # Mapping
            mapped_payload = fault_service.get_inverter_status_payload(inv.brand, raw_state, raw_fault)
            
            # In kết quả
            print(f"  [RAW] State: {raw_state} ({hex(raw_state)}) | Fault: {raw_fault}")
            print(f"  [MAPPED PAYLOAD]:")
            print(json.dumps(mapped_payload, indent=4, ensure_ascii=False))
            
        except Exception as e:
            print(f"  ❌ Lỗi khi đọc inverter {inv.id}: {e}")

    # Đóng kết nối
    for t in transports.values():
        t.close()

    print("\n" + "="*70)
    print("  Hoàn tất kiểm tra live.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_live_test()
