# Written by: Christopher Gholmieh
# Imports:

# GPIO:
import RPi.GPIO as GPIO

# Loguru:
from loguru import logger

# Typing:
from typing import List

# CTypes:
import ctypes


# Writer:
class Writer:
    """
    * Writes specific binary values to eight GPIO pins in specific order.
        * GPIO 14: 1
        * GPIO 15: 2
        * GPIO 18: 4
        * GPIO 23: 8
        * GPIO 24: 16
        * GPIO 25: 32
        * GPIO 08: 64
        * GPIO 07: 128

    * Has functionality to write a value to designated STOP pin.
        * GPIO 12: STOP
    """

    # Initialization:
    def __init__(self, debug: bool = False) -> None:
        # Debug:
        self.debug: bool = debug

        # GPIO:
        GPIO.setmode(GPIO.BCM)

        # Pins:
        self.pins: List[int] = [14, 15, 18, 23, 24, 25, 8, 7]
        self.stop: int = 12

        # Library:
        self.library: ctypes.CDLL = ctypes.CDLL("./one-step-writer/one-step-writer.so")

        self.library.initialize_optimizations.restype = None
        self.library.initialize_optimizations.argtypes = []

        self.library.initialize_pins.restype = None
        self.library.initialize_pins.argtypes = []

        self.library.number_to_binary.restype = ctypes.c_char_p
        self.library.number_to_binary.argtypes = [ctypes.c_ubyte]

        self.library.write_pulse_modulation.restype = None
        self.library.write_pulse_modulation.argtypes = [ctypes.c_int]

        self.library.write_stop_pin.restype = None
        self.library.write_stop_pin.argtypes = []

        # Logic:
        self.library.initialize_optimizations()
        self.library.initialize_pins()

        if self.debug:
            logger.info("[*] Initialized GPIO output pins.")

    # Methods:
    def write_pulse_modulation(self, value: int) -> None:
        self.library.write_pulse_modulation(value)

        logger.info(f"[*] Wrote {value} to GPIO pins.")

    def write_stop_pin(self) -> None:
        self.library.write_stop_pin()
