import os
import shutil

# Define the source and destination folders
source_folder = r'E:\2024 Total Eclipse\frames'
destination_folder = r'E:\2024 Total Eclipse\frames_reduced'

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# List all files in the source folder
files = os.listdir(source_folder)

# Filter and copy every 10th image
for file in files:
    if file.startswith('frame_'):
        # Extract the frame number from the filename
        frame_number = int(file.split('_')[1].split('.')[0])

        # Check if the frame number is a multiple of 10
        if frame_number % 10 == 0:
            # Construct full file paths
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)

            # copy the file
            shutil.copy(source_path, destination_path)
            print(f'Copied {file} to {destination_folder}')
