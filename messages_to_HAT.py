import serial
import struct
import time

def send_ascii_read_int32(port, ascii_text):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        ser.write(ascii_text.encode())
        data = ser.read(4)
        int_value = struct.unpack('i', data)[0]
        return int_value

def send_ascii_read_uint16(port, ascii_text):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        ser.write(ascii_text.encode())
        data = ser.read(2)
        uint_value = struct.unpack('H', data)[0]
        ascii_value = chr(uint_value)  # Convert uint16 to ASCII
        #return ascii_value
        return uint_value

def send_ascii_receive_decimal(port, ascii_text):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        ser.write(ascii_text.encode())
        received_data = ser.read(4)  # Adjust the number of bytes as needed
        decimal_value = int.from_bytes(received_data, byteorder='big')
        #print(f"Received binary data: {received_data}")
        print(f"{decimal_value}")

def send_ascii_receive_binary(port, ascii_text):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        ser.write(ascii_text.encode())
        time.sleep(1)
        received_data = ser.read(4)  # Adjust the number of bytes as needed
        print(f"Received binary data: {received_data}")

def send_hex_receive_decimal(port, hex_data):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        hex_bytes = bytes.fromhex(hex_data)
        ser.write(hex_bytes)
        received_data = ser.read(4)  # Adjust the number of bytes as needed
        decimal_value = int.from_bytes(received_data, byteorder='big')
        print(f"Received binary data: {received_data}")
        print(f"Decimal value: {decimal_value}")

# Example usage:
# Replace 'COM1' with your serial port name (e.g., 'COM3' for Windows).
port_name = 'COM5'

# Example sending 'hello' and reading int32
int_value = send_ascii_read_int32(port_name, ",T1'")
print(f"Received int32 value: {int_value}")

# Example sending 'world' and reading uint16
value = send_ascii_read_uint16(port_name, ",I1'")
print(f"Received uint16 value: {value}")

print(f"TEMP 1: ")
send_ascii_receive_decimal(port_name, ",T1'")
print(f"PROPORTIONAL PART: ")
send_ascii_receive_decimal(port_name, ",P1'")
print(f"INTEGRAL PART: ")
send_ascii_receive_decimal(port_name, ",I1'")
print(f"DERIVATIVE PART: ")
send_ascii_receive_decimal(port_name, ",D1'")
#send_ascii_receive_binary(port_name, ",b1' 5 CR")
#send_hex_receive_decimal(port_name, "69 31 00 3C 0D")
