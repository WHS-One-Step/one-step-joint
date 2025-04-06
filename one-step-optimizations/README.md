# Optimizations
This is the official source code repository containing C mathematical methods that will possibly be merged into the one-step-joint repository.

## Compilation
The bindings for the Raspberry Pi can be compiled using the command below:

> gcc -fPIC -shared -o calculator-optimizations.so calculator-optimizations.c -lm

## Preview
```c
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
```

## Explanation
Python, an interpreted language, can be quite slow when performing mathematical operations. Benchmarks will be eventually performed testing the difference between the baseline python operations and the optimized C binding operations.
* It is the goal that these C bindings will reduce the latency of the Raspberry Pi, allowing for extreme performance and efficiency.
