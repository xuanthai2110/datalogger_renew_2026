from pymodbus.client import ModbusTcpClient
import argparse
import sys
import time


DEFAULT_IP = "192.168.1.8"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 9
DEFAULT_KW = 50.0
DEFAULT_RESET_PERCENT = 100.0
DEFAULT_DELAY_1 = 100.0
DEFAULT_DELAY_2 = 100.0


def read_power(client: ModbusTcpClient, slave_id: int, label: str):
    response = client.read_holding_registers(32080, 2, slave=slave_id)
    if response.isError():
        print(f"{label}: READ 32080-32081 FAILED: {response}")
        return None

    regs = response.registers
    value = (regs[0] << 16) + regs[1]
    if value > 0x7FFFFFFF:
        value -= 0x100000000

    print(f"{label}: READ 32080-32081 OK: regs={regs}, power_w={value}")
    return value


def write_40120_kw(client: ModbusTcpClient, slave_id: int, kw: float):
    value = int(round(kw * 10))
    print(f"WRITE 40120 -> kw={kw}, raw={value}, slave_id={slave_id}")
    response = client.write_register(40120, value, slave=slave_id)

    if response.isError():
        print(f"WRITE 40120 FAILED: {response}")
        return False

    print(f"WRITE 40120 OK: {response}")
    return True


def write_40125_percent(client: ModbusTcpClient, slave_id: int, percent: float):
    value = int(round(percent * 10))
    print(f"WRITE 40125 -> percent={percent}, raw={value}, slave_id={slave_id}")
    response = client.write_register(40125, value, slave=slave_id)

    if response.isError():
        print(f"WRITE 40125 FAILED: {response}")
        return False

    print(f"WRITE 40125 OK: {response}")
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test Huawei 50kW control, then observe power after 10s and 20s, then reset to 100%."
    )
    parser.add_argument("--host", default=DEFAULT_IP, help="Modbus TCP host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Modbus TCP port")
    parser.add_argument("--slave", type=int, default=DEFAULT_SLAVE_ID, help="Modbus slave ID")
    parser.add_argument("--kw", type=float, default=DEFAULT_KW, help="kW value to write to register 40120")
    parser.add_argument(
        "--reset-percent",
        type=float,
        default=DEFAULT_RESET_PERCENT,
        help="Percent value to write to register 40125 when resetting",
    )
    parser.add_argument(
        "--delay1",
        type=float,
        default=DEFAULT_DELAY_1,
        help="Seconds to wait before the first power readback",
    )
    parser.add_argument(
        "--delay2",
        type=float,
        default=DEFAULT_DELAY_2,
        help="Additional seconds to wait before the second power readback",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    client = ModbusTcpClient(args.host, port=args.port, timeout=3)

    print(
        f"CONNECT -> host={args.host}, port={args.port}, slave_id={args.slave}, "
        f"kw={args.kw}, reset_percent={args.reset_percent}, delay1={args.delay1}, delay2={args.delay2}"
    )
    if not client.connect():
        print("CONNECT FAILED")
        sys.exit(1)

    print("CONNECT OK")

    exit_code = 0
    try:
        read_power(client, args.slave, "BEFORE WRITE")

        ok_write = write_40120_kw(client, args.slave, args.kw)
        if not ok_write:
            exit_code = 2
        else:
            print(f"\nWAIT {args.delay1}s")
            time.sleep(args.delay1)
            read_power(client, args.slave, f"AFTER {args.delay1:.1f}s")

            print(f"\nWAIT {args.delay2}s")
            time.sleep(args.delay2)
            read_power(client, args.slave, f"AFTER {args.delay1 + args.delay2:.1f}s")
    finally:
        print("\nRESET TO 100%")
        ok_reset = write_40125_percent(client, args.slave, args.reset_percent)
        if not ok_reset and exit_code == 0:
            exit_code = 3

        client.close()
        print("\nDISCONNECTED")

    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
