import sys
import os
import logging
import time
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Imports using absolute package names
from backend.database import MetadataDB, CacheDB, RealtimeDB
from backend.workers.polling_worker import PollingWorker
from backend.workers.logic_worker import LogicWorker
from backend.workers.persistence_worker import PersistenceWorker
from backend.workers.uploader_worker import UploaderWorker
from backend.services.fault_service import FaultService
from backend.core import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MainLauncher")

def main():
    try:
        logger.info("Initializing Modular 6-Threads Datalogger...")
        
        # 1. DB Layer
        metadata_db = MetadataDB(config.METADATA_DB)
        cache_db = CacheDB(config.CACHE_DB)
        realtime_db = RealtimeDB(config.REALTIME_DB)
        
        # 2. Service Layer
        fault_service = FaultService(realtime_db, metadata_db)
        
        # 3. Worker Layer
        poll_worker = PollingWorker(metadata_db, cache_db, config.POLL_INTERVAL)
        logic_worker = LogicWorker(cache_db, metadata_db, realtime_db, fault_service)
        persist_worker = PersistenceWorker(cache_db, realtime_db, logic_worker.energy_service, config.SNAPSHOT_INTERVAL)
        upload_worker = UploaderWorker(realtime_db, config.SNAPSHOT_INTERVAL)
        
        # Start Threads
        poll_worker.start()
        logic_worker.start()
        persist_worker.start()
        upload_worker.start()
        
        logger.info("System operational.")
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Shutdown requested.")
    except Exception as e:
        logger.error(f"Critical startup failure: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
