from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# Replace with your ROC107's IP address and port
client = ModbusTcpClient('192.168.207.59', port=502)

# Connect to the client
connection = client.connect()
if connection:
    try:
        # Define register addresses
        REGISTER_ADDRESSES = {
            "CPU Temp": 1,
            "Logic Voltage": 3,
            "Charge Voltage": 5,
            "Battery Voltage": 7
        }
        UNIT_ID = 1  # Modbus Slave ID
        REG_COUNT = 2  # Number of registers to read

        # Function to read and decode register values
        def read_register(address):
            result = client.read_input_registers(address, count=REG_COUNT, slave=UNIT_ID)
            if not result.isError():
                decoder = BinaryPayloadDecoder.fromRegisters(
                    result.registers, byteorder=Endian.BIG, wordorder=Endian.BIG
                )
                return decoder.decode_32bit_float()
            else:
                print(f"Error reading register {address}: {result}")
                return None

        # Read and print values
        for name, address in REGISTER_ADDRESSES.items():
            value = read_register(address)
            if value is not None:
                unit = "°F" if name == "CPU Temp" else "V"
                print(f"{name}: {value} {unit}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
else:
    print("Failed to connect to the ROC107.")