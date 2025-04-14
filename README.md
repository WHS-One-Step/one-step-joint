# One-Step-Joint
This is the official source code repository powering the prosthetic leg for team One-Step.

## Directories:
- Bootstrap: Contains linux scripts to bootstrap dependencies, the virtual environment, and linux packages for the raspberry pi.

- Components: Contains the core components that power the prosthetic leg, such as the learning model, the knee flexion calculator, and the GPIO writer.

- Data: Contains CSV files that are used to train the learning model.

- Learners: Contains learning models in the .pkl format, as well as the encoders for the particular models.

- Optimizations: Contains the C-optimized bindings for extensive math functions to increase performance and reduce latency

- Writer: Contains the C-optimized bindings for low level hardware access to GPIO pins, decreasing time in applying voltages to pins.

## Data:
* Ensure that all .CSV files in the **data folder** have appropriate lengths, as this can mess the sliding window algorithm (each data buffer should have a length of three).
    * (Length of CSV file - 1) / 3

* The tools used to collect data and predict gait states were purposely excluded from this repository to remove clutter.
    * Please use the one-step-learner repository that contains the appropriate tools to collect appropriate data and to have access to excluded tools.

    * Link: https://github.com/christopher-gholmieh/one-step-learner

## Installation:
Execute the following steps in a Linux terminal to install and run the project:
```bash
# Clone Repository:
git clone https://https://github.com/whs-one-step/one-step-joint && cd ./one-step-joint/

# Instructions:
chmod +x ./bootstrap/* # Transform the scripts into executables.

./bootstrap/bootstrap-raspberry.sh # Install appropriate linux dependencies.
./bootstrap/bootstrap-environment.sh # Install appropriate python dependencies and virtual environment.

venv/bin/python ./joint.py # Run the python project.
```

## Frameworks:
No frameworks were used in this repository, however an extensive amount of libraries came together to make this project possible. The libraries used are as follows:
- Joblib (Serialization of learner instances)
  
- Loguru (Logging information, warnings, and errors for debugging)

- Numpy (Optimized math functions for extensive calculations, such as dot products of matrices for angle calculation)

- Pandas (CSV processing for learner models)

- Phidget22 (Python library used to communicate with PhidgetSpatial Precision 3/3/3 IMUs)

- Scikit-learn (Used to create decision tree RainForestClassifier learner models to predict gait state)

- Scipy (Used for quaternion processing)

- Wiringpi (A C library used to provide low level access to GPIO pins)

- RPi.GPIO (Python library used to provide access to GPIO pins)

- Ctypes (Python library allowing for C bindings to be used to increase performance, e.g when performing extensive math calculations)

## Languages:
The two languages that make up this project are Python and C, not including the C-like language provided by Arduino. Python has an extensive support for libraries, allowing for faster development productivity. Code was optimized utilizing C through shared libraries and the **GCC** compiler, permitting compilation.
