# One-Step-Joint
This is the official source code repository powering the prosthetic leg for team One-Step.

## Directories:
- Bootstrap: Contains linux scripts to bootstrap dependencies, the virtual environment, and linux packages for the raspberry pi.

- Components: Contains the core components that power the prosthetic leg, such as the learning model, the knee flexion calculator, and the GPIO writer.

- Data: Contains CSV files that are used to train the learning model.

- Learners: Contains learning models in the .pkl format, as well as the encoders for the particular models.

## Data:
* Ensure that all .CSV files in the **data folder** have appropriate lengths, as this can mess the sliding window algorithm (each data buffer should have a length of three).
    * (Length of CSV file - 1) / 3

* The tools used to collect data and predict gait states were purposely excluded from this repository to remove clutter.
    * Please use the one-step-learner repository that contains the appropriate tools to collect appropriate data and to have access to excluded tools.

    * Link: https://github.com/christopher-gholmieh/one-step-learner

## Installation:
```bash
# Clone Repository:
git clone https://https://github.com/whs-one-step/one-step-joint && cd ./one-step-joint/

# Instructions:
chmod +x ./bootstrap/* # Transform the scripts into executables.

./bootstrap/bootstrap-raspberry.sh # Install appropriate linux dependencies.
./bootstrap/bootstrap-environment.sh # Install appropriate python dependencies and virtual environment.

venv/bin/python ./joint.py # Run the python project.
```
