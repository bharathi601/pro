from package import SSD1306
import time

oled = SSD1306()
oled.clear()
oled.draw_text(0, 0, "HELLO")
oled.draw_text(0, 10, "PI ZERO 2W")
oled.display()
time.sleep(5)
oled.clear()
oled.display()
