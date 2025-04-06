// Written by: Christopher Gholmieh
// Headers:

// Math:
#include <math.h>

// Methods:
/**
    @brief Performs a dot product operation on two vectors.

    @param vector_one A vector.
    @param vector_two A vector.
*/
float calculate_dot_product(const float* vector_one, const float* vector_two) {
    return (
        (vector_one[0] * vector_two[0]) +
        (vector_one[1] * vector_two[1]) +
        (vector_one[2] * vector_two[2])
    );
}

/**
    @brief Clamps a value between a minimum and a maxium.

    @param minimum The minimum bound value.
    @param value The value to be clamped.
    @param maximum The maximum bound value.
*/
float clamp(float minimum, float value, float maximum) {
    if (minimum > value) {
        return minimum;
    }

    if (maximum < value) {
        return maximum;
    }

    return value;
}

/**
    @brief Maps an angle in degrees to an appropriate pulse modulation.

    @param angle The angle in degrees to be mapped to a pulse modulation.
*/
int calculate_pulse_modulation(float angle) {
    return (int) clamp(31.0f, (31.0f + ((angle * (255.0f - 31.0f)) / 180.0f)), 255.0f);
}

/**
    @brief Calculates the flexion angle using two gyroscopic vectors.

    @param thigh_orientation The thigh gyroscopic vector.
    @param shank_orientation The shank gyroscopic vector.
    @param calibration_offset The initial calibration offset that will be taken into account during calculations.
*/
float calculate_flexion_angle(const float* thigh_orientation, const float* shank_orientation, const float calibration_offset) {
    // Variables (Assignment):
    // Scalar:
    const float scalar = clamp(-1.0f, calculate_dot_product(thigh_orientation, shank_orientation), 1.0f);

    // Angle:
    const float angle = acosf(scalar) * (180.0f / M_PI);

    // Logic:
    return clamp(0.0f, angle + calibration_offset, 180.0f);
}

/**
    @brief Performs the quaternion multiplication operation on two quaternions.

    @param quaternion_one The first quaternion.
    @param quaternion_two The second quaternion.
    @param result The result quaternion where calculations will be applied to.
*/
void multiply_quaternions(const float* quaternion_one, const float* quaternion_two, float* result) {
    // Calculations:
    // W:
    result[0] = quaternion_one[0] * quaternion_two[0] - quaternion_one[1] * quaternion_two[1] - quaternion_one[2] * quaternion_two[2] - quaternion_one[3] * quaternion_two[3];

    // X:
    result[1] = quaternion_one[0] * quaternion_two[1] + quaternion_one[1] * quaternion_two[0] + quaternion_one[2] * quaternion_two[3] - quaternion_one[3] * quaternion_two[2];

    // Y:
    result[2] = quaternion_one[0] * quaternion_two[2] - quaternion_one[1] * quaternion_two[3] + quaternion_one[2] * quaternion_two[0] + quaternion_one[3] * quaternion_two[1];

    // Z:
    result[3] = quaternion_one[0] * quaternion_two[3] + quaternion_one[1] * quaternion_two[2] - quaternion_one[2] * quaternion_two[1] + quaternion_one[3] * quaternion_two[0];
}

/**
    @brief Normalizes a quaternion, effectively dividing each component by its magnitude.

    @param quaternion The quaternion to be normalized and modified in place.
*/
void normalize_quaternion(float* quaternion) {
    // Variables (Assignment):
    // Magnitude:
    const float magnitude = sqrtf(quaternion[0] * quaternion[0] + quaternion[1] * quaternion[1] + quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]);

    // Logic:
    if (magnitude > 1e-6) {
        // Calculations:
        // W:
        quaternion[0] /= magnitude;

        // X:
        quaternion[1] /= magnitude;

        // Y:
        quaternion[2] /= magnitude;

        // Z:
        quaternion[3] /= magnitude;
    }
}

/**
    @brief Inverts the signs of a quaternion's components.

    @param quaternion The quaternion to perform operations on.
    @param result The resulting quaternion that will be modified in place.
*/
void invert_quaternion(const float* quaternion, float* result) {
    // Calculations:
    // W:
    result[0] = quaternion[0];

    // X:
    result[1] = -quaternion[1];

    // Y:
    result[2] = -quaternion[2];

    // Z:
    result[3] = -quaternion[3];
}

/**
    @brief Calculates the angle between two quaternions.
    
    @param quaternion_one The first quaternion.
    @param quaternion_two The second quaternion.
*/
float calculate_angle_between_quaternions(const float* quaternion_one, const float* quaternion_two) {
    // Variables (Assignment):
    // Scalar:
    float scalar = clamp(-1.0f, quaternion_one[0] * quaternion_two[0] + quaternion_one[1] * quaternion_two[1] + quaternion_one[2] * quaternion_two[2] + quaternion_one[3] * quaternion_two[3], 1.0f);

    // Logic:
    return acosf(scalar) * (180.0f / M_PI);
}

/**
    @brief Calculates the knee flexion angle using the thigh quaternion, shank quaternion, and the initial calibration offset.

    @param thigh_quaternion The quaternion pertaining to the thigh.
    @param shank_quaternion The quaternion pertaining to the shank.
    @param calibration_offset The initial calibration offset used in calculations.
*/
float calculate_quaternion_flexion_angle(const float* thigh_quaternion, const float* shank_quaternion, const float calibration_offset) {
    // Variables (Assignment):
    // Rotation:
    float relative_rotation[4];

    // Inverse:
    float inverse_thigh[4];

    // Operations:
    invert_quaternion(thigh_quaternion, inverse_thigh);
    multiply_quaternions(inverse_thigh, shank_quaternion, relative_rotation);

    // Logic:
    return clamp(0.0f, 2.0f * acosf(relative_rotation[0]) * (180.0f / M_PI) + calibration_offset, 180.0f);
}

/** 
    @brief Calculates the initial flexion offset using the thigh quaternion and shank quaternion.

    @param thigh_quaternion The quaternion pertaining to the thigh.
    @param shank_quaternion The quaternion pertaining to the shank.
*/
float calibrate_quaternion_flexion(const float* thigh_quaternion, const float* shank_quaternion) {
    // Variables (Assignment):
    // Rotation:
    float relative_rotation[4];

    // Inverse:
    float inverse_thigh[4];

    // Operations:
    invert_quaternion(thigh_quaternion, inverse_thigh);
    multiply_quaternions(inverse_thigh, shank_quaternion, relative_rotation);

    // Logic:
    return 2.0f * acosf(relative_rotation[0]) * (180.0f / M_PI);
}

/**
    @brief Calculates the initial flexion offset using the thigh gyroscopical vector and the shank gyroscopical vector.

    @param thigh_orientation The thigh gyroscopical vector.
    @param shank_orientation The shank gyroscopical vector.
*/
float calibrate_flexion(const float* thigh_orientation, const float* shank_orientation) {
    // Variables (Assignment):
    // Scalar:
    const float scalar = clamp(-1.0f, calculate_dot_product(thigh_orientation, shank_orientation), 1.0f);

    // Logic:
    return acosf(scalar) * (180.0f / M_PI);
}
