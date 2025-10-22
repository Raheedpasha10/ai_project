import cv2
import numpy as np
from skimage import filters

def enhance_image(image):
    """Enhance image contrast and sharpness."""
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Contrast enhancement
    enhanced = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
    # Sharpen using unsharp mask
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
    sharpened = filters.unsharp_mask(enhanced, radius=1.0, amount=1.5)
    return (sharpened * 255).astype(np.uint8)

def simulate_degradation(image, degrade_type):
    """Simulate degradation effects on the image."""
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    if degrade_type == "thermal damage":
        # Simulate thermal damage with noise
        noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
        degraded = cv2.add(image, noise)
    elif degrade_type == "water damage":
        # Simulate water damage with blur
        degraded = cv2.GaussianBlur(image, (15, 15), 0)
    else:  # trauma
        # Simulate trauma with random dark patches
        mask = np.random.randint(0, 2, image.shape).astype(np.uint8) * 50
        degraded = cv2.subtract(image, mask)
    return degraded
