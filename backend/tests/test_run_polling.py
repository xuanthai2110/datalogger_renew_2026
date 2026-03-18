# tests/test_run_polling.py
"""
Script chạy polling giả lập (hoặc thật) nhưng KHÔNG gửi dữ liệu lên server.
Dùng để kiểm tra luồng đọc Modbus -> Ghi Cache -> Ghi RealtimeDB -> Build Telemetry (Local).
"""

import sys
import os
import logging

# Thêm project root vào path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sqlite_manager import MetadataDB, RealtimeDB, CacheDB
from services.polling_service import PollingService
from services.uploader_service import UploaderService
from services.buffer_service import BufferService
from services.project_service import ProjectService
from services.telemetry_service import TelemetryService
from services.fault_state_service import FaultStateService
import config

# Cấu hình logging - Chi tiết hơn để dễ debug
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test_polling.log", encoding="utf-8")
    ]
)

logger = logging.getLogger("TestRunPolling")

class MockUploader:
    """Uploader giả lập để không gửi dữ liệu thật lên server"""
    def __init__(self, buffer_service):
        self.buffer_service = buffer_service
        
    def upload(self):
        # Chỉ log ra là có dữ liệu trong buffer thay vì gửi đi
        # Tránh việc làm sạch buffer nếu muốn kiểm tra data.json sau đó
        count = self.buffer_service.get_pending_count()
        if count > 0:
            logger.info(f"[MOCK UPLOADER] Có {count} bản ghi telemetry chờ gửi. SKIPPING UPLOAD (Test Mode).")
        return True

def main():
    try:
        logger.info("=== INITIALIZING TEST POLLING SYSTEM (No Upload) ===")
        
        metadata_db = MetadataDB(config.METADATA_DB)
        realtime_db = RealtimeDB(config.REALTIME_DB)
        cache_db = CacheDB(config.CACHE_DB)
        
        project_service = ProjectService(metadata_db, realtime_db)
        buffer_service = BufferService(realtime_db)
        telemetry_service = TelemetryService(project_service, buffer_service)
        
        # Sử dụng MockUploader thay vì UploaderService thật
        uploader = MockUploader(buffer_service)
        fault_service = FaultStateService()
        
        service = PollingService(
            metadata_db, 
            realtime_db, 
            uploader=uploader, 
            telemetry_service=telemetry_service, 
            cache_db=cache_db, 
            fault_service=fault_service
        )
        
        logger.info("Test Polling Service đang chạy... (Nhấn Ctrl+C để dừng)")
        service.run_forever()
        
    except KeyboardInterrupt:
        logger.info("Test Polling Service đã dừng bởi người dùng.")
    except Exception as e:
        logger.error(f"Lỗi nghiêm trọng trong Test Polling Service: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
