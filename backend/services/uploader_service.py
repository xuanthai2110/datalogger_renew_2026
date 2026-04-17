import requests
import json
import logging
from backend.core.settings import API_BASE_URL
from backend.services.auth_service import AuthService

logger = logging.getLogger(__name__)

class UploaderService:
    def __init__(self, realtime_db):
        self.db = realtime_db
        self.auth = AuthService()
        self.token = None

    def _should_delete_outbox_record(self, response) -> bool:
        """Drop records already accepted earlier by the server."""
        if response.status_code != 409:
            return False

        response_text = response.text or ""
        try:
            body = response.json()
            if isinstance(body, dict):
                detail = body.get("detail")
                if isinstance(detail, str):
                    response_text = detail
        except (ValueError, json.JSONDecodeError, AttributeError, TypeError):
            pass

        normalized = response_text.casefold()
        return "da ton tai" in normalized or "đã tồn tại" in normalized or "already exists" in normalized

    def upload(self):
        token = self.auth.get_access_token()
        if not token: return
        data_list = self.db.get_all_outbox()
        if not data_list: return
        for data in data_list:
            try:
                payload = data.copy()
                payload.pop("id", None)
                payload.pop("project_id", None)
                payload.pop("server_id", None)
                payload.pop("timestamp", None)
                server_id = data.get("server_id")
                if not server_id: continue
                url = f"{API_BASE_URL}/api/telemetry/project/{server_id}"
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers)
                
                # Handle 401 Unauthorized
                if response.status_code == 401:
                    logger.warning(f"Unauthorized (401) for project {server_id}. Attempting token renewal...")
                    new_token = self.auth.handle_unauthorized()
                    if new_token:
                        token = new_token # Update token for current and future items in loop
                        headers["Authorization"] = f"Bearer {token}"
                        logger.info(f"Retrying upload for project {server_id} with new token...")
                        response = requests.post(url, json=payload, headers=headers)

                if response.status_code in (200, 201):
                    self.db.delete_from_outbox(data["id"])
                    logger.info(f"Uploaded project {server_id} (status={response.status_code})")
                elif self._should_delete_outbox_record(response):
                    self.db.delete_from_outbox(data["id"])
                    logger.info(
                        f"Dropped duplicate outbox record for project {server_id} "
                        f"(status={response.status_code}): {response.text}"
                    )
                else:
                    logger.warning(f"Upload failed for project {server_id} (status={response.status_code}): {response.text}")
            except Exception as e:
                logger.error(f"Upload error: {e}")

    def send_immediate(self, data: dict):
        token = self.auth.get_access_token()
        if not token: return
        server_id = data.get("server_id")
        payload = data.copy()
        payload.pop("project_id", None)
        payload.pop("server_id", None)
        payload.pop("timestamp", None)
        if not server_id: return
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{API_BASE_URL}/api/telemetry/project/{server_id}"
        try:
            logger.info(f"Sending immediate update for {server_id}...")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 401:
                logger.warning(f"Unauthorized (401) on immediate send for {server_id}. Attempting token renewal...")
                new_token = self.auth.handle_unauthorized()
                if new_token:
                    headers["Authorization"] = f"Bearer {new_token}"
                    logger.info(f"Retrying immediate send for {server_id} with new token...")
                    requests.post(url, json=payload, headers=headers, timeout=10)
        except Exception as e:
            logger.error(f"Immediate send error: {e}")
