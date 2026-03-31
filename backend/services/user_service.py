import logging
from typing import Optional, List
from backend.models.user import UserCreate
from backend.services.local_auth_utils import hash_password

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, metadata_db):
        self.metadata_db = metadata_db

    def get_user_by_name(self, username: str) -> Optional[dict]:
        return self.metadata_db.get_user_by_name(username)

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        return self.metadata_db.get_user_by_id(user_id)

    def get_users(self) -> List[dict]:
        # Ghi chú: Có thể thêm hàm get_all_users() vào MetadataDB nếu cần list toàn bộ user
        try:
            return self.metadata_db.get_users()
        except AttributeError:
            return []

    def create_user(self, data: UserCreate) -> int:
        """Tạo user mới, đã băm mật khẩu từ ngoài hoặc băm ở đây."""
        return self.metadata_db.create_user(data)

    def create_admin_if_not_exists(self, default_password: str = "admin123"):
        """Khởi tạo tài khoản admin mặc định nếu chưa tồn tại."""
        try:
            if not self.get_user_by_name("admin"):
                logger.info("Initializing default admin user...")
                pwd = hash_password(default_password)
                admin_user = UserCreate(
                    username="admin", 
                    password=pwd, 
                    email="admin@localhost", 
                    role="admin"
                )
                self.create_user(admin_user)
                logger.info("Admin user created with default password 'admin123'. Please change it later.")
        except Exception as e:
            logger.error(f"Error creating default admin: {e}")
