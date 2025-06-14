import numpy as np
from PIL import Image
import argparse

# A delimiter to mark the end of the secret message
DELIMITER = "#####"

def to_binary(data):
    """Convert data to a binary string."""
    if isinstance(data, str):
        return ''.join(format(ord(i), '08b') for i in data)
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, '08b')
    else:
        raise TypeError("Type not supported for binary conversion")

def encode_message(image, secret_message):
    """Hides a secret message within an image using LSB steganography."""
    # Check if the image has an alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
        
    width, height = image.size
    max_bytes = (width * height * 4) // 8  # 4 channels (RGBA)
    
    print(f"[*] Maximum message size: {max_bytes} bytes")
    
    secret_message += DELIMITER
    
    if len(secret_message) > max_bytes:
        raise ValueError("[!] Message is too large for the image.")
        
    print("[*] Encoding message...")
    
    binary_secret_message = to_binary(secret_message)
    data_index = 0
    
    # Get image data as a NumPy array for fast manipulation
    img_data = np.array(image)

    for row in img_data:
        for pixel in row:
            # Get the RGBA values of the pixel
            r, g, b, a = to_binary(pixel)
            
            # Modify the LSB of the red channel
            if data_index < len(binary_secret_message):
                pixel[0] = int(r[:-1] + binary_secret_message[data_index], 2)
                data_index += 1
            # Modify the LSB of the green channel
            if data_index < len(binary_secret_message):
                pixel[1] = int(g[:-1] + binary_secret_message[data_index], 2)
                data_index += 1
            # Modify the LSB of the blue channel
            if data_index < len(binary_secret_message):
                pixel[2] = int(b[:-1] + binary_secret_message[data_index], 2)
                data_index += 1
            # Modify the LSB of the alpha channel
            if data_index < len(binary_secret_message):
                pixel[3] = int(a[:-1] + binary_secret_message[data_index], 2)
                data_index += 1

            # If message is fully encoded, break out
            if data_index >= len(binary_secret_message):
                break
        if data_index >= len(binary_secret_message):
            break
            
    encoded_image = Image.fromarray(img_data)
    return encoded_image

def decode_message(image):
    """Extracts a hidden message from an image."""
    print("[*] Decoding message...")
    binary_data = ""
    img_data = np.array(image)

    for row in img_data:
        for pixel in row:
            r, g, b, a = to_binary(pixel)
            binary_data += r[-1]  # Extract LSB from red channel
            binary_data += g[-1]  # Extract LSB from green channel
            binary_data += b[-1]  # Extract LSB from blue channel
            binary_data += a[-1]  # Extract LSB from alpha channel

    # Split by 8-bits
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]

    # Convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-len(DELIMITER):] == DELIMITER:
            print("[*] Delimiter found. Message decoded.")
            return decoded_data[:-len(DELIMITER)]
            
    return "No hidden message found or message is corrupted."

def main():
    parser = argparse.ArgumentParser(description="Steganography Tool: Hide messages in images.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encoder command
    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image.")
    encode_parser.add_argument("-i", "--input", required=True, help="Input image file (cover image).")
    encode_parser.add_argument("-o", "--output", required=True, help="Output image file (stego image).")
    encode_parser.add_argument("-m", "--message", required=True, help="The secret message to hide.")

    # Decoder command
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image.")
    decode_parser.add_argument("-i", "--input", required=True, help="Input image file to decode.")

    args = parser.parse_args()

    if args.command == "encode":
        try:
            image = Image.open(args.input)
            encoded_image = encode_message(image, args.message)
            encoded_image.save(args.output, "PNG")
            print(f"[+] Message encoded successfully into {args.output}")
        except FileNotFoundError:
            print(f"[!] Error: The file {args.input} was not found.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

    elif args.command == "decode":
        try:
            image = Image.open(args.input)
            message = decode_message(image)
            print(f"[*] Decoded Message: {message}")
        except FileNotFoundError:
            print(f"[!] Error: The file {args.input} was not found.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()