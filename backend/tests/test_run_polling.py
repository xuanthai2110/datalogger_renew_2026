# tests/test_run_polling.py
"""
Script chạy polling thực tế nhưng KHÔNG gửi dữ liệu lên server.
Dùng để kiểm tra:
1. Luồng đọc Modbus từ Inverter.
2. Mapping trạng thái (Raw vs Unified).
3. Đóng gói Telemetry JSON (Lưu vào data.json thay vì gửi server).
"""

import sys
import os
import logging
import json
import time

# Thêm project root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sqlite_manager import MetadataDB, RealtimeDB, CacheDB
from services.polling_service import PollingService
from services.buffer_service import BufferService
from services.project_service import ProjectService
from services.telemetry_service import TelemetryService
from services.fault_state_service import FaultStateService
import config

# Cấu hình logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s | %(levelname)s | %(message)s')
logging.getLogger("pymodbus").setLevel(logging.WARNING)
logging.getLogger("services.polling_service").setLevel(logging.WARNING)

# Logger riêng cho script test
test_logger = logging.getLogger("TestConsole")
test_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%H:%M:%S | %(message)s'))
test_logger.addHandler(console_handler)
test_logger.propagate = False

class MockUploader:
    """Mock Uploader: Ghi payload ra file data.json thay vì gửi lên server"""
    def __init__(self, buffer_service):
        self.buffer_service = buffer_service
        self.output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data.json")
        
    def upload(self):
        records = self.buffer_service.get_all()
        if not records:
            return True
        
        test_logger.info(f"🚀 [SERVER] Chặn upload {len(records)} records. Đang ghi payload ra data.json...")
        
        try:
            # Lấy record mới nhất
            latest_record = records[-1]
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(latest_record, f, indent=4, ensure_ascii=False)
            test_logger.info(f"💾 [FILE] Đã lưu telemetry vào: {self.output_path}")
            
            # In tóm tắt Errors Payload của record cuối
            inv_list = latest_record.get("inverters", [])
            for inv in inv_list:
                sn = inv.get("serial_number", "N/A")
                errs = inv.get("errors", [])
                if errs:
                    test_logger.info(f"   └─ [INV {sn}] Errors Status: {errs[0].get('fault_description')} (Severity: {errs[0].get('severity')})")
        except Exception as e:
            test_logger.error(f"❌ [FILE] Lỗi khi ghi file: {e}")

        # Xoá buffer để tránh tích tụ
        for rec in records:
            self.buffer_service.delete(rec["id"])
        return True

def main():
    test_logger.info("="*65)
    test_logger.info("  BẮT ĐẦU SYSTEM TEST: POLLING & TELEMETRY (NO UPLOAD)")
    test_logger.info("="*65)

    # 1. Khởi tạo Database
    metadata_db = MetadataDB(config.METADATA_DB)
    realtime_db = RealtimeDB(config.REALTIME_DB)
    cache_db = CacheDB(config.CACHE_DB)
    
    # 2. Khởi tạo Services
    project_service = ProjectService(metadata_db, realtime_db)
    buffer_service = BufferService(realtime_db)
    telemetry_service = TelemetryService(project_service, buffer_service)
    fault_service = FaultStateService()
    uploader = MockUploader(buffer_service)
    
    polling_service = PollingService(
        metadata_db, 
        realtime_db, 
        uploader=uploader, 
        telemetry_service=telemetry_service, 
        cache_db=cache_db, 
        fault_service=fault_service
    )

    # 3. Patching để log thông tin chi tiết
    original_poll = polling_service.poll_all_inverters
    def patched_poll(project_id):
        test_logger.info(f"🔍 [POLL] Quét Project {project_id}...")
        p_total = original_poll(project_id)
        
        # Log trạng thái thô từng inverter từ buffer
        for inv_id, data in polling_service.buffer.items():
            raw_state = data.get("state_id", 0)
            raw_fault = data.get("fault_code", 0)
            mapped_state = data.get("state_name", "Unknown")
            mapped_fault = data.get("fault_description") or "None"
            
            test_logger.info(f"   ├─ [INV {inv_id}] Raw: State={raw_state} ({hex(raw_state)}) | Fault={raw_fault}")
            test_logger.info(f"   └─ [INV {inv_id}] Map: {mapped_state} | Status: {mapped_fault}")
            
        test_logger.info(f"✅ [READ] Hoàn tất. Tổng AC: {p_total:.2f} W")
        return p_total

    original_send_immediate = polling_service._check_and_send_immediate
    def patched_send_immediate(inv, raw_data):
        # Kiểm tra xem có thay đổi làm trigger gửi ngay không
        old_state = polling_service.last_states.get(inv.id)
        old_fault = polling_service.last_faults.get(inv.id)
        
        new_state = raw_data.get("state_id")
        new_fault = raw_data.get("fault_code", 0)
        
        if old_state is not None and (old_state != new_state or old_fault != new_fault):
            test_logger.warning(f"🚨 [TRIGGER] Phát hiện thay đổi trên Inverter {inv.id}!")
            test_logger.warning(f"   └─ State: {old_state} -> {new_state} | Fault: {old_fault} -> {new_fault}")
        
        return original_send_immediate(inv, raw_data)

    original_build_and_buffer = telemetry_service.build_and_buffer
    def patched_build_and_buffer(project_id):
        test_logger.info(f"⚡ [PAYLOAD] Đang tạo telemetry snapshot...")
        res = original_build_and_buffer(project_id)
        if res:
            test_logger.info("✅ [PAYLOAD] Payload mới đã sẵn sàng trong buffer.")
        return res

    # Áp dụng patch
    polling_service.poll_all_inverters = patched_poll
    polling_service._check_and_send_immediate = patched_send_immediate
    telemetry_service.build_and_buffer = patched_build_and_buffer

    try:
        # Chạy vòng lặp polling
        polling_service.run_forever()
    except KeyboardInterrupt:
        test_logger.info("\n" + "="*65)
        test_logger.info("  ĐÃ DỪNG HỆ THỐNG TEST.")
        test_logger.info("="*65)
    except Exception as e:
        test_logger.error(f"🔥 LỖI THỰC THI: {e}", exc_info=True)

if __name__ == "__main__":
    main()
