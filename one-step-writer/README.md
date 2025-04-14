# One-Step-Writer
This repository contains the official source code pertaining to the GPIO writer optimizations for one-step.

## Installation:
> $ sudo apt install ./wiringpi_3.14_arm64.deb

## Compilation:
> $ gcc -fPIC -shared -o one-step-writer.so one-step-writer.c -lm -l wiringPi
