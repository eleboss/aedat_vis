import os
import cv2
import datetime
import numpy as np
import argparse

def generate_video(image_folder, output_path, frame_rate):
    # Get the list of image files in the folder
    image_files = sorted(os.listdir(image_folder))
    print(image_files)
    image_paths = [os.path.join(image_folder, file) for file in image_files]

    init_ts = int(os.path.splitext(os.path.basename(image_paths[0]))[0])

    # Read the first image to get image dimensions
    first_image = cv2.imread(image_paths[0])
    height, width, _ = first_image.shape

    # Create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (width, height))
    prev_timestamp = None
    for image_path in image_paths:
        # Extract the timestamp from the file name
        filename = os.path.basename(image_path)
        # determine weather or not filename is animage
        if not filename.endswith(".png"):
            continue
        timestamp = int(os.path.splitext(filename)[0])

        # Convert the timestamp to a valid time format
        capture_time = datetime.datetime.fromtimestamp(timestamp / 1e6)  # Assuming the timestamp is in milliseconds

        print("Processing image:", filename)
        print("Capture time:", capture_time)

        image = cv2.imread(image_path)

        # Write the image to the video file
        video_writer.write(image)

        if prev_timestamp is not None:
            # Calculate the time difference between consecutive frames
            time_diff = (float(timestamp) - float(prev_timestamp))/1e6
            interpolation_num = np.floor(time_diff / (1/frame_rate)) - 1
            print(time_diff / (1/frame_rate),1/frame_rate)
            print("fr:",1/time_diff, "interval:", time_diff, "intepolrate:", interpolation_num)
            if interpolation_num > 0:
                for i in range(int(interpolation_num)):
                    video_writer.write(image)

        prev_timestamp = timestamp


    # Release the VideoWriter object
    # cv2.destroyAllWindows()
    video_writer.release()

    print("Video generation complete.", output_path)





if __name__ == '__main__':

    # write an argument
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the frames folder")
    parser.add_argument("video_name", help="output video name")

    args = parser.parse_args()

    out_path = args.input

    frame_rate = 30  # Set the desired frame rate
    generate_video(out_path, os.path.join(out_path, args.video_name), frame_rate)