# Written by: Christopher Gholmieh
# Imports:

# GPIO:
import RPi.GPIO as GPIO

# Loguru:
from loguru import logger

# Typing:
from typing import List


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

        # Logic:
        self.initialize_pins()

    # Methods:
    def initialize_pins(self) -> None:
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        GPIO.setup(self.stop, GPIO.OUT)

        if self.debug:
            logger.info("[*] Initialized GPIO output pins.")

    def write(self, value: int) -> None:
        # Logic:
        self.clear()

        # Variables (Assignment):
        # Binary:
        binary: str = format(value, "08b")

        # Logic:
        GPIO.output(self.stop, GPIO.LOW)

        for iteration, bit in enumerate(binary[::-1]):
            GPIO.output(self.pins[iteration], GPIO.HIGH if bit == "1" else GPIO.LOW)

        logger.info(f"[*] Wrote {value} to GPIO pins.")

    def clear(self) -> None:
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def write_stop(self) -> None:
        self.clear()

        GPIO.output(self.stop, GPIO.HIGH)

