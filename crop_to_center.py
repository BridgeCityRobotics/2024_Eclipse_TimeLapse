from PIL import Image, ImageEnhance
import os
import cv2
import numpy as np
from scipy.optimize import least_squares

def crop_image_center_old(image_path, crop_width, crop_height):
    # Open the image
    with Image.open(image_path) as img:
        # Calculate the center point
        #center_x, center_y = img.width // 2, img.height // 2
        
        # Load the image in grayscale
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply a binary threshold to the image
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour which should be the eclipse
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        print(M)
        if M["m00"] != 0:
            # Calculate the centroid of the contour
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
        else:
            # If the contour is a line (m00 == 0), then use the bounding rectangle
            x, y, w, h = cv2.boundingRect(max_contour)
            center_x, center_y = x + w // 2, y + h // 2
        
        # Calculate the coordinates of the upper-left and lower-right corners of the crop box
        left = center_x - crop_width // 2
        upper = center_y - crop_height // 2
        right = center_x + crop_width // 2
        lower = center_y + crop_height // 2
        
        # Crop the image
        cropped_img = img.crop((left, upper, right, lower))
        
        cropped_img = add_warmth(cropped_img)
        
        return cropped_img
        

def add_warmth(image):
    
    # Increase red channel, decrease blue channel
    increase = 20  # Adjust this value to control the effect
    blue, green, red = cv2.split(image)
    red = np.clip(red + increase, 0, 255)
    blue = np.clip(blue - increase, 0, 255)
    
    # Merge the channels back
    warmed_image = cv2.merge([blue, green, red])
    
    return warmed_image
    
    
def add_warmth_pil(image, enhancement=1.2):
    
    # Enhance the color to add warmth
    enhancer = ImageEnhance.Color(image)
    warm_image = enhancer.enhance(enhancement)
    
    # Optionally, you can also enhance the red channel specifically
    # but usually, color enhancement should suffice for a warm effect
    
    return warm_image
    
    

def fit_circle_to_contour(contour):
    # Initial guess for the circle's center and radius
    x0, y0 = np.mean(contour[:, 0, :], axis=0)
    r0 = np.mean(np.sqrt((contour[:, 0, 0] - x0)**2 + (contour[:, 0, 1] - y0)**2))

    def residuals(circle, contour):
        x_center, y_center, radius = circle
        x_contour, y_contour = contour[:, 0, 0], contour[:, 0, 1]
        return np.sqrt((x_contour - x_center)**2 + (y_contour - y_center)**2) - radius

    # Optimize the circle fit
    optimized = least_squares(residuals, x0=[x0, y0, r0], args=(contour,))
    x_center, y_center, radius = optimized.x
    return int(x_center), int(y_center), int(radius)

def center_eclipse_on_sun(image_path, crop_width, crop_height):
    # Load the original image
    original_image = cv2.imread(image_path)
    # Convert the original image to grayscale for processing
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # image = cv2.imread(image_path)
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale image
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour which should be the eclipse
    max_contour = max(contours, key=cv2.contourArea)

    # Fit a circle to the largest contour, which should approximate the sun
    x_center, y_center, _ = fit_circle_to_contour(max_contour)

    # Calculate the distance to move the center of the sun to the center of the image
    rows, cols, _ = original_image.shape
    shift_x = cols // 2 - x_center
    shift_y = rows // 2 - y_center

    # Create the transformation matrix for the translation
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])

    # Perform the translation on the original colored image
    shifted = cv2.warpAffine(original_image, M, (cols, rows))
    
    # Calculate the coordinates of the upper-left and lower-right corners of the crop box
    left = x_center - crop_width // 2
    upper = y_center - crop_height // 2
    right = x_center + crop_width // 2
    lower = y_center + crop_height // 2
    
    # Crop the image
    cropped_img = shifted[left:right, upper:lower]
    
    # cropped_img = add_warmth(cropped_img)
    
    return Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    

# Example usage:
cropped_image = center_eclipse_on_sun(r"D:\2024 Total Eclipse\frames_centered\frame_5240.jpg", 1200, 1200)
cropped_image.show()

stop()
source_folder = r'D:\2024 Total Eclipse\frames_centered'
destination_folder = r'D:\2024 Total Eclipse\frames_shrunk'

# List all files in the source folder
files = os.listdir(source_folder)

# Filter and copy every 10th image
for file in files:
    print(os.path.join(r'D:\2024 Total Eclipse\frames_centered', file))
    centered_image = crop_image_center(os.path.join(r'D:\2024 Total Eclipse\frames_centered', file), 1200, 1200)
    # centered_image.show()
    centered_image.save(os.path.join(r'D:\2024 Total Eclipse\frames_shrunk', file))