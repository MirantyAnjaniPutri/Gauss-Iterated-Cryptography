import numpy as np
from PIL import Image
import math

class GaussCircleCrypto:
    def __init__(self, initial_x = 0.5, iterations = 10000):
        self.initial_x = initial_x
        self.iterations = iterations
        self.alpha = 9
        self.beta = 0.481
        self.omega = 0.5
        self.K = 1000000

    def gauss_iterated_map(self):
        result = []
        x = self.initial_x
        for _ in range(self.iterations):
            x = math.exp(-self.alpha * (5/4 * ((x + self.omega + self.K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2 + self.beta)
            y = int(x * 10**13)
            result.append(y)
        return result

    def write_key_to_file(self, key, filename):
        with open(filename, 'w') as file:
            for value in key:
                binary_value = "{0:b}".format(value)
                file.write(f"{binary_value}\n")

    def encrypt(self, image_path, key):
        image = Image.open(image_path)
        image_array = np.array(image)
        flattened_image = image_array.flatten()

        # XOR each pixel value with the corresponding key value
        encrypted_data = [pixel ^ int(key[i % len(key)] * 255) for i, pixel in enumerate(flattened_image)]

        encrypted_image = np.array(encrypted_data, dtype=np.uint8).reshape(image_array.shape)
        return Image.fromarray(encrypted_image)
    
    def read_key_from_file(self, filename):
        key = []
        with open(filename, 'r') as file:
            for line in file:
                # Convert binary string to integer
                key_value = int(line.strip(), 2)
                key.append(key_value)
        return key


    def decrypt(self, encrypted_image_path, key):
        encrypted_image = Image.open(encrypted_image_path)
        encrypted_image_array = np.array(encrypted_image)
        flattened_encrypted_data = encrypted_image_array.flatten()

        # XOR each pixel value with the corresponding key value
        decrypted_data = [pixel ^ int(key[i % len(key)] * 255) for i, pixel in enumerate(flattened_encrypted_data)]

        decrypted_image = np.array(decrypted_data, dtype=np.uint8).reshape(encrypted_image_array.shape)
        return Image.fromarray(decrypted_image)


# # Generate key using gauss_iterated_map
# encryptor = GaussCircleCrypto()

# # Generate key using gauss_iterated_map
# key = encryptor.gauss_iterated_map()

# # Write key to file
# encryptor.write_key_to_file(key, "key.txt")

# read_key = encryptor.read_key_from_file("key.txt")

# # Encrypt image
# encrypted_image = encryptor.encrypt("maestro.png", key)
# encrypted_image.save("encrypted_image.png")

# # Decrypt image
# decrypted_image = encryptor.decrypt("encrypted_image.png", read_key)
# decrypted_image.show()