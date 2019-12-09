'''
Applies median normalization to an input video, and saves the output (.avi).'
'''
import os
import argparse

import cv2
import imageio
import numpy as np

def median_normalize(vid_name, vid_path, out_path):
	'''
	Parameters
	----------
	vid_name: String
		name for the output video
	vid_path: String
		path to the input video
	out_path: String
		path to the directory to save the ouptut video

	Returns
	----------
	NoneType object
	'''

	medians = []
	reader = imageio.get_reader(vid_path)
	for frame in reader:
		frame_array = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
		flat_frame = frame_array.flatten()
		flat_frame[flat_frame > 0]
		medians.append(np.median(flat_frame))

	medians = np.array(medians)
	max_median = np.max(medians)
	adjusted_medians = medians - max_median

	reader = imageio.get_reader(vid_path)
	output = os.path.join(out_path, vid_name + '.avi')
	fps = reader.get_meta_data()['fps']
	size = reader.get_meta_data()['size']
	writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
		fps, size)
	for i, frame in enumerate(reader):
		frame_array = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
		flat_frame = frame_array.flatten()
		out_frame = [pixel + adjusted_medians[i] if pixel != 0 else 0 for pixel in flat_frame]
		out_frame = np.array(out_frame, dtype=np.uint8).reshape(size)
		color_img = cv2.cvtColor(out_frame, cv2.COLOR_GRAY2BGR)
		writer.write(color_img)

	reader.close()
	writer.release()

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(
		description='Applies median normalization to an input video,' +
			' and saves the output (.avi)')
	parser.add_argument('-i', '--input', required=True, help='Input video path')
	parser.add_argument('-o', '--output', required=True, help='Output video path')
	args = vars(parser.parse_args())

	vid_name = os.path.split(args['input'])[1].split('.')[0] + '_normalized'
	median_normalize(vid_name, args['input'], args['output'])
