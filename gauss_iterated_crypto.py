import numpy as np
from PIL import Image

import math

def gauss_iterated_map(x, alpha, beta, omega, K, phi, iterations):
    result = []
    for _ in range(iterations):
        x = math.exp(-alpha * (5/4 * ((x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)) % 1) - 1/2)**2 + beta)
        result.append(x)
    return result

def write_key_to_file(key, filename):
    with open(filename, 'w') as file:
        for value in key:
            file.write(f"{value}\n")

def encrypt(image_path, key):
    image = Image.open(image_path)
    image_array = np.array(image)
    flattened_image = image_array.flatten()

    # XOR each pixel value with the corresponding key value
    encrypted_data = [pixel ^ int(key[i % len(key)] * 255) for i, pixel in enumerate(flattened_image)]

    encrypted_image = np.array(encrypted_data, dtype=np.uint8).reshape(image_array.shape)
    return Image.fromarray(encrypted_image)

def decrypt(encrypted_image_path, key):
    encrypted_image = Image.open(encrypted_image_path)
    encrypted_image_array = np.array(encrypted_image)
    flattened_encrypted_data = encrypted_image_array.flatten()

    # XOR each pixel value with the corresponding key value
    decrypted_data = [pixel ^ int(key[i % len(key)] * 255) for i, pixel in enumerate(flattened_encrypted_data)]

    decrypted_image = np.array(decrypted_data, dtype=np.uint8).reshape(encrypted_image_array.shape)
    return Image.fromarray(decrypted_image)

# Example usage
initial_x = 0.5  # Initial value of x for the Gauss map
alpha = 4      # Value of alpha
beta = 0.8       # Value of beta
omega = 0.8      # Value of omega
K = 1000000          # Value of K
phi = math.pi        # Value of phi
iterations = 10000  # Number of iterations for the Gauss map

# Generate key using gauss_iterated_map
key = gauss_iterated_map(initial_x, alpha, beta, omega, K, phi, iterations)

# Write key to file
write_key_to_file(key, "key.txt")

# Encrypt image
encrypted_image = encrypt("maestro.png", key)
encrypted_image.save("encrypted_image.png")

# Decrypt image
decrypted_image = decrypt("encrypted_image.png", key)
decrypted_image.show()