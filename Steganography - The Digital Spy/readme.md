# Steganography: The Digital Spy

This is a command-line tool to encode and decode secret messages within PNG image files using the Least Significant Bit (LSB) steganography technique.

The encoded image looks virtually identical to the original, allowing you to hide data in plain sight.

## Features
- **Encode**: Hide a secret text message inside a cover image.
- **Decode**: Extract a hidden message from an encoded image.
- Uses a delimiter to know when the message ends.

## Requirements
You'll need Python 3 and the Pillow library.

```bash
pip install Pillow numpy
