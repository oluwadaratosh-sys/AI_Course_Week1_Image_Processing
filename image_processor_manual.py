import argparse
import cv2
import numpy as np

# --- 1. Grayscale: Vector Operation ---
def manual_grayscale(img_float):
    """
    Manually converts an BGR image (3D array) to grayscale (2D array)
    using the luminosity weighted average (Vector Operation).
    BGR indices: B=0, G=1, R=2 (OpenCV default).
    """
    # Isolate color channels using NumPy slicing
    B = img_float[:, :, 0]
    G = img_float[:, :, 1]
    R = img_float[:, :, 2]

    # Perform the weighted sum (Vector Operation)
    # Gray = 0.114*B + 0.587*G + 0.299*R
    grayscale_img = (0.114 * B) + (0.587 * G) + (0.299 * R)
    
    return grayscale_img

# --- 2. Convolution: Core Matrix Operation ---
def convolve2d(image, kernel):
    """
    Performs 2D convolution (a Matrix Operation) by sliding a kernel
    over the image, performing element-wise multiplication and summation.
    NOTE: This uses 'valid' padding, making the output slightly smaller.
    """
    # 1. Flip the kernel (standard convolution definition)
    kernel = np.flipud(np.fliplr(kernel))
    
    # Get dimensions
    i_h, i_w = image.shape
    k_h, k_w = kernel.shape
    
    # Calculate output dimensions
    o_h = i_h - k_h + 1
    o_w = i_w - k_w + 1
    
    # Initialize the output matrix
    output = np.zeros((o_h, o_w), dtype=image.dtype)

    # 2. Slide the kernel over the image
    for y in range(o_h):
        for x in range(o_w):
            # Extract the Region of Interest (ROI)
            roi = image[y:y + k_h, x:x + k_w]
            
            # 3. Element-wise multiplication and summation (the matrix operation)
            output[y, x] = np.sum(roi * kernel)
            
    return output

# --- 3. Blur: Matrix Operation (using convolution) ---
def manual_blur(img_gray):
    """
    Applies an Averaging Blur filter using the convolve2d function.
    """
    # Define a 5x5 average kernel (all elements are 1/25)
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size * kernel_size)
    
    # Apply the convolution
    blurred_img = convolve2d(img_gray, kernel)
    return blurred_img

# --- 4. Edge Detection: Matrix and Vector Operations ---
def manual_edge(img_gray):
    """
    Applies Sobel filters (Matrix Operation) to find gradients and 
    calculates the gradient magnitude (Vector Operation) for edge detection.
    """
    # Define Sobel kernels for horizontal (Gx) and vertical (Gy) gradients
    sobel_x = np.array([[-1, 0, 1], 
                        [-2, 0, 2], 
                        [-1, 0, 1]], dtype=np.float32)
                        
    sobel_y = np.array([[-1, -2, -1], 
                        [ 0,  0,  0], 
                        [ 1,  2,  1]], dtype=np.float32)

    # Convolve with both kernels (Matrix Operation)
    Gx = convolve2d(img_gray, sobel_x)
    Gy = convolve2d(img_gray, sobel_y)

    # Calculate the final gradient magnitude (Vector Operation)
    # Magnitude = sqrt(Gx^2 + Gy^2)
    magnitude = np.sqrt(Gx**2 + Gy**2)
    
    return magnitude

# ----------------------------------------
# Main processing logic and command line arguments
# ----------------------------------------

def process_manual(operation, input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not load image from {input_path}")
        return

    processed_img = None
    
    # Convert image to float32 for accurate numerical calculations
    img_float = img.astype(np.float32)

    if operation == 'grayscale':
        # Apply manual grayscale function
        processed_img = manual_grayscale(img_float)

    else:
        # Blur and Edge detection typically start from a grayscale image
        gray_img = manual_grayscale(img_float)
        
        if operation == 'blur':
            processed_img = manual_blur(gray_img) 
        elif operation == 'edge':
            processed_img = manual_edge(gray_img)
        else:
            print(f"Error: Unsupported operation '{operation}'.")
            return

    # Final cleanup and saving
    if processed_img is not None:
        # Clip values to 0-255 range and convert back to 8-bit integer
        processed_img = np.clip(processed_img, 0, 255).astype(np.uint8)
        cv2.imwrite(output_path, processed_img)
        print(f"✅ Successfully applied {operation} (MANUAL) and saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manual Image Processor using NumPy for array/matrix operations.")
    parser.add_argument('--operation', required=True, choices=['grayscale', 'blur', 'edge'], help='Image transformation to apply.')
    parser.add_argument('--input', required=True, help='Path to the input image.')
    parser.add_argument('--output', required=True, help='Path to save the output image.')

    args = parser.parse_args()
    process_manual(args.operation, args.input, args.output)