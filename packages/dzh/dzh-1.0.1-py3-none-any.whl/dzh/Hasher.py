from argon2 import low_level


ITERATIONS = 100
MEMORY_USAGE = 20  # the real memory usage will be 2^N in KiB
HASH_LENGTH = 50  # the real output len will be 2*HASH_LENGTH
THREADS = 8


class Hasher:
    def __init__(self, password, salt):
        self.password = password.encode()
        self.salt = salt.encode()

    def generate(self):
        print("Generating...")
        return low_level.hash_secret_raw(self.password, self.salt, time_cost=ITERATIONS,
                                         memory_cost=2 ** MEMORY_USAGE, parallelism=THREADS,
                                         hash_len=HASH_LENGTH, type=low_level.Type.I, version=19).hex()
