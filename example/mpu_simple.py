# main.py
from package import MPU6050
import time

mpu = MPU6050()
print("Reading accelerometer and gyroscope data...\n")

try:
    while True:
        accel = mpu.get_accel_data()
        gyro = mpu.get_gyro_data()

        print(f"Accelerometer: X={accel['x']:.2f}g  Y={accel['y']:.2f}g  Z={accel['z']:.2f}g")
        print(f"Gyroscope:     X={gyro['x']:.2f}°/s  Y={gyro['y']:.2f}°/s  Z={gyro['z']:.2f}°/s")
        print("-------------------------------")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
