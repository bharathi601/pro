from machine import Pin, I2C, PWM
from imu import MPU6050
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread

# Constants
WIDTH = 128
HEIGHT = 64
TCA_ADDR = 0x70
THRESHOLD = 0.2

# Initialize I2C on Raspberry Pi Zero 2 W (using I2C1)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=500000)  # Use GPIO2 and GPIO3 for SDA and SCL

# TCA9548A helper functions
def tca_select_channel(channel):
    if 0 <= channel <= 7:
        i2c.writeto(TCA_ADDR, bytes([1 << channel]))

def tca_disable_all():
    i2c.writeto(TCA_ADDR, b'\x00')

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
    raise SystemExit

# Initialize PWM for servo
servo = PWM(Pin(15))  # GPIO15 (pin 22)
servo.freq(50)  # 50 Hz for standard servos

def set_angle(angle):
    min_duty = 1638  # ~1ms (0°)
    max_duty = 8192  # ~2ms (180°)
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    
def second_core():
    while True:
        for angle in range(0, 181, 1):   # Smaller step = smoother
            set_angle(angle)
            sleep(0.015)  # Faster but smooth delay
        for angle in range(180, -1, -1):
            set_angle(angle)
            sleep(0.015)

_thread.start_new_thread(second_core, ())

# Main loop
while True:
        # Read MPU6050
        tca_select_channel(0)
        sleep(0.005)
        ax = round(imu.accel.x, 3)
        ay = round(imu.accel.y, 3)
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
        oled.text(direction, 81, 0)
        oled.show()
        tca_disable_all()
            # Fail silently if OLED write fails
        print(direction)
        sleep(0.1)
