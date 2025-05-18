from package import MPU6050
from package import SSD1306
from time import sleep

mpu = MPU6050()#Initiallize MPU6050
oled = SSD1306()#Initiallize SSD1306
oled.clear()#clear regsister
ACCEL_THRESHOLD = 0.2  # Sensitivity for tilt (in g)
print("Running")
try:
    while True:
        oled.clear()
        accel = mpu.get_accel_data()
        ax = accel['x']
        ay = accel['y']

        if ay > ACCEL_THRESHOLD:
            direction = "Left"
        elif ay < -ACCEL_THRESHOLD:
            direction = "Right"
        elif ax > ACCEL_THRESHOLD:               
            direction = "Forward"                
        elif ax < -ACCEL_THRESHOLD:
            direction = "Backward"
        else:
            direction = "Stable"
        
        oled.draw_text(0, 0, "Direction:")
        oled.draw_text(60, 0,direction)
        oled.display()
        sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")
