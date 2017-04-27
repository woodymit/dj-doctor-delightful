from sensor_interface import SensorInterface as SI
import cv2
import numpy as np

def capture_finger_coordinates(sensor):
	# set up video writers and blob detector
	rows, cols = 46, 72 #magic numbers but these work for the synaptic board
	fourcc = cv2.cv.CV_FOURCC(*'XVID')
	out_norm = cv2.VideoWriter('vids/norm.avi',fourcc, 10, (cols,rows))
	out_keypoints = cv2.VideoWriter('vids/keypoints.avi',fourcc, 10, (cols,rows))

	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = 20
	detector = cv2.SimpleBlobDetector(params)

	first_image = True
	image_max_val = 0
	image_min_val = 4095

	cv2.namedWindow("")
	while True:
		if cv2.waitKey(1) & 0xFF == ord('q'):
			# clean up and exit if q is pressed
			out_norm.release()
			out_keypoints.release()
			cv2.destroyAllWindows()
			for i in range(5):
				cv2.waitKey(1)
			raise StopIteration

		image_data_sequence = sensor.getAllImages()
		images = map(lambda imageData: np.array(imageData["image"]), image_data_sequence)
		times = map(lambda imageData: imageData["timeStamp"], image_data_sequence)

		if images:
			if first_image:
				baseline_image = images[0]
				first_image = False

			baselined_images = images - baseline_image
			if np.max(baselined_images) > image_max_val:
				image_max_val = np.max(baselined_images)
			if np.min(baselined_images) < image_min_val:
				image_min_val = np.min(baselined_images)

			# normalize images
			if image_max_val - image_min_val != 0:
				normalized_images = (baselined_images-image_min_val)/float(image_max_val-image_min_val)*255
			else:
				normalized_images = np.ones(images[0].shape)*127 #make it medium gray if there is no variation
			# convert to correct format
			normalized_images = normalized_images.astype(np.uint8)
			normalized_images = map(lambda image: cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), normalized_images)

			# do detection
			keypoint_centers = []
			for image in normalized_images:
				keypoints = detector.detect(image)
				keypoint_centers.append(map(lambda k: k.pt, keypoints))
				im_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255))

				out_norm.write(image)
				out_keypoints.write(im_keypoints)

			yield keypoint_centers
	

sensor = SI()
try:
	sensor.connect()
except:
	print "Error connecting to sensor"
	raise

sensor_iterator = capture_finger_coordinates(sensor)
while True:
	keypoint_centers = sensor_iterator.next()
	print keypoint_centers