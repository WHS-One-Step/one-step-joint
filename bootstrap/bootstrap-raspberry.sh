# Written by: Christopher Gholmieh
# Sources:

# Functions:
function bootstrap-raspberry() {
    # Validation:
    if [[ "$EUID" != "0" ]]; then
        echo "[*] Please rerun this script as root." && exit
    fi

    # Execution:
    echo "[*] Executing dependency installer.."

    # Download:
    if curl -fsSL https://www.phidgets.com/downloads/setup_linux | bash -; then
        echo "[*] Phidgets setup script executed successfully."
    else
        echo "[!] Failed to execute Phidgets setup script. Exiting." && exit 1
    fi

    # Package:
    if apt-get install -y libphidget22; then
        echo "[*] libphidget22 installed successfully."
    else
        echo "[!] Failed to install libphidget22. Exiting." && exit 1
    fi

    # Clean:
    clear

    # Exiting:
    echo "[*] Finished installing required dependencies.." && exit
}


# Main:
bootstrap-raspberry