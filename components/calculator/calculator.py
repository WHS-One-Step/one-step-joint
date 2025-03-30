# Written by: Christopher Gholmieh
# Imports:

# Phidget:
from Phidget22.PhidgetException import PhidgetException
from Phidget22.Devices.Spatial import Spatial

# Loguru:
from loguru import logger

# Typing:
from typing import Optional, List, Any

# Scipy:
from scipy.spatial.transform import Rotation

# Numpy:
import numpy

# Math:
from math import degrees, acos

# Time:
from time import sleep


# Stack:
class Stack:
    """
    * Used to contain the past nth readings of the accelerometer or gyroscope.
        * Readings of the accelerometer or gyroscope can be used to predict current movement/gait state.
    """

    # Initialization:
    def __init__(self, limit: int) -> None:
        # Limit:
        self.limit: int = limit

        # Stack:
        self.stack: List[Any] = []

    # Methods:
    def append(self, value: Any) -> None:
        self.stack.append(value)

        if len(self.stack) > value:
            self.stack.pop(0)

    def __len__(self) -> int:
        return len(self.stack)


# Calculator:
class Calculator:
    """
    * Calculates PWM and the knee flexion angle using two IMUs.
        * NOTE: Please add type functionality for existing things such as rotations.

        * NOTE: When calibrating, keep knee fully extended.
    """

    # Initialization:
    def __init__(self, use_quaternions: bool = False, debug: bool = False) -> None:
        # Orientations:
        self.thigh_orientation: numpy.ndarray = numpy.array([0.0, 0.0, 1.0])
        self.shank_orientation: numpy.ndarray = numpy.array([0.0, 0.0, 1.0])

        # Quaternions:
        self.use_quaternions: bool = use_quaternions

        self.thigh_quaternion: numpy.ndarray = numpy.array([1.0, 0.0, 0.0, 0.0])
        self.shank_quaternion: numpy.ndarray = numpy.array([1.0, 0.0, 0.0, 0.0])

        # Actuated:
        self.actuated: bool = False

        # Offset:
        self.calibration_offset: float = 0.0

        # Debug:
        self.debug: bool = debug

        # IMUs:
        self.thigh_imu: Spatial = Spatial()
        self.shank_imu: Spatial = Spatial()

        # Serial:
        self.thigh_imu.setDeviceSerialNumber(721783)
        self.shank_imu.setDeviceSerialNumber(721888)

        # Stacks:
        self.thigh_acceleration_readings: Stack = Stack(limit=3)
        self.thigh_gyroscope_readings: Stack = Stack(limit=3)

        self.shank_acceleration_readings: Stack = Stack(limit=3)
        self.shank_gyroscope_readings: Stack = Stack(limit=3)

    # Methods:
    def calculate_pulse_modulation(angle: float) -> int:
        # Variables (Assignment):
        # Modulation:
        modulation: float = 31 + ((angle * (255 - 31)) / 180)

        # Logic:
        return int(modulation)

    def handle_thigh_imu(self, spatial: Spatial, acceleration: List[float], angular_rotation: List[float], magnetic_field: List[float], timestamp: float) -> None:
        if not self.actuated:
            logger.error("[*] Handler set when calculator not Actuated.")

            return

        self.thigh_gyroscope_readings.append(angular_rotation)
        self.thigh_acceleration_readings.append(acceleration)

        try:
            if self.use_quaternions:
                # Variables (Assignment):
                # Quaternion:
                quaternion = spatial.getQuaternion()

                # Logic:
                self.thigh_quaternion = numpy.array([quaternion.w, quaternion.x, quaternion.y, quaternion.z])
            else:
                self.thigh_orientation = numpy.array([acceleration[0], acceleration[1], acceleration[2]])

                self.thigh_orientation = self.thigh_orientation / numpy.linalg.norm(self.thigh_orientation)
        except PhidgetException as exception:
            logger.error(f"[!] Error: {exception}")

    def handle_shank_imu(self, spatial: Spatial, acceleration: List[float], angular_rotation: List[float], magnetic_field: List[float], timestamp: float) -> None:
        if not self.actuated:
            logger.error("[*] Handler set when calculator not Actuated.")

            return

        self.shank_gyroscope_readings.append(angular_rotation)
        self.shank_acceleration_readings.append(acceleration)

        try:
            if self.use_quaternions:
                # Variables (Assignment):
                # Quaternion:
                quaternion = spatial.getQuaternion()

                # Logic:
                self.shank_quaternion = numpy.array([quaternion.w, quaternion.x, quaternion.y, quaternion.z])
            else:
                self.shank_orientation = numpy.array([acceleration[0], acceleration[1], acceleration[2]])

                self.shank_orientation = self.shank_orientation / numpy.linalg.norm(self.shank_orientation)
        except PhidgetException as exception:
            logger.error(f"[!] Error: {exception}")

    def terminate(self) -> None:
        if not self.actuated:
            logger.error("[*] Attempted to terminate when calculator not Actuated.")

            return

        self.thigh_imu.close()
        self.shank_imu.close()

        logger.info("[*] IMUs disconnected.")

        self.actuated = False

    def calibrate(self) -> None:
        # Logic:
        if not self.actuated:
            logger.error("[*] Attempted to calibrate when calculator not Actuated.")

            return

        # Variables (Assignment):
        # Dot:
        dot_product = numpy.dot(self.thigh_orientation, self.shank_orientation)

        # Logic:
        self.calibration_offset = degrees(acos(self.clamp(-1.0, dot_product, 1.0)))

        logger.warning(f"[*] Calibrated angle: {self.calibration_offset}")

    def calculate(self) -> Optional[float]:
        if not self.actuated:
            logger.error("[*] Attempted to calculate when calculator not Actuated.")

            return

        try:
            if self.use_quaternions:
                # Variables (Assignment):
                # Rotations:
                rotation_thigh = Rotation.from_quat(self.thigh_quaternion)
                rotation_shank = Rotation.from_quat(self.shank_quaternion)

                # Rotation:
                relative_rotation = rotation_shank * rotation_thigh.inv()

                # Euler:
                euler_angles = relative_rotation.as_euler("xyz", degrees=True)

                # Flexion:
                flexion: float = self.clamp(0.0, euler_angles[2], 180.0)

                # Logic:
                if self.debug:
                    logger.info(f"[*] Flexion angle (Quaternion): {flexion}")

                return flexion
            else:
                # Variables (Assignment):
                # Dot:
                dot_product = numpy.dot(self.thigh_orientation, self.shank_orientation)

                # Offset:
                flexion: float = degrees(acos(self.clamp(-1.0, dot_product, 1.0))) + self.calibration_offset

                flexion: float = self.clamp(0.0, flexion, 180.0)

                # Logic:
                if self.debug:
                    logger.info(f"[*] Flexion angle (Acceleration): {flexion}")

        except Exception as exception:
            logger.error(f"[!] Error: {exception}")

    def clamp(self, minimum: float, value: float, maximum: float) -> float:
        if minimum > value:
            return minimum

        if value > maximum:
            return maximum

        return value

    def actuate(self) -> None:
        self.actuated = True

        try:
            # Initialization:
            self.thigh_imu.openWaitForAttachment(5000)
            self.shank_imu.openWaitForAttachment(5000)

            # Logic:
            logger.info("[*} IMUs connected.")

            self.thigh_imu.setOnSpatialDataHandler(self.handle_thigh_imu)
            self.shank_imu.setOnSpatialDataHandler(self.handle_shank_imu)

            if not self.use_quaternions:
                logger.info("[*] Waiting 2.0 seconds for proper calibration. Please keep knee fully extended during this time.")

                sleep(2.0)

                self.calibrate()

        except PhidgetException as exception:
            logger.error(f"[!] Error: {exception}")
