from smbus2 import SMBus

# Register definitions
SET_CONTRAST = 0x81
SET_ENTIRE_ON = 0xA4
SET_NORM_INV = 0xA6
SET_DISP = 0xAE
SET_MEM_ADDR = 0x20
SET_COL_ADDR = 0x21
SET_PAGE_ADDR = 0x22
SET_DISP_START_LINE = 0x40
SET_SEG_REMAP = 0xA0
SET_MUX_RATIO = 0xA8
SET_IREF_SELECT = 0xAD
SET_COM_OUT_DIR = 0xC0
SET_DISP_OFFSET = 0xD3
SET_COM_PIN_CFG = 0xDA
SET_DISP_CLK_DIV = 0xD5
SET_PRECHARGE = 0xD9
SET_VCOM_DESEL = 0xDB
SET_CHARGE_PUMP = 0x8D

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.width * self.height // 8)
        self.init_display()

    def init_display(self):
        for cmd in [
            SET_DISP, SET_MEM_ADDR, 0x00, SET_DISP_START_LINE, SET_SEG_REMAP | 0x01, SET_MUX_RATIO,
            self.height - 1, SET_COM_OUT_DIR | 0x08, SET_DISP_OFFSET, 0x00, SET_COM_PIN_CFG, 0x12,
            SET_DISP_CLK_DIV, 0x80, SET_PRECHARGE, 0xF1, SET_VCOM_DESEL, 0x30, SET_CONTRAST, 0xFF,
            SET_ENTIRE_ON, SET_NORM_INV, SET_IREF_SELECT, 0x30, SET_CHARGE_PUMP, 0x14, SET_DISP | 0x01]:
            self.write_cmd(cmd)

    def write_cmd(self, cmd):
        self.i2c.write_byte_data(self.addr, 0x00, cmd)

    def fill(self, color):
        self.buffer = bytearray(self.width * self.height // 8)

    def text(self, text, x, y):
        # Basic text rendering (to be extended)
        pass

    def show(self):
        self.i2c.write_i2c_block_data(self.addr, 0x40, self.buffer)
