import argparse
import os.path as osp
import cv2 as cv

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Filename of the image to display. It will be converted to full path: data/noshadow/filename and data/mask/filename.")
parser.add_argument("-o", "--output", type=bool, default=False, help="Display output/demo.jpg or not.")

if __name__ == '__main__':
	args = parser.parse_args()
	filename = args.filename
	output = args.output

	input_image_filename = osp.join('data', 'noshadow', filename)
	if not osp.exists(input_image_filename):
		print("[ERROR] No file %s." % input_image_filename)
		exit(1)
	input_image = cv.imread(input_image_filename, cv.IMREAD_UNCHANGED)
	if input_image is None:
		print("[ERROR] %s is not an image." % input_image_filename)
		exit(1)
	input_image = cv.resize(input_image, (400, 300), cv.INTER_CUBIC)
	cv.namedWindow('InputImage', cv.WINDOW_AUTOSIZE)
	cv.imshow('InputImage', input_image)
	cv.moveWindow('InputImage', 0, 0)

	input_mask_filename = osp.join('data', 'mask', filename)
	if not osp.exists(input_mask_filename):
		print("[ERROR] No file %s." % input_mask_filename)
		exit(1)
	input_mask = cv.imread(input_mask_filename, cv.IMREAD_UNCHANGED)
	if input_mask is None:
		print("[ERROR] %s is not an image." % input_mask_filename)
		exit(1)
	input_mask = cv.resize(input_mask, (400, 300), cv.INTER_CUBIC)
	cv.namedWindow('InputMask', cv.WINDOW_AUTOSIZE)
	cv.imshow('InputMask', input_mask)
	cv.moveWindow('InputMask', 400, 0)

	if output:
		output_image_filename = osp.join('output', 'demo.jpg')
		if not osp.exists(output_image_filename):
			print("[ERROR] No file %s." % output_image_filename)
			exit(1)
		output_image = cv.imread(output_image_filename, cv.IMREAD_UNCHANGED)
		if output_image is None:
			print("[ERROR] %s is not an image." % output_image_filename)
			exit(1)
		output_image = cv.resize(output_image, (400, 300), cv.INTER_CUBIC)
		cv.namedWindow('OutputImage', cv.WINDOW_AUTOSIZE)
		cv.imshow('OutputImage', output_image)
		cv.moveWindow('OutputImage', 800, 0)

	cv.waitKey(0)
	cv.destroyAllWindows()

