from machine import Pin, I2C
import time

# I2C setup
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)  # Adjust pins if needed
AS5600_I2C_ADDRESS = 0x36

# Register addresses
RAW_ANGLE_HIGH_REGISTER = 0x0C
RAW_ANGLE_LOW_REGISTER = 0x0D

# Function to read data from the AS5600
def read_angle():
    try:
        # Read high and low bytes from the respective registers
        high_byte = i2c.readfrom_mem(AS5600_I2C_ADDRESS, RAW_ANGLE_HIGH_REGISTER, 1)[0]
        low_byte = i2c.readfrom_mem(AS5600_I2C_ADDRESS, RAW_ANGLE_LOW_REGISTER, 1)[0]

        # Combine the high and low bytes to form the raw angle value (bits 11:8 and 7:0)
        angle = ((high_byte & 0x0F) << 8) | low_byte

        # Convert raw angle to degrees (0 to 360)
        angle_in_degrees = (angle / 4096) * 360

        return int(angle_in_degrees)  # Ensure the angle is an integer
    except Exception as e:
        print("Error reading angle:", e)
        return None

# Main loop
while True:
    angle = read_angle()
    if angle is not None:
        print("Raw Angle: {} degrees".format(angle))
    time.sleep(0.1)

