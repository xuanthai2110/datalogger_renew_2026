# Tài liệu Kỹ thuật: Luồng Polling & Thu thập Dữ liệu

Tài liệu này mô tả chi tiết kiến trúc và luồng thực hiện của hệ thống Polling trong Datalogger, bao gồm các service, hàm quan trọng và quy trình tương tác.

---

## 1. Kiến trúc Service
Hệ thống được thiết kế theo mô hình Service-Oriented nhằm tách biệt trách nhiệm:

| Service | Vai trò | Hàm quan trọng |
|---|---|---|
| `main.py` | Orchestration (Khởi tạo và chạy luồng chính) | `main()` |
| `PollingService` | Điều phối việc quét dữ liệu và quản lý Snapshot | `run_forever()`, `poll_all_inverters()`, `save_to_database()` |
| `ProjectService` | Tổng hợp dữ liệu từ nhiều bảng DB thành snapshot | `get_project_snapshot()` |
| `TelemetryService` | Đóng gói JSON theo format Server | `build_and_buffer()`, `_build_payload()` |
| `BufferService` | Quản lý hàng đợi gửi dữ liệu (Outbox) | `save()`, `get_all()`, `delete()` |
| `RealtimeDB` | Tương tác SQLite cho dữ liệu thực tế | `post_inverter_ac_batch()`, `upsert_latest_realtime()`, `post_to_outbox()` |
| `UploaderService` | Gửi dữ liệu lên Server qua API | `upload()`, `send_immediate()` |
| `NormalizationService` | Chuẩn hóa đơn vị và kiểm tra giải giá trị | `normalize()` |
| `TrackingService` | Tính toán năng lượng tháng và giá trị MAX | `update_energy()`, `update_max_values()` |

---

## 2. Quy trình Chi tiết (Polling Flow)

### Giai đoạn 1: Chu kỳ Quét (Mỗi 10 giây)
1. **`PollingService.run_forever()`**: Gọi `metadata_db.get_all_projects()` để lấy danh sách dự án.
2. **`poll_all_inverters(project_id)`**:
    - Kiểm tra danh sách Inverter của dự án.
    - Với mỗi Inverter:
        - Gọi **Driver** (`read_all()`) để lấy dữ liệu qua Modbus.
        - **`TrackingService.update_energy()`**: Tính năng lượng lũy kế.
        - **`NormalizationService.normalize()`**: Làm sạch dữ liệu.
        - **`RealtimeDB.upsert_latest_realtime()`**: Lưu bản ghi 10s vào bảng `latest_realtime` (để Web UI local truy cập).
        - **`_check_and_send_immediate()`**: Nếu trạng thái/lỗi thay đổi so với chu kỳ trước -> Gọi ngay `telemetry_service.build_and_buffer()` và `uploader.upload()` để cập nhật Server tức thì.
3. **Cơ chế Night Mode**: Nếu tổng `P_ac` của toàn dự án = 0, đánh dấu dự án vào trạng thái "Night Mode" để tối ưu tài nguyên.

### Giai đoạn 2: Chu kỳ Snapshot (Mỗi 5 phút)
1. **`PollingService.save_to_database(project_id)`**:
    - Thu thập tất cả dữ liệu thành công từ bộ nhớ đệm (`self.buffer`).
    - Lưu các bản ghi snapshot vào DB local: `inverter_ac_realtime`, `mppt_realtime`, `string_realtime`, `project_realtime`.
2. **`TelemetryService.build_and_buffer(project_id)`**:
    - Gọi **`ProjectService.get_project_snapshot(project_id)`**: Hàm này sử dụng **Batch Loading (SQL Window Function)** để thu thập Snapshot mới nhất của toàn bộ AC, MPPT, String và Errors của một dự án chỉ qua vài câu query hiệu quả.
    - **`_build_payload()`**: Đóng gói thành cấu trúc JSON phân cấp sâu.
    - **`BufferService.save()`**: Lưu JSON payload vào bảng `uploader_outbox` trong `realtime.db`.

### Giai đoạn 3: Chu kỳ Tải lên (Độc lập hoặc Tuần tự)
1. **`UploaderService.upload()`**:
    - Lấy danh sách từ hàng đợi `uploader_outbox`.
    - Gửi `POST` lên Server Endpoint.
    - Nếu Server phản hồi 200 OK -> Xoá bản ghi trong hàng đợi (`delete_from_outbox`).

---

## 3. Cấu trúc Cơ sở dữ liệu liên quan (RealtimeDB)
- `latest_realtime`: Lưu 1 bản ghi duy nhất/1 inverter (Upsert mỗi 10s).
- `project_realtime` & `inverter_ac_realtime`: Lưu lịch sử snapshot (Mỗi 5 phút).
- `uploader_outbox`: Hàng đợi dữ liệu JSON chờ Cloud sync.
- `inverter_errors`: Lưu vết các lỗi quan trọng.

---

## 4. Tham số Cấu hình chính (`config.py`)
- `POLL_INTERVAL = 10`
- `SNAPSHOT_INTERVAL = 300`
- `API_BASE_URL = "..."`
