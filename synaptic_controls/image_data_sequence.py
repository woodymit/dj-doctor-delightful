import time
import cv2
import numpy as np

class ImageDataSequence:
	def __init__(self, image_data_sequence):
		self.image_data_sequence = image_data_sequence

	def get_images(self):
		"""
		Returns normalized, 3-channel list of images formatted for opencv (uint8)
		"""
		images = map(lambda imageData: np.array(imageData["image"]), self.image_data_sequence)

		if not images:
			return []

		baselined_images = images - images[0]
		image_max_val = np.max(baselined_images)
		image_min_val = np.min(baselined_images)
		if image_max_val - image_min_val != 0:
			normalized_images = (baselined_images-image_min_val)/float(image_max_val-image_min_val)*255
		else:
			normalized_images = np.ones(images[0].shape)*127 #make it medium gray if there is no variation

		normalized_images = normalized_images.astype(np.uint8)
		normalized_images = map(lambda image: cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), normalized_images)
		return normalized_images

	def get_image_times(self):
		"""
		Returns timestamps of images
		"""
		return map(lambda imageData: imageData["timeStamp"], self.image_data_sequence)

	def show_images(self):
		"""
		Shows images with approximately same time as recorded
		"""
		t=time.time()
		for i,image in enumerate(self.get_images()):
			cv2.imshow("window",image)
			if i<len(self.get_images())-1:
				delay = self.get_image_times()[i+1] - self.get_image_times()[i]
				delay /= 1000 #convert from microseconds to milliseconds
			else:
				delay = 1
			cv2.waitKey(delay)
		cv2.destroyAllWindows()

		# to close window, have to send waitKey's to flush out messages
		for i in range(5):
			cv2.waitKey(1)

	def save_to_file(self,filename):
		"""
		Save images as a video to file

		Args:
			filename: filename ending in video extension (.avi)
		"""
		img = self.get_images()[0]
		rows = img.shape[0]
		cols = img.shape[1]
		total_time = (self.get_image_times()[-1] - self.get_image_times()[0])/1000000; #convert from microseconds to seconds
		frame_rate = len(self.get_images())/total_time

		fourcc = cv2.cv.CV_FOURCC(*'XVID')
		out = cv2.VideoWriter(filename,fourcc, frame_rate, (cols,rows))
		print out.isOpened()

		for i,image in enumerate(self.get_images()):
			cv2.imshow("frame",image)
			out.write(image)
		out.release()
		cv2.destroyAllWindows()
