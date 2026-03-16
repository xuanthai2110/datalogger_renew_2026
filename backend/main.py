import time
import logging
import config
from database.sqlite_manager import MetadataDB, RealtimeDB
from services.polling_service import PollingService
from services.uploader_service import UploaderService
from services.buffer_service import BufferService
from services.project_service import ProjectService
from services.telemetry_service import TelemetryService
from logger_config import get_logger

logger = get_logger()

def main():
    metadata_db = MetadataDB(config.METADATA_DB)
    realtime_db = RealtimeDB(config.REALTIME_DB)
    
    project_service = ProjectService(metadata_db, realtime_db)
    buffer_service = BufferService(realtime_db)
    telemetry_service = TelemetryService(project_service, buffer_service)
    
    uploader = UploaderService(buffer_service)
    poller = PollingService(metadata_db, realtime_db, uploader, telemetry_service)

    logger.info("Starting datalogger service with Telemetry support...")
    
    try:
        # PollingService.run_forever handles the loop, night mode, and 10s interval
        poller.run_forever()
    except KeyboardInterrupt:
        logger.info("Datalogger stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()