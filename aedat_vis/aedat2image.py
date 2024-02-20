# this program will open the aedat and create a folder and save events and image to it
import numpy as np
import cv2
import os
import dv_processing as dv
import argparse


if __name__ == '__main__':

    # write an argument
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the aedat file")
    parser.add_argument("output", help="folder to save image file")

    args = parser.parse_args()

    mother_path = args.output
    EGAE_path = os.path.join(args.input) 


    # read the egae shimae nae simutinuously , determine the clip time, apply the clip time to all other file.
    egae_result_dir = os.path.join(mother_path)
    if not os.path.exists(egae_result_dir):
        os.makedirs(egae_result_dir)


    egae_ev_reader = dv.io.MonoCameraRecording(EGAE_path)

    store = dv.EventStore()

    resolution = None
    print(f"loading events from {EGAE_path}...")
    while egae_ev_reader.isRunning():
        events = egae_ev_reader.getNextEventBatch()
        resolution = egae_ev_reader.getEventResolution()
        if events is not None:
            # Print received packet time range
            store.add(events)



    event_image = np.ones((resolution[1], resolution[0], 3), dtype=np.uint8) * 255  # White background
    event_frame_rate = 30
    time_interval = 1e6/event_frame_rate
    prev_save_time = 0
    for ev in store:
        # print(f"Sliced event [{ev.timestamp()}, {ev.x()}, {ev.y()}, {ev.polarity()}]")

        # cast polarity to 1 -1
        if ev.polarity():
            event_image[ev.y(), ev.x()] = [0, 0, 255]  # Red for positive polarity
        else:
            event_image[ev.y(), ev.x()] = [255, 0, 0]  # Blue for negative polarity

        # save and reset the event image for a give frame rate
        if ev.timestamp() > prev_save_time + time_interval:
            prev_save_time = ev.timestamp()
            print("saving event image: ", ev.timestamp())
            cv2.imwrite(os.path.join(mother_path, str(ev.timestamp())+".png"), event_image)
            event_image = np.ones((resolution[1], resolution[0], 3), dtype=np.uint8) * 255  # Reset to white background