from database.sqlite_manager import RealtimeDB

class BufferService:
    def __init__(self, realtime_db: RealtimeDB):
        self.db = realtime_db

    def save(self, project_id: int, data: dict):
        """Lưu dữ liệu snapshot vào hàng đợi gửi server"""
        self.db.post_to_outbox(project_id, data)

    def get_all(self):
        """Lấy tất cả bản ghi chờ gửi"""
        return self.db.get_all_outbox()

    def delete(self, record_id: int):
        """Xoá bản ghi sau khi gửi thành công"""
        self.db.delete_from_outbox(record_id)