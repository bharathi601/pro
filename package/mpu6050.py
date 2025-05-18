# mpu6050.py created by Bharathi
import smbus
import time

MPU6050_ADDR = 0x68

# Registers
PWR_MGMT_1 = 0x6B
INT_ENABLE = 0x38
FIFO_EN = 0x23
USER_CTRL = 0x6A
FIFO_COUNT = 0x72
FIFO_R_W = 0x74
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
TEMP_OUT_H = 0x41

class MPU6050:
    def __init__(self, bus=1, address=MPU6050_ADDR):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0)  # Wake up

        # Enable accelerometer and gyro in FIFO
        self.bus.write_byte_data(self.address, USER_CTRL, 0x40)  # Enable FIFO
        self.bus.write_byte_data(self.address, FIFO_EN, 0x78)    # Enable accel & gyro to FIFO

        # Enable interrupt (data ready)
        self.bus.write_byte_data(self.address, INT_ENABLE, 0x01)

    def read_raw_data(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg+1)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_accel_data(self):
        ax = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        ay = self.read_raw_data(ACCEL_XOUT_H+2) / 16384.0
        az = self.read_raw_data(ACCEL_XOUT_H+4) / 16384.0
        return {'x': ax, 'y': ay, 'z': az}

    def get_gyro_data(self):
        gx = self.read_raw_data(GYRO_XOUT_H) / 131.0
        gy = self.read_raw_data(GYRO_XOUT_H+2) / 131.0
        gz = self.read_raw_data(GYRO_XOUT_H+4) / 131.0
        return {'x': gx, 'y': gy, 'z': gz}

    def get_temperature(self):
        temp_raw = self.read_raw_data(TEMP_OUT_H)
        temp_c = temp_raw / 340.0 + 36.53
        return temp_c

    def read_fifo_count(self):
        high = self.bus.read_byte_data(self.address, FIFO_COUNT)
        low = self.bus.read_byte_data(self.address, FIFO_COUNT + 1)
        return (high << 8) | low

    def read_fifo_data(self, length=12):
        # Read accelerometer + gyro data (6 words = 12 bytes)
        data = []
        for _ in range(length):
            data.append(self.bus.read_byte_data(self.address, FIFO_R_W))
        return data

    def reset_fifo(self):
        self.bus.write_byte_data(self.address, USER_CTRL, 0x04)  # Reset FIFO
        time.sleep(0.05)
        self.bus.write_byte_data(self.address, USER_CTRL, 0x40)  # Re-enable FIFO

    def dmp_setup_placeholder(self):
        print("DMP support requires loading firmware via I2C – not implemented in this version.")
