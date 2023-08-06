from getpass import getpass
from hashlib import sha256
from .hasher import Hasher
from random import SystemRandom
import pyperclip
from pyqrcode import create

BUILD = {"version": "1.0.0",
         "date": "2021-06-20"}


NONCE_MIN = 1000000
NONCE_MAX = 9999999


def print_build():
    print("DZ Hasher {}".format(BUILD["version"]))


def get_sha256(raw_string):
    return sha256(raw_string.encode("utf-8")).hexdigest()


def yes_or_no(question):
    try:
        while True:
            answer = input(question).lower().strip()[0]
            if answer == 'y':
                return True
            elif answer == 'n':
                return False
            else:
                print("Invalid answer, retry")
                continue
    except EOFError as e:
        print(e)


def get_hidden_int(requested_int_parameter):
    while True:
        try:
            hidden_int = int(getpass(requested_int_parameter).encode('utf-8'))
            if hidden_int < NONCE_MIN:
                raise ValueError
        except ValueError:
            print("Invalid input, {} must be an int of at least {} digits for this implementation".format(
                requested_int_parameter[:len(requested_int_parameter) - 2], len(str(NONCE_MIN))))
            continue
        return hidden_int


def get_nonce(is_first_time):
    if is_first_time:
        prng = SystemRandom()
        nonce = prng.randint(NONCE_MIN, NONCE_MAX)
        print("Nonce: ", nonce)
    else:
        nonce = get_hidden_int("Nonce: ")
    return nonce


def get_hidden_input(nonce):
    return get_sha256(getpass("Password: ")),\
        get_sha256(str(get_hidden_int("Salt: ") + nonce))


def get_qr(value):
    qr = create(value)
    qr.show()


def main():
    try:
        is_first_time = yes_or_no("Is this the first time? [y/n]: ")
        nonce = get_nonce(is_first_time)
        password, salt = get_hidden_input(nonce)

        if is_first_time:
            print("Confirm requested, retype")
            password_confirm, salt_confirm = get_hidden_input(nonce)
            if password != password_confirm or salt != salt_confirm:
                print("The two input doesn't match, retry.")
                return

        secret = Hasher(password, salt).generate()

        print("Done!")
        try:
            pyperclip.copy(secret)
        except Exception:
            print("Error: xclip needed")
        if yes_or_no("Display the QR code? [y/n]: "):
            get_qr(secret)

    except KeyboardInterrupt:
        print("\nCtrl-c signal received.")

    print("Exit.")
    return


if __name__ == "__main__":
    print_build()
    main()
