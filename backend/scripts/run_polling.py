import sys
import os
import logging
import time
from datetime import datetime

# 1. Thêm PROJECT ROOT vào sys.path để hỗ trợ absolute imports (backend.xxx)
# __file__ = e:\datalogger_project_2102\backend\scripts\run_polling.py
# current_dir = backend/scripts
# parent = backend
# grand_parent = e:\datalogger_project_2102 (ROOT)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 2. Imports chuẩn từ backend package
from backend.database import MetadataDB, CacheDB, RealtimeDB
from backend.workers.polling_worker import PollingWorker
from backend.workers.logic_worker import LogicWorker
from backend.workers.persistence_worker import PersistenceWorker
from backend.workers.uploader_worker import UploaderWorker
from backend.services.fault_service import FaultService
from backend.core import config

# Cấu hình Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("polling.log")]
)
logger = logging.getLogger("Launcher")

def main():
    try:
        logger.info(f"System Path: {sys.path[:3]}") # Debug
        logger.info("Starting Datalogger 6-Threads Modular Architecture...")
        
        # 1. Khởi tạo Database Layer
        metadata_db = MetadataDB(config.METADATA_DB)
        cache_db = CacheDB(config.CACHE_DB)
        realtime_db = RealtimeDB(config.REALTIME_DB)
        
        # 2. Khởi tạo Logic Services
        fault_service = FaultService(realtime_db, metadata_db)
        
        # 3. KHỞI CHẠY WORKERS
        poll_worker = PollingWorker(metadata_db, cache_db, config.POLL_INTERVAL)
        poll_worker.start()
        
        logic_worker = LogicWorker(cache_db, metadata_db, realtime_db, fault_service)
        logic_worker.start()
        
        persist_worker = PersistenceWorker(cache_db, realtime_db, logic_worker.energy_service, config.SNAPSHOT_INTERVAL)
        persist_worker.start()
        
        upload_worker = UploaderWorker(realtime_db, config.SNAPSHOT_INTERVAL)
        upload_worker.start()
        
        logger.info("All workers active.")
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Stopping...")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
