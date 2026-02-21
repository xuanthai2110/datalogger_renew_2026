import time
from services.poller_service import PollerService
from services.uploader_service import UploaderService
from services.buffer_service import BufferService
from core.logger import get_logger

logger = get_logger()

def main():
    buffer_service = BufferService()
    uploader = UploaderService(buffer_service)
    poller = PollerService(buffer_service)

    logger.info("Starting datalogger...")

    while True:
        try:
            poller.poll()
            uploader.upload()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()