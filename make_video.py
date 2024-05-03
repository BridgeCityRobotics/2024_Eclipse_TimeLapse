import cv2
import os
import re
from vidstab import VidStab

def make_video(images_folder, output_video_file, fps=30, size=None):
    # Get all image files from the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Sort files based on the numerical value X in 'frame_X.jpg'
    image_files.sort(key=lambda f: int(re.search(r'(\d+)', f).group()))

    # Determine the size of images if not provided
    if not size:
        first_image = cv2.imread(os.path.join(images_folder, image_files[0]))
        height, width, layers = first_image.shape
        size = (width, height)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec used to create video, 'mp4v' is a good choice for .mp4 files
    video = cv2.VideoWriter(output_video_file, fourcc, fps, size)
    
    for image in image_files:
        img_path = os.path.join(images_folder, image)
        img = cv2.imread(img_path)
        video.write(img)
    
    video.release()
    print(f'Video saved as {output_video_file}')

# Usage
images_folder = r'E:\2024 Total Eclipse\frames_shrunk'  # Replace with the path to your image folder
output_video_file = 'output_video.mp4'  # Output video file
fps = 30  # Frames per second

make_video(images_folder, output_video_file, fps)

# Stabilize the video
print("Now Stabilizing...")
stabilizer = VidStab()
stabilizer.stabilize(input_path=output_video_file, output_path='stabilized_' + output_video_file)
