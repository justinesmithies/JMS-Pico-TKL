# JMS TKL - Raspberry Pi PICO keyboard
#
import board
import pwmio
import time
import supervisor
import busio
from time import sleep
import microcontroller
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

from kmk.kmk_keyboard import KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.keys import KC, make_key, make_consumer_key
import digitalio
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.international import International

supervisor.set_next_stack_limit(4096 + 4096)

# Run the LED
led = pwmio.PWMOut(board.GP25, frequency=1, duty_cycle=1024, variable_frequency=True)

# Create the I2C interface.
displayio.release_displays()

i2c = busio.I2C(board.GP1, board.GP0, frequency=800000)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Boot splash
splash = displayio.Group()
background = displayio.Group()
splash_text = displayio.Group()
main = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
background.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(126, 62, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
background.append(inner_sprite)

splash.append(background)

# Draw a label
text = "JMS Pico TKL"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=25, y=8)
splash_text.append(text_area)

text = "Powered by"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=30, y=18)
splash_text.append(text_area)

text = "CircuitPython"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=23, y=28)
splash_text.append(text_area)

text = "and"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=50, y=38)
splash_text.append(text_area)

text = "KMK"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=50, y=48)
splash_text.append(text_area)

splash.append(splash_text)

sleep(2)

# Main screen

splash.remove(splash_text)

text = "Caps lock:"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=8, y=8)
main.append(text_area)

text = "Scroll lock:"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=8, y=18)
main.append(text_area)

text = "Layer:"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=8, y=40)
main.append(text_area)

if microcontroller.nvm[0] == 1:
    text = "Maintenance mode"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=8, y=50)
    main.append(text_area)

caps_text_on = label.Label(terminalio.FONT, text="On", color=0xFFFFFF, x=70, y=8)
caps_text_off = label.Label(terminalio.FONT, text="Off", color=0xFFFFFF, x=70, y=8)
scroll_text_on = label.Label(terminalio.FONT, text="On", color=0xFFFFFF, x=82, y=18)
scroll_text_off = label.Label(terminalio.FONT, text="Off", color=0xFFFFFF, x=82, y=18)

layer_0 = label.Label(terminalio.FONT, text="0", color=0xFFFFFF, x=45, y=40)
layer_1 = label.Label(terminalio.FONT, text="1", color=0xFFFFFF, x=45, y=40)

splash.append(main)

class _LockStatus(LockStatus):
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        if self.get_caps_lock():
            main.append(caps_text_on)
            main.remove(caps_text_off)
        else:
            main.append(caps_text_off)
            main.remove(caps_text_on)
    def before_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        if self.get_scroll_lock():
            main.append(scroll_text_on)
            main.remove(scroll_text_off)
        else:
            main.append(scroll_text_off)
            main.remove(scroll_text_on)
    def after_matrix_scan(self, sandbox):
        super().after_matrix_scan(sandbox)
        if jmskb.active_layers[0] == 1:
            main.append(layer_1)
            main.remove(layer_0)
        else:
            main.append(layer_0)
            main.remove(layer_1)

jmskb = KMKKeyboard()

jmskb.extensions.append(_LockStatus())
jmskb.extensions.append(MediaKeys())
jmskb.extensions.append(International())

jmskb.modules.append(Layers())

LAYER1 = KC.LT(1, KC.APPLICATION)

jmskb.col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19)
jmskb.row_pins = (board.GP20, board.GP21, board.GP22, board.GP26, board.GP27, board.GP28)
jmskb.diode_orientation = DiodeOrientation.COLUMNS

rollover_cols_every_rows = 4
jmskb.debug_enabled = False

nokey = KC.NO
jmskb.keymap = [
    [
        # Layer 0
        KC.ESC, nokey, KC.F1, KC.F2, KC.F3, KC.F4, nokey, KC.F5, KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11, KC.F12, KC.PSCREEN, KC.SCROLLLOCK, KC.PAUSE,
        KC.GRAVE, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINUS, KC.EQUAL, nokey, KC.BSPC, KC.INS, KC.HOME, KC.PGUP,
        KC.TAB, nokey, KC.Q, KC.W, KC.E, KC.R, KC.T, KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC, KC.RBRC, KC.BSLS, KC.DEL, KC.END, KC.PGDN,
        KC.CAPS, nokey, KC.A, KC.S, KC.D, KC.F, KC.G, KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT, nokey, KC.ENT, nokey, nokey, nokey,
        KC.LSFT, KC.NONUS_BSLASH, KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH, nokey, KC.RSHIFT, nokey, nokey, KC.UP, nokey,
        KC.LCTL, KC.LGUI, nokey, KC.LALT, nokey, nokey, KC.SPC, nokey, nokey, nokey, KC.RALT, KC.RGUI, nokey, LAYER1, KC.RCTRL, KC.LEFT, KC.DOWN, KC.RIGHT,
    ],
    [
        # Layer 1
        KC.TRNS, nokey, KC.F13, KC.F14, KC.F15, KC.F16, nokey, KC.F17, KC.F18, KC.F19, KC.F20, KC.MPRV, KC.MSTP, KC.MPLY, KC.MNXT, KC.MUTE, KC.VOLD, KC.VOLU,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, nokey, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, nokey, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
        KC.TRNS, nokey, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, nokey, KC.TRNS, nokey, nokey, nokey,
        KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, nokey, KC.TRNS, nokey, nokey, KC.TRNS, nokey,
        KC.TRNS, KC.TRNS, nokey, KC.TRNS, nokey, nokey, KC.TRNS, nokey, nokey, nokey, KC.TRNS, KC.TRNS, nokey, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    ],
]

def usbfunc():

    if __name__ == '__main__':
        led.duty_cycle=16384
        led.frequency=144
        print("Started")
        jmskb.go()
        raise Exception('Something has caused an error.')

try:
    usbfunc()
except KeyboardInterrupt:
    led.duty_cycle = 0
    print("Keyboard Interrupt")
except Exception as e:
    print(e)
    led.duty_cycle=0
    supervisor.reload()


supervisor.reload()
