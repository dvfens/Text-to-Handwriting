import cv2
import numpy as np
from PIL import Image
import os
import fontforge
import potrace
from pathlib import Path

def image_to_svg(image_path, output_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Convert to binary
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # Create bitmap from binary image
    bmp = potrace.Bitmap(binary)
    
    # Trace the bitmap to get paths
    path = bmp.trace()
    
    # Save as SVG
    with open(output_path, 'w') as f:
        f.write(path.export_svg())

def create_font(glyphs_dir):
    # Create new font
    font = fontforge.font()
    
    # Set font properties
    font.fontname = "MyHandwriting"
    font.familyname = "MyHandwriting"
    font.fullname = "MyHandwriting Regular"
    
    # Process each glyph image
    for glyph_file in Path(glyphs_dir).glob('*.png'):
        char = glyph_file.stem  # Get character from filename
        if len(char) != 1:
            continue
            
        # Convert PNG to SVG
        svg_path = glyph_file.with_suffix('.svg')
        image_to_svg(str(glyph_file), str(svg_path))
        
        # Create glyph
        glyph = font.createChar(ord(char))
        glyph.importOutlines(str(svg_path))
        glyph.autoHint()
    
    # Generate TTF file
    font.generate("MyHandwriting.ttf")

def process_handwriting():
    # Create glyphs directory
    os.makedirs('glyphs', exist_ok=True)
    
    # Read handwriting image
    img = cv2.imread('handwriting_sample.png')
    if img is None:
        print("Error: Could not read handwriting_sample.png")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    print("\nInstructions:")
    print("1. Click and drag to select a character")
    print("2. Release mouse to capture")
    print("3. Type the character it represents")
    print("4. Press 'q' to finish\n")
    
    # Variables for mouse callback
    drawing = False
    ix, iy = -1, -1
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, ix, iy
        
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_copy = img.copy()
                cv2.rectangle(img_copy, (ix,iy), (x,y), (0,255,0), 2)
                cv2.imshow('Select Characters', img_copy)
        
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x1, y1 = min(ix, x), min(iy, y)
            x2, y2 = max(ix, x), max(iy, y)
            
            # Get selection
            selection = binary[y1:y2, x1:x2]
            
            # Show selection
            cv2.imshow('Selected Character', selection)
            
            # Get character input
            char = input("Enter the character this represents (or press Enter to skip): ").strip()
            
            if char and len(char) == 1:
                # Save character image
                cv2.imwrite(f'glyphs/{char}.png', selection)
                print(f"Saved character '{char}'")
            
            cv2.destroyWindow('Selected Character')
    
    # Set up window and mouse callback
    cv2.namedWindow('Select Characters')
    cv2.setMouseCallback('Select Characters', mouse_callback)
    
    # Main loop
    while True:
        cv2.imshow('Select Characters', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    # Create font from saved glyphs
    create_font('glyphs')

if __name__ == "__main__":
    process_handwriting() 