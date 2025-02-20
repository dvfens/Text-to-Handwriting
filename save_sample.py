import numpy as np
from PIL import Image
import base64
import io

# This is where we'll store the base64 image data
image_data = None  # Replace with actual base64 image data

if image_data:
    # Decode base64 image
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    
    # Save as PNG
    image.save("handwriting_sample.png")
    print("Saved handwriting sample as handwriting_sample.png")
else:
    print("Please provide the base64 image data") 