# Written by: Christopher Gholmieh
# Imports:

# Components:
from components import Calculator, Learner, Writer

# Typing:
from typing import Optional

# Loguru:
from loguru import logger

# Time:
from time import sleep


# Joint:
class Joint:
    # Constants:
    INTERVAL_DELAY: float = 0.50

    # Initialization:
    def __init__(self) -> None:
        # Calculator:
        self.calculator: Calculator = Calculator(use_quaternions=False, debug=True)

        # Learner:
        self.learner: Learner = Learner(learner_path="./learners/one-step-learner.pkl")
        self.learner.load()

        # Writer:
        self.writer: Writer = Writer(debug=True)

    # Methods:
    def loop(self) -> None:
        try:
            logger.warning("[*] Press CTRL + C to halt code execution.")

            while True:
                # Interval:
                sleep(self.INTERVAL_DELAY)

                # Logic:
                if len(self.calculator.shank_acceleration_readings) == 3 and len(self.calculator.shank_gyroscope_readings) == 3:
                    # Variables (Assignment):
                    # Prediction:
                    prediction: str = self.learner.predict([
                        acceleration_vector + gyroscope_vector for acceleration_vector, gyroscope_vector in zip(
                            self.calculator.shank_acceleration_readings.stack, self.calculator.shank_gyroscope_readings.stack
                        )
                    ])

                    # Flexion:
                    flexion: Optional[float] = self.calculator.calculate()

                    # Modulation:
                    modulation: int = self.calculator.calculate_pulse_modulation(flexion)

                    # Logic:
                    logger.info(f"[*] Prediction: {prediction}")
                    logger.info(f"[*] Flexion: {flexion}")
                    logger.info(f"[*] Modulation: {modulation}")

                    if prediction == "standing still":
                        self.writer.write_stop_pin()
                    else:
                        self.writer.write_pulse_modulation(modulation)

        except KeyboardInterrupt:
            self.calculator.terminate()
            self.writer.write_pulse_modulation(0)

            logger.info("[*] Execution halted by user.")

    def actuate(self) -> None:
        # Initialization:
        self.calculator.actuate()

        # Logic:
        self.loop()


# Main:
joint: Joint = Joint()
joint.actuate()
