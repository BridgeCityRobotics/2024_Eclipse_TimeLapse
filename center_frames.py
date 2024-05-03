from PIL import Image, ImageOps
import numpy as np
import cv2
import os


def center_eclipse_in_image_old(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold or edge detection to highlight the eclipse
    # These parameters may need adjustment based on the image characteristics
    _, thresholded = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None  # No contours found

    # Assuming the largest contour is the eclipse
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None  # Avoid division by zero

    # Calculate the centroid of the eclipse
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Calculate the new box to center around the eclipse
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    width, height = image_pil.size
    new_left = max(0, cx - width // 2)
    new_upper = max(0, cy - height // 2)
    new_right = new_left + width
    new_lower = new_upper + height

    # Crop the image to center on the eclipse
    image_cropped = image_pil.crop((new_left, new_upper, new_right, new_lower))

    return image_cropped
    

def center_eclipse_in_image_old2(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance the contrast of the image
    contrast_enhanced = cv2.equalizeHist(gray)

    # Use adaptive thresholding to accommodate varying lighting conditions
    thresh = cv2.adaptiveThreshold(contrast_enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None  # No contours found, unable to center

    # Assuming the largest contour corresponds to the eclipse
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None  # Avoid division by zero

    # Calculate the centroid of the eclipse
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Center the image around this centroid
    width, height = gray.shape[::-1]
    x_shift = width // 2 - cx
    y_shift = height // 2 - cy

    # Translate the image to center the eclipse
    M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
    centered_img = cv2.warpAffine(image, M, (width, height))

    return Image.fromarray(cv2.cvtColor(centered_img, cv2.COLOR_BGR2RGB))
    
def center_eclipse_in_image(image_path):
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
    if M["m00"] != 0:
        # Calculate the centroid of the contour
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        # If the contour is a line (m00 == 0), then use the bounding rectangle
        x, y, w, h = cv2.boundingRect(max_contour)
        cX, cY = x + w // 2, y + h // 2

    # Calculate the distance to move the centroid of the eclipse to the center of the image
    rows, cols = gray_image.shape
    shift_x = cols // 2 - cX
    shift_y = rows // 2 - cY

    # Create the transformation matrix for the translation
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])

    # Perform the translation
    shifted = cv2.warpAffine(image, M, (cols, rows))

    # Convert the result to a PIL Image for better compatibility
    centered_image = Image.fromarray(shifted)

    return Image.fromarray(cv2.cvtColor(np.array(centered_image), cv2.COLOR_BGR2RGB))



source_folder = r'E:\2024 Total Eclipse\frames_reduced'
destination_folder = r'E:\2024 Total Eclipse\frames_centered'

# List all files in the source folder
files = os.listdir(source_folder)

# Filter and copy every 10th image
for file in files:
    print(os.path.join(r'E:\2024 Total Eclipse\frames_reduced', file))
    centered_image = center_eclipse_in_image(os.path.join(r'E:\2024 Total Eclipse\frames_reduced', file))
    # centered_image.show()
    centered_image.save(os.path.join(r'E:\2024 Total Eclipse\frames_centered', file))

