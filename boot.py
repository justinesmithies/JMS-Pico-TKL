import supervisor
import board
import digitalio
import storage
import usb_cdc
import usb_midi
import usb_hid
from time import sleep
import busio
import microcontroller

supervisor.set_next_stack_limit(4096 + 4096)

# I have an 18 x 6 matrix with diodes so to read a keypress
# for setting maintenance mode I use the following.

# Set GP15 on the column to high
column = digitalio.DigitalInOut(board.GP15)
column.direction = digitalio.Direction.OUTPUT
column.value = True

# Set pull down resisitor to low and read switch on GP28
row = digitalio.DigitalInOut(board.GP28)
row.direction = digitalio.Direction.INPUT
row.pull = digitalio.Pull.DOWN
sleep(0.1)


REFERENCE_BOOT_KEYBOARD_DESCRIPTOR = bytes((
    0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
    0x09, 0x06,        # Usage (Keyboard)
    0xA1, 0x01,        # Collection (Application)
    0x75, 0x01,        # Report Size (1)
    0x95, 0x08,        # Report Count (8)
    0x05, 0x07,        # Usage Page (Kbrd/Keypad)
    0x19, 0xE0,        # Usage Minimum (0xE0, 224)
    0x29, 0xE7,        # Usage Maximum (0xE7, 231)
    0x15, 0x00,        # Logical Minimum (0)
    0x25, 0x01,        # Logical Maximum (1)
    0x81, 0x02,        # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x01,        # Report Count (1)
    0x75, 0x08,        # Report Size (8)
    0x81, 0x03,        # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x03,        # Report Count (3)
    0x75, 0x01,        # Report Size (1)
    0x05, 0x08,        # Usage Page (LEDs)
    0x19, 0x01,        # Usage Minimum (Num Lock)
    0x29, 0x05,        # Usage Maximum (Kana)
    0x91, 0x02,        # Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    0x95, 0x01,        # Report Count (1)
    0x75, 0x05,        # Report Size (5)
    0x91, 0x01,        # Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    0x95, 0x06,        # Report Count (6)
    0x75, 0x08,        # Report Size (8)
    0x15, 0x00,        # Logical Minimum (0)
    0x26, 0xFF, 0x00,  # Logical Maximum (104)
    0x05, 0x07,        # Usage Page (Kbrd/Keypad)
    0x19, 0x00,        # Usage Minimum (0)
    0x2A, 0xFF, 0x00,  # Usage Maximum (104)
    0x81, 0x00,        # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,
))

reference_keyboard = usb_hid.Device(
    report_descriptor=REFERENCE_BOOT_KEYBOARD_DESCRIPTOR,
    usage=0x06,
    usage_page=0x01,
    report_ids=(0,),
    in_report_lengths=(8,),
    out_report_lengths=(1,),
    )

maintenance_mode = row.value
if not maintenance_mode:
    microcontroller.nvm[0] = 0
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    # usb_hid.enable((reference_keyboard,), boot_device=1)
    usb_hid.enable(boot_device=1)
else:
    microcontroller.nvm[0] = 1

row.deinit()
column.deinit()
