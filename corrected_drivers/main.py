from smbus2 import SMBus
from time import sleep
from mpu6050 import MPU6050
from ssd1306 import SSD1306_I2C

# Constants
WIDTH = 128
HEIGHT = 64
TCA_ADDR = 0x70
THRESHOLD = 0.2

# Initialize I2C on Raspberry Pi (bus 1)
i2c = SMBus(1)

# TCA9548A helper functions
def tca_select_channel(channel):
    if 0 <= channel <= 7:
        i2c.write_byte(TCA_ADDR, 1 << channel)

def tca_disable_all():
    i2c.write_byte(TCA_ADDR, 0x00)

# Initialize MPU6050 and OLED
try:
    tca_select_channel(0)
    sleep(0.02)
    imu = MPU6050(i2c)
    tca_disable_all()

    tca_select_channel(1)
    sleep(0.02)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    tca_disable_all()

except Exception as e:
    print("Init Error:", e)
    exit(1)

# Main loop
while True:
    try:
        # Read MPU6050
        tca_select_channel(0)
        sleep(0.005)
        accel_data = imu.get_accel_data()
        ax = round(accel_data['x'], 3)
        ay = round(accel_data['y'], 3)
        tca_disable_all()

        # Detect direction
        direction = ""
        if ax > THRESHOLD:
            direction += "Right "
        elif ax < -THRESHOLD:
            direction += "Left "
        if ay > THRESHOLD:
            direction += "Front "
        elif ay < -THRESHOLD:
            direction += "Back "
        if not direction:
            direction = "Stable"

        # Update OLED
        tca_select_channel(1)
        oled.fill(0)
        oled.text("Direction:", 0, 0)
        oled.text(direction, 0, 16)
        oled.show()
        tca_disable_all()

        # Print direction
        print(direction)
        sleep(0.1)

    except Exception as e:
        print("Runtime Error:", e)
        sleep(0.5)
