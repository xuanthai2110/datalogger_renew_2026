from backend.drivers.smartloggerHuawei import SmartLoggerHuawei

smart = SmartLoggerHuawei(transport, slave_id=0)

# đọc trạng thái
status = smart.control_status()
print(status)

# điều khiển công suất
smart.control_P(100)
print("Đã điều khiển công suất")