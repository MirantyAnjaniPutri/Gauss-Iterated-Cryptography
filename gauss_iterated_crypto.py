import numpy as np
from PIL import Image

def gauss_map(x, r):
    return r * x * (1 - x)

def generate_key(seed, iterations, r):
    key = []
    x = seed
    for _ in range(iterations):
        x = gauss_map(x, r)
        key.append(x)
    return key

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
seed = 0.5  # Initial seed for the Gauss map
iterations = 10000  # Number of iterations to generate the key
r = 3.8  # Parameter for the Gauss map

# Generate key
key = generate_key(seed, iterations, r)

# Write key to file
write_key_to_file(key, "key.txt")

# Encrypt image
encrypted_image = encrypt("maestro.png", key)
encrypted_image.save("encrypted_image.png")

# Decrypt image
decrypted_image = decrypt("encrypted_image.png", key)
decrypted_image.show()