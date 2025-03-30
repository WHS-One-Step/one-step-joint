# Written by: Christopher Gholmieh
# Sources:

# Functions:
function bootstrap-environment {
    # Validation:
    if [ ! -f ./joint.py ]; then
        echo "[!] Please rerun this script in the project directory." && exit
    fi

    # Initialization:
    echo "[*] Initializing virtual environment.."

    # Command:
    python3 -m venv venv

    # Libraries:
    echo "[*] Installing appropriate dependencies.."

    # Command:
    ./venv/bin/pip install -r ./requirements.txt

    # Termination:
    echo "[*] Finished installing dependencies.." && exit
}


# Main:
bootstrap-environment
