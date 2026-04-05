from communication.modbus_tcp import ModbusTCP
import time

IP = "192.168.1.8"
PORT = 502
SLAVE_ID = 1   # inverter thường = 1


# =========================
# WRITE HELPERS
# =========================
def write_u16(transport, addr, value):
    return transport.write_register(addr, int(value) & 0xFFFF, slave=SLAVE_ID)


def write_u32(transport, addr, value):
    high = (int(value) >> 16) & 0xFFFF
    low = int(value) & 0xFFFF
    return transport.write_multiple_registers(addr, [high, low], slave=SLAVE_ID)


# =========================
# TEST FUNCTIONS
# =========================

def set_power_percent(transport, percent):
    """
    40125 - Active power %
    scale = 0.1%
    """
    value = int(percent * 10)
    print(f"Set P = {percent}%")
    for i in range(5):
        write_u16(transport, 40125, value)
        print(f"  send {i+1}/5")
        time.sleep(1)


def set_power_kw(transport, kw):
    """
    40120 - Active power kW
    scale = 0.1 kW
    """
    value = int(kw * 10)
    print(f"Set P = {kw} kW")
    for i in range(5):
        write_u16(transport, 40120, value)
        print(f"  send {i+1}/5")
        time.sleep(1)


def set_power_w(transport, watt):
    """
    40126 - Active power W (U32)
    """
    print(f"Set P = {watt} W")
    for i in range(5):
        write_u32(transport, 40126, watt)
        print(f"  send {i+1}/5")
        time.sleep(1)


def set_cosphi(transport, cosphi):
    """
    40122 - cosφ
    scale = 0.001
    """
    value = int(cosphi * 1000)
    print(f"Set cosφ = {cosphi}")
    for i in range(3):
        write_u16(transport, 40122, value)
        print(f"  send {i+1}/3")
        time.sleep(1)


def disable_control(transport):
    """
    Tắt control → set 100%
    """
    print("Disable control (100%)")
    set_power_percent(transport, 100)


# =========================
# MAIN TEST
# =========================

def main():

    transport = ModbusTCP(IP, PORT)

    if not transport.connect():
        print("❌ Không connect được inverter")
        return

    try:
        print("\n=== TEST INVERTER CONTROL ===\n")

        # =========================
        # TEST 1: giảm công suất
        # =========================
        set_power_percent(transport, 50)

        # =========================
        # TEST 2: set theo kW
        # =========================
        set_power_kw(transport, 50)

        # =========================
        # TEST 3: set theo W
        # =========================
        set_power_w(transport, 50000)

        # =========================
        # TEST 4: set cosφ
        # =========================
        set_cosphi(transport, 0.95)

        # =========================
        # TEST 5: disable control
        # =========================
        disable_control(transport)

        print("\n✅ Done test")

    except Exception as e:
        print("❌ ERROR:", e)

    finally:
        transport.close()
        print("Disconnected")


if __name__ == "__main__":
    main()