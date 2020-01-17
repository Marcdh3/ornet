'''
This script serves as a helper to the track_cells script by taking the 
segmentation masks generated by it and creating individual videos of
each cell.
'''
# Author: Marcus Hill

import os
import argparse

import cv2
import imageio
import numpy as np
from tqdm import tqdm

def extract_cells(vid_path, masks_path, output_path, show_vid=False):
    '''
    Each individual cell in a video is extracted into it's own video.

    Parameters
    ----------
    vid_path: String
        Path to the input video.
    masks_path: String
        Path to the segmentation masks for the input video.
    output_path: String
        Path to the directory to save the individual videos.
    show_vid: boolean
        Flag to show video while extracting cells.

    Returns
    ----------
    NoneType object
    '''

    masks = np.load(masks_path)
    segments = len(np.unique(masks[0])) - 1

    writers = []
    vid_name = os.path.split(vid_path)[1].split('.')[0]
    os.makedirs(output_path, exist_ok=True)
    reader = imageio.get_reader(vid_path)

    for i in range(segments):
        writers.append(cv2.VideoWriter(
            os.path.join(
                str(output_path), str(vid_name) + '_' + str(i + 1) + '.avi'),
            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
            reader.get_meta_data()['fps'], (masks.shape[1], masks.shape[2])))

    progress_bar = tqdm(total=reader.count_frames())
    progress_bar.set_description('  Extracting cells')
    for i, frame in enumerate(reader):
        mask = cv2.cvtColor(masks[i], cv2.COLOR_GRAY2BGR)
        for j in range(segments):
            output = np.ma.masked_where(mask != j + 1, frame)
            output = np.ma.filled(output, 0)
            writers[j].write(output)

        if show_vid:
            cv2.putText(frame, 'Frame number: ' + str(i), (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
            cv2.imshow("Original Video", frame)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                exit(0)
        progress_bar.update()

    progress_bar.close()
    if show_vid:
        cv2.destroyAllWindows()

    reader.close()
    for writer in writers:
        writer.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reads in segmentation masks and the original video to seperate each cell into their own video.")
    parser.add_argument('-i', '--input', required=True,
                        help="Path to original video")
    parser.add_argument('-m', '--masks', required=True,
                        help="Path to segmentation masks (.npy)")
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help="Path to output directory. Default cwd")
    args = vars(parser.parse_args())
    extract_cells(args['input'], args['masks'], args['output'])
