from PIL import Image
import numpy as np
from scipy.ndimage import label
from scipy.signal import convolve2d

def count_intersections(image_path):
    # Load image as grayscale
    img = Image.open(image_path).convert('L')
    arr = np.array(img)

    # Binarize: black lines as 1, background 0
    binary = (arr < 128).astype(np.uint8)

    h, w = binary.shape

    # Detect axes using projection profiles (row and column sums)
    row_sums = binary.sum(axis=1)
    col_sums = binary.sum(axis=0)

    # Find the most prominent horizontal and vertical axes
    horizontal_axis = np.argmax(row_sums)
    vertical_axis = np.argmax(col_sums)

    # Remove axes with a small margin to avoid counting intersections on them
    margin = 3
    binary[max(horizontal_axis - margin, 0): min(horizontal_axis + margin + 1, h), :] = 0
    binary[:, max(vertical_axis - margin, 0): min(vertical_axis + margin + 1, w)] = 0

    # Define kernel to count neighbors in 8 directions
    neighbor_kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]], dtype=np.uint8)

    # Count black neighbors for each pixel
    neighbor_count = convolve2d(binary, neighbor_kernel, mode='same', boundary='fill', fillvalue=0)

    # Intersection pixels: black pixel with more than 2 black neighbors
    intersection_pixels = (binary == 1) & (neighbor_count > 2)

    # Cluster connected intersection pixels into single points
    labeled_array, num_features = label(intersection_pixels)

    return num_features

# For testing (uncomment and change path as needed)
# print(count_intersections("line_graph.jpg"))
