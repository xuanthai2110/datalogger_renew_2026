from typing import List, Optional
import logging
from backend.db_manager.realtime import RealtimeDB
from backend.models.schedule import ControlScheduleCreate, ControlScheduleUpdate, ControlScheduleResponse

logger = logging.getLogger(__name__)

class ScheduleService:
    def __init__(self, db: RealtimeDB):
        self.db = db

    def get_all(self) -> List[ControlScheduleResponse]:
        return self.db.get_all_schedules()

    def get(self, schedule_id: int) -> Optional[ControlScheduleResponse]:
        return self.db.get_schedule(schedule_id)

    def create(self, data: ControlScheduleCreate) -> ControlScheduleResponse:
        logger.info(f"[ScheduleService] Creating schedule: {data}")
        return self.db.upsert_schedule(data)

    def update(self, schedule_id: int, data: ControlScheduleUpdate):
        logger.info(f"[ScheduleService] Updating schedule {schedule_id}")
        self.db.patch_schedule(schedule_id, data)

    def update_status(self, schedule_id: int, status: str):
        logger.info(f"[ScheduleService] Updating status of schedule {schedule_id} to {status}")
        self.db.patch_schedule(schedule_id, ControlScheduleUpdate(status=status))

    def delete(self, schedule_id: int):
        logger.info(f"[ScheduleService] Deleting schedule {schedule_id}")
        self.db.delete_schedule(schedule_id)
