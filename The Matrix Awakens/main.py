import cv2
import numpy as np
import os
import platform

# --- Configuration ---
SCALE_FACTOR = 0.15  # Adjust to change the output size. Smaller value = smaller art.
# Use a more detailed character set for better gradients
ASCII_CHARS = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNW%&@"

def get_terminal_size():
    """Gets the size of the terminal window."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24  # Default size

def clear_screen():
    """Clears the terminal screen."""
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def image_to_ascii(image, width, height):
    """Converts a single image frame to an ASCII string."""
    # Resize the image to fit the desired dimensions
    image = cv2.resize(image, (width, height))
    
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Map pixel intensity to ASCII characters
    # Each pixel (0-255) is mapped to an index in the ASCII_CHARS string
    indices = (gray_image / 255.0 * (len(ASCII_CHARS) - 1)).astype(int)
    ascii_frame = "\n".join("".join(ASCII_CHARS[pixel] for pixel in row) for row in indices)
    
    return ascii_frame

def main():
    """Main function to capture video and display ASCII art."""
    # Attempt to open the default webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame. Exiting ...")
                break

            # Get terminal size and calculate ASCII art dimensions
            term_width, term_height = get_terminal_size()
            
            # Use a scale factor to make it smaller than the full terminal
            # to prevent line wrapping issues and improve performance
            ascii_width = int(term_width * SCALE_FACTOR * 2) # *2 for character aspect ratio
            ascii_height = int(term_height * SCALE_FACTOR)

            # Generate the ASCII art for the current frame
            ascii_frame = image_to_ascii(frame, ascii_width, ascii_height)

            # Clear the screen and print the new frame
            clear_screen()
            print(ascii_frame)

            # Exit loop if 'q' is pressed
            # Note: This check is rudimentary and might not always capture the key
            # press immediately, as the focus needs to be on the terminal.
            # A more robust solution would use a library like `keyboard`.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        print("\nWebcam released. Program terminated.")

if __name__ == '__main__':
    main()