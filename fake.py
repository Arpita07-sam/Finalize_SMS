import cv2
import numpy as np

def forensic_green_extraction(image_path):
    # 1. Load the image
    img = cv2.imread(image_path)
    # Convert to float32 for high-precision math
    data = img.astype(np.float32) / 255.0
    
    # 2. Focus on the 'Green Dominance'
    # In RGB, black text has R≈G≈B. Green ink has G > R and G > B.
    # We create a 'Pure Green' score for every pixel
    b, g, r = cv2.split(data)
    
    # Calculate how much "greener" a pixel is compared to the other channels
    # This specifically targets the green ink signature
    green_score = g - (r * 0.5 + b * 0.5)
    
    # 3. Enhance the contrast of the signature
    green_score = np.clip(green_score, 0, 1)
    green_score = (green_score * 255).astype(np.uint8)
    
    # 4. Use Otsu's Binarization to find the signature automatically
    _, mask = cv2.threshold(green_score, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 5. Noise Removal (Removes tiny speckles from the paper texture)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 6. Apply to original image to get the color signature back
    # This keeps the green ink texture while making everything else transparent
    result = cv2.merge([img[:,:,0], img[:,:,1], img[:,:,2], mask])
    
    return result

# Save as PNG to keep transparency
final_extraction = forensic_green_extraction('extracted_signature.jpg')
cv2.imwrite('extracted.png', final_extraction)