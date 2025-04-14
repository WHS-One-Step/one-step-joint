// Written by: Christopher Gholmieh
// Imports:

// Standard:
#include <stdio.h>
#include <stdlib.h>

// Library:
#include "one-step-writer.h"

// Wiring:
#include <wiringPi.h>


// Constants:
// Values:
const int values[] = {128, 64, 32, 16, 8, 4, 2, 1};

// Pins:
const int pins[] = {14, 15, 18, 23, 24, 25, 8, 7};

// Variables (Assignment):
// Status:
int status[] = {0, 0, 0, 0, 0, 0, 0, 0};


// Methods:
void initialize_optimizations() {
    // Initialization:
    wiringPiSetupGpio();
}

void initialize_pins() {
    // Initialization:
    for (int iteration = 0; iteration < 8; iteration++) {
        pinMode(pins[iteration], OUTPUT);

        pullUpDnControl(pins[iteration], PUD_DOWN);
    }

    pinMode(STOP_PIN, OUTPUT);
    pullUpDnControl(STOP_PIN, PUD_DOWN);
}

char* number_to_binary(unsigned char number) {
    // Variables (Assignment):
    // Binary:
    char* binary = (char*) malloc(sizeof(char) * 9);

    if (binary == NULL) {
        fprintf(stderr, "%s", "[!] Failed to allocate memory for binary.\n");
    }

    // Logic:
    for (int iteration = 7; iteration >= 0; iteration--) {
        binary[7 - iteration] = ((number >> iteration) & 1) ? '1' : '0';
    }

    binary[8] = '\0';

    return binary;
}

void write_pulse_modulation(int pulse_modulation) {
    // Variables (Assignment):
    // Binary:
    char* binary = number_to_binary((unsigned char) pulse_modulation);

    // Logic:
    digitalWrite(STOP_PIN, LOW);

    for (int iteration = 7; iteration >= 0; iteration--) {
        if (binary[iteration] == '1' && status[iteration] == 0) {
            digitalWrite(pins[iteration], HIGH);
            status[iteration] = 1;

            continue;
        } else if (binary[iteration] == '0' && status[iteration] == 1) {
            digitalWrite(pins[iteration], LOW);
            status[iteration] = 0;
        }
    }

    free(binary);
}

void write_stop_pin() {
    for (int iteration = 0; iteration < 8; iteration++) {
        digitalWrite(pins[iteration], LOW);
    }

    digitalWrite(STOP_PIN, HIGH);
}
