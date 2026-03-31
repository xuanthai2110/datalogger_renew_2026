import sqlite3

try:
    conn = sqlite3.connect('backend/db_manager/data/metadata.db')
    conn.row_factory = sqlite3.Row
    
    # 1. Check Projects
    print("\n=== PROJECTS ===")
    projects = conn.execute("SELECT * FROM projects").fetchall()
    print(f"Total projects: {len(projects)}")
    for p in projects:
        d = dict(p)
        print(f"  - ID: {d.get('id')} | Name: {d.get('name')} | Server ID: {d.get('server_id')} | Capacity: {d.get('capacity_kwp')} kWp")

    # 2. Check Inverters
    print("\n=== INVERTERS ===")
    inverters = conn.execute("SELECT * FROM inverters").fetchall()
    print(f"Total inverters: {len(inverters)}")
    for i, inv in enumerate(inverters):
        if i >= 5: 
            print("  ... (hiển thị 5 inverter đầu tiên)")
            break
        d = dict(inv)
        print(f"  - ID: {d.get('id')} | Proj ID: {d.get('project_id')} | SN: {d.get('serial_number')} | Model: {d.get('model')} | Server ID: {d.get('server_id')}")

    # 3. Check Comm Config
    print("\n=== COMM CONFIG ===")
    comms = conn.execute("SELECT * FROM comm_config").fetchall()
    print(f"Total comm configs: {len(comms)}")
    for c in comms:
        d = dict(c)
        print(f"  - Comm: {d.get('comm_type')} | Host/Port: {d.get('host')}:{d.get('port')} (or {d.get('com_port')}) | Baudrate: {d.get('baudrate')}")
        
except Exception as e:
    print(f"Error reading MetadataDB: {e}")
