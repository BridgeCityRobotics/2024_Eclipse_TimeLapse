import cv2

# Open the video file
cap = cv2.VideoCapture('DWARF_TELE_TL_2024-04-08-10-06-11-882.h264')

# Initialize a counter
frame_count = 0

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Save frame as JPEG file
        cv2.imwrite(f'./frames/frame_{frame_count}.jpg', frame)
        frame_count += 1
    else:
        break

# When everything done, release the video capture object
cap.release()

# Close all the frames
cv2.destroyAllWindows()
