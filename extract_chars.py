import cv2
import numpy as np
import os
import svgwrite
from PIL import Image

def process_image(image_path):
    print(f"Processing image: {image_path}")
    
    # Read the image using PIL first
    pil_image = Image.open(image_path)
    print(f"Image size: {pil_image.size}, mode: {pil_image.mode}")
    
    # Convert to RGB if needed
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Convert PIL image to numpy array for OpenCV
    image = np.array(pil_image)
    print(f"Numpy array shape: {image.shape}")
    
    # Convert BGR to RGB if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(f"Grayscale shape: {gray.shape}")
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,  # Block size
        2    # C constant
    )
    
    # Remove noise
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Save debug images
    cv2.imwrite('debug_gray.png', gray)
    cv2.imwrite('debug_binary.png', binary)
    
    return binary

def extract_characters(binary_image):
    # Find contours
    contours, hierarchy = cv2.findContours(
        binary_image, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    print(f"Found {len(contours)} contours")
    
    # Filter and sort contours
    valid_contours = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        # Filter based on area and aspect ratio
        if area > 50 and 0.1 < w/h < 10:  # Adjust these thresholds as needed
            valid_contours.append((x, y, w, h, contour))
            print(f"Contour {i}: pos=({x},{y}), size={w}x{h}, area={area}")
    
    # Sort contours left to right
    valid_contours.sort(key=lambda x: x[0])
    
    return valid_contours

def save_character_svg(contour, output_path, width, height):
    # Create SVG drawing with some padding
    padding = 5
    dwg = svgwrite.Drawing(
        output_path, 
        size=(width + 2*padding, height + 2*padding)
    )
    
    # Create a group with translation to add padding
    g = dwg.g(transform=f'translate({padding},{padding})')
    
    # Convert contour to path data
    path_data = []
    first_point = True
    
    for point in contour:
        x, y = point[0]
        if first_point:
            path_data.append(f"M {x},{y}")
            first_point = False
        else:
            path_data.append(f"L {x},{y}")
    
    path_data.append("Z")  # Close the path
    path_str = " ".join(path_data)
    
    # Add path to group
    g.add(dwg.path(d=path_str, fill="black"))
    
    # Add group to drawing
    dwg.add(g)
    
    # Save SVG file
    dwg.save()
    print(f"Saved SVG: {output_path}")

def main():
    # Create output directory if it doesn't exist
    output_dir = "glyphs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process image
    try:
        binary_image = process_image("handwriting_sample.png")
    except Exception as e:
        print(f"Error processing image: {e}")
        return
    
    # Extract characters
    characters = extract_characters(binary_image)
    print(f"\nExtracted {len(characters)} valid characters")
    
    # Save each character as SVG
    for i, (x, y, w, h, contour) in enumerate(characters):
        # Create SVG file
        svg_path = os.path.join(output_dir, f"char_{i}.svg")
        save_character_svg(contour, svg_path, w, h)

if __name__ == "__main__":
    main() 