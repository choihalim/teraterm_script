from dotenv import load_dotenv
import os
import re
import serial.tools.list_ports
import subprocess

load_dotenv()

# constants
BAUDRATE = 115200
# edit path to match your Tera Term installation
TERA_TERM_PATH = os.getenv("TERA_TERM_PATH")
print(TERA_TERM_PATH)

# fetch and return a list of available USB serial ports
def get_serial_ports():
    serial_ports = []
    for port_info in sorted(serial.tools.list_ports.comports()):
        if port_info.description[:15] == "USB Serial Port":
            serial_ports.append(port_info.device)
    return serial_ports

# check if COM port is a UART port with data output
def is_uart_port(port):
    try:
        ser = serial.Serial(port, baudrate=BAUDRATE, timeout=1)
        data = ser.readline()  # Read one line of data
        ser.close()

        if data:  # If data is returned, it's a UART outputting logs
            print(f'{port} is a valid port actively outputting data')
            return True
        else:
            print(f'{port} is a valid port, but not outputting data')
            return False

    except serial.SerialException:
        print(f'{port} is not a valid port.')
        return False

# removes non-digit characters such as 'COM' converts the string to an integer
def parse_num(s):
    s_digits = re.sub(r'\D', '', s)
    return int(s_digits) if s_digits else None

# traverse the potential ports and check if they are actively outputting UART data
def find_uart_port():
    serial_ports = get_serial_ports()

    for port in serial_ports:
        if is_uart_port(port):
            return port

    return None

# launches Tera Term with the specified UART port
def launch_teraterm(uart_port):
    if uart_port is not None:
        comport = parse_num(uart_port)
        print(f"Attempting to open Tera Term with port {uart_port}...")
        process = subprocess.Popen(
            f'{TERA_TERM_PATH} /C={comport} /BAUD={BAUDRATE}', stdout=subprocess.PIPE, text=True
        )
    else:
        print("No active UART ports found. Tera Term not launched.")

# main function to find UART port and launch Tera Term
def run():
    uart_port = find_uart_port()
    launch_teraterm(uart_port)

if __name__ == "__main__":
    run()
