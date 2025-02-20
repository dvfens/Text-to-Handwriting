import cv2
import numpy as np
from PIL import Image
import os

def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to get binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Remove noise
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    return binary

def extract_characters(image_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image: {image_path}")
        return
    
    # Process image
    binary = process_image(image)
    
    # Show the processed image
    cv2.imshow('Processed Image', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Instructions:")
    print("1. Click and drag to select a character")
    print("2. Press 'c' to capture the selection")
    print("3. Enter the character this represents")
    print("4. Press 'q' to quit when done")
    
    # Set up mouse callback
    drawing = False
    ix, iy = -1, -1
    
    def draw_rectangle(event, x, y, flags, param):
        nonlocal drawing, ix, iy
        
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_copy = binary.copy()
                cv2.rectangle(img_copy, (ix,iy), (x,y), (0,255,0), 2)
                cv2.imshow('Image', img_copy)
        
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x1, y1 = min(ix, x), min(iy, y)
            x2, y2 = max(ix, x), max(iy, y)
            
            # Get the selection
            selection = binary[y1:y2, x1:x2]
            
            # Show selection
            cv2.imshow('Selection', selection)
            
            # Wait for character input
            char = input("Enter the character this represents: ")
            
            if char:
                # Save the character image
                cv2.imwrite(os.path.join(output_dir, f'{char}.png'), selection)
                print(f"Saved character '{char}'")
            
            cv2.destroyWindow('Selection')
    
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_rectangle)
    
    while True:
        cv2.imshow('Image', binary)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    extract_characters('handwriting_sample.png', 'glyphs') 