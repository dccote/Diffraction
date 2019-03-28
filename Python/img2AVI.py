import cv2
import argparse
import os

# Obtained from Stackoverflow: 
# https://stackoverflow.com/questions/47342738/opencv-3-videowriter-inserting-an-extra-frames
# To install OpenCV, type "pip install opencv-python"
# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ext", "--extension", required=False, default='tiff', help="extension name. default is 'tiff'.")
ap.add_argument("-o", "--output", required=False, default='output.avi', help="output video file")
ap.add_argument("-i", "--input", required=False, default='.', help="input directory")
ap.add_argument("-s", "--show", action="store_true", help="show images as they are processed")
args = vars(ap.parse_args())

# Arguments
ext = args['extension']
output = args['output']
sourcePath = args['input']
showImages = args['show']
pwd = os.path.dirname(os.path.abspath(__file__))

images = []
allFiles = os.listdir(sourcePath)
for f in allFiles:
    if f.endswith(ext):
        images.append(f)
images.sort()

# Determine the width and height from the first image
image_path = os.path.join(sourcePath, images[0])
frame = cv2.imread(image_path)
if showImages:
    cv2.imshow('video',frame)

height, width, channels = frame.shape

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'DIB ') 
# use fourcc = 0 for uncompressed.

out = cv2.VideoWriter(output, 0, 20.0, (width, height))

for image in images:
    image_path = os.path.join(sourcePath, image)
    frame = cv2.imread(image_path)
    out.write(frame) # Write out frame to video

    if showImages:
        cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break

# Release everything if job is finished
out.release()
cv2.destroyAllWindows()

print(os.path.join(pwd, output))