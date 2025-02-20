import fontforge
import os

def create_font():
    # Create a new font
    font = fontforge.font()
    
    # Set font properties
    font.fontname = "MyHandwriting"
    font.familyname = "MyHandwriting"
    font.fullname = "MyHandwriting"
    font.encoding = "UnicodeFull"
    
    # Get all SVG files from the glyphs directory
    glyphs_dir = "glyphs"
    svg_files = sorted([f for f in os.listdir(glyphs_dir) if f.endswith('.svg')])
    
    # Define the characters to map (adjust as needed)
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # Import glyphs and map them to characters
    for char, svg_file in zip(chars, svg_files):
        # Create glyph
        glyph = font.createChar(ord(char))
        
        # Import SVG
        svg_path = os.path.join(glyphs_dir, svg_file)
        glyph.importOutlines(svg_path)
        
        # Auto-scale and center the glyph
        glyph.autoWidth(70, 10)  # Adjust spacing as needed
        glyph.round()  # Round to integer coordinates
        
        print(f"Processed character: {char}")
    
    # Generate font files
    font.generate("MyHandwriting.ttf")
    print("Font file generated: MyHandwriting.ttf")

if __name__ == "__main__":
    create_font() 