from je_auto_control.linux_with_x11.core.display import display
from Xlib.ext.xtest import fake_input
from Xlib import X

from je_auto_control.linux_with_x11.core.x11_vk import key_num1


def press_key(keycode):
    fake_input(display, X.KeyPress, keycode)


def release_key(keycode):
    fake_input(display, X.KeyRelease, keycode)


