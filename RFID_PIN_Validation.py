import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
import time
import os

# Define valid PINs for validation
VALID_PINS = ['12345', '78965', '45454']

# Function to read the PIN from the block
def read_pin_from_block(pn532, uid, block_number=6):
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Default key A
    try:
        pn532.mifare_classic_authenticate_block(uid, block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
        data = pn532.mifare_classic_read_block(block_number)
        return data.decode('utf-8').strip('\x00')  # Decode and remove padding zeros
    except Exception as e:
        print("Error reading PIN:", e)
        return None

# Function to clear the screen (cross-platform support for Linux/Windows)
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux/macOS
        os.system('clear')

# Main function to run the validation script
def main():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)

    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    pn532.SAM_configuration()

    while True:  # Loop to continuously check for cards
        print('Waiting for RFID/NFC card for validation...')
        uid = None
        while uid is None:
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="", flush=True)  # Keep printing dots while waiting for a card

        print('\nFound card with UID:', [hex(i) for i in uid])

        # Read the PIN from the block
        pin_read = read_pin_from_block(pn532, uid)

        # Check if the PIN matches
        if pin_read in VALID_PINS:
            print("\nACCESS GRANTED! Valid PIN:", pin_read)
        else:
            print("\nACCESS DENIED! Invalid PIN:", pin_read)

        # Wait for 5 seconds to show the result clearly
        time.sleep(5)

        # Clear the screen before prompting for a new card
        clear_screen()

        # Prompt for the next card
        print('Please scan a new RFID card for authentication.\n')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up GPIO...")
        GPIO.cleanup()
