import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
import time

# Function to get the PIN from the user
def get_pin():
    while True:
        pin = input("Enter the PIN to write to the RFID card (max 16 characters): ")
        if len(pin) <= 16:
            return pin
        else:
            print("PIN too long! Please enter a PIN with 16 characters or less.")

# Function to write the PIN to an RFID card
def write_pin_to_card(pn532, pin):
    # Convert the chosen PIN to bytes
    data = pin.encode('utf-8')  # Encode the PIN as UTF-8
    data = data.ljust(16, b'\x00')[:16]  # Pad with zeros or truncate if necessary

    print('Waiting for RFID/NFC card to write to!')
    uid = None
    while uid is None:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="", flush=True)
    print('\nFound card with UID:', [hex(i) for i in uid])

    # Write to block #6 (user can modify this if needed)
    block_number = 6
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Default key A

    try:
        pn532.mifare_classic_authenticate_block(
            uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
        pn532.mifare_classic_write_block(block_number, data)
        if pn532.mifare_classic_read_block(block_number) == data:
            print('Write to block %d successfully' % block_number)
        else:
            print('Failed to verify the written data.')
    except nfc.PN532Error as e:
        print("Authentication or write error:", e.errmsg)

# Main function to run the script
def main():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)

    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    while True:
        # Get the PIN from the user
        pin_to_write = get_pin()

        # Write the PIN to the RFID card
        write_pin_to_card(pn532, pin_to_write)

        # Wait for 5 seconds before prompting for the next card
        print("\nWaiting 5 seconds before writing to the next card...")
        time.sleep(5)

        # Ask the user if they want to write another card or exit
        write_another = input("Do you want to write another PIN to a new RFID card? (y/n): ").strip().lower()
        if write_another != 'y':
            break

    print("Exiting program. Cleaning up GPIO...")
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up GPIO...")
        GPIO.cleanup()
