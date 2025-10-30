import argparse
import cv2
import numpy as np
import os

def process_simple(operation, input_path, output_path):
    # 1. Load the image
    img = cv2.imread(input_path)
    
    if img is None:
        print(f"FATAL ERROR: Image not found or could not be loaded from: {input_path}")
        # Debugging: Show where the script is looking
        print(f"DEBUG: Current Working Directory is: {os.getcwd()}") 
        return

    processed_img = None

    if operation == 'grayscale':
        # Grayscale: Converts BGR (3-channel) to GRAY (1-channel)
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif operation == 'blur':
        # Blur: Gaussian filter with a 15x15 kernel (must be odd numbers)
        kernel_size = (15, 15)
        processed_img = cv2.GaussianBlur(img, kernel_size, 0)

    elif operation == 'edge':
        # Edge: Requires Grayscale first, then Canny detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # T1=100, T2=200 are common threshold values
        processed_img = cv2.Canny(gray, 100, 200)

    else:
        print(f"ERROR: Unsupported operation '{operation}'.")
        return

    # 2. Save the processed image
    if processed_img is not None:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Convert to 8-bit integer before saving (ensures compatibility)
        final_image = processed_img.astype(np.uint8) 
        
        # cv2.imwrite returns True on success, False on failure
        success = cv2.imwrite(output_path, final_image)
        
        if success:
            print(f"✅ Successfully applied {operation} and saved to {output_path}")
        else:
            print(f"❌ ERROR: Failed to write image to {output_path}. Check file permissions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Image Processor using OpenCV.")
    parser.add_argument('--operation', required=True, choices=['grayscale', 'blur', 'edge'], help='Image transformation to apply (grayscale, blur, edge).')
    parser.add_argument('--input', required=True, help='Path to the input image (e.g., images/city.jpg).')
    parser.add_argument('--output', required=True, help='Path to save the output image (e.g., outputs/city_gray.jpg).')

    args = parser.parse_args()
    process_simple(args.operation, args.input, args.output)