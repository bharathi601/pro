import time

class MPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        self._init_device()

    def _init_device(self):
        # Wake up the MPU6050
        self.i2c.write_byte_data(self.address, 0x6B, 0)
        time.sleep(0.1)

    def get_accel_data(self):
        raw_data = self.i2c.read_i2c_block_data(self.address, 0x3B, 6)
        ax = self._convert_to_signed(raw_data[0], raw_data[1])
        ay = self._convert_to_signed(raw_data[2], raw_data[3])
        az = self._convert_to_signed(raw_data[4], raw_data[5])
        return {"x": ax, "y": ay, "z": az}

    def _convert_to_signed(self, high_byte, low_byte):
        value = (high_byte << 8) + low_byte
        if value >= 0x8000:
            value -= 0x10000
        return value / 16384.0
