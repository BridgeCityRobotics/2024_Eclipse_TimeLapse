# 2024_Eclipse_TimeLapse
Super fast and lazy workflow for converting my DwarfII Timelapse into a shorter and more centered video

https://github.com/BridgeCityRobotics/2024_Eclipse_TimeLapse/blob/main/20240408_Partial_Eclipse.mp4

### Workflow:
1. h264_to_Frames.py
2. reduce_frames.py
3. center_frames.py
4. crop_to_center.py
5. make_video.py

### To Do:
* One script obviously
* Automatic removal of black and unusable frames
* Better centering - instead of largest circle finding use cirle with color threshold
* File clean up