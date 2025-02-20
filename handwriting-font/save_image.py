from PIL import Image
import numpy as np

# Create a new image with white background
width = 800
height = 400
background = Image.new('RGB', (width, height), 'white')

# Save the image
background.save('handwriting_sample.png') 