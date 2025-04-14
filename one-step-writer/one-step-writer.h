// Written by: Christopher Gholmieh
// Guards:
#ifndef __ONE_STEP_WRITER_H__
#define __ONE_STEP_WRITER_H__

// Definitions:
#define STOP_PIN 12

// Methods:
void initialize_optimizations();
void initialize_pins();

char* number_to_binary(unsigned char number);

void write_pulse_modulation(int pulse_modulation);
void write_stop_pin();

// Guard:
#endif // __ONE_STEP_WRITER_H__
