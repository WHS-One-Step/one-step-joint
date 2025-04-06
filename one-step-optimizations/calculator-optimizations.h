// Written by: Christopher Gholmieh
// Header Guards:
#ifndef __CALCULATOR_OPTIMIZATIONS_H__
#define __CALCULATOR_OPTIMIZATIONS_H__

// Definitions:
float calculate_dot_product(const float* vector_one, const float* vector_two);
float clamp(float minimum, float value, float maximum);

int calculate_pulse_modulation(float angle);

float calculate_flexion_angle(const float* thigh_orientation, const float* shank_orientation, const float calibration_offset);
float calibrate_flexion(const float* thigh_orientation, const float* shank_orientation);

void multiply_quaternions(const float* quaternion_one, const float* quaternion_two, float* result); 
void normalize_quaternion(float* quaternion);
void invert_quaternion(const float* quaternion, float* result);

float calculate_angle_between_quaternions(const float* quaternion_one, const float* quaternion_two);
float calculate_quaternion_flexion_angle(const float* thigh_quaternion, const float* shank_quaternion, const float calibration_offset);
float calibrate_quaternion_flexion(const float* thigh_quaternion, const float* shank_quaternion);

// Header Guard:
#endif // __CALCULATOR_OPTIMIZATIONS_H__
