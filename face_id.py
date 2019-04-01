#-*- coding:utf-8 -*-
import time
from face_recognition import load_image_file, face_encodings, face_distance
import cv2
import win32api, win32con
import os
import threading


# Global variables
flag = False  # if the face ID program finished
log_status = True # if person is lichaoqun

t0 = time.time()
cam = cv2.VideoCapture(0) # opencamera
print('Time for loading library is: ', time.time() - t0)


def face_ID():
	'''
	main program of face identificaiton to log in the system
	'''
	global flag, log_status
	threshold = 0.4
	count = 0
	
	# three chances for identify the face.
	for i in range(3):
		
		# read image from front camera
		ret, frame = cam.read()
		if not ret: 
			break

		# Save current image
		cv2.imwrite("./images/id_card_current.jpg", frame) 

		# Encoding refer image
		refer_image = load_image_file("./images/id_card_refer.jpg")
		refer_encodings = []
		for i in face_encodings(refer_image) :
			refer_encodings.append(i)
		
		# Encoding current image
		image_to_ID = load_image_file("./images/id_card_current.jpg")
		try:
			image_to_ID_encoding = face_encodings(image_to_ID)[0]
		except:
			if count == 2:
				flag = True
				log_status = False
				win32api.MessageBox(0, u'最终未识别到人脸，请重新登陆！', 'Face_ID', win32con.MB_ICONWARNING)
				break
			else:
				count = count + 1
				continue
		
		# Caculate the distance of two images
		face_distances = face_distance(refer_encodings, image_to_ID_encoding)
		
		# Compare the two images
		if face_distances < threshold:
			flag = True
			win32api.MessageBox(0, u'You are the owner of the computer，welcome to log in windows 10.', 'Face_ID', win32con.MB_OK)
			break
		elif face_distances >= threshold:
			if count == 2:
				flag = True
				log_status = False
				win32api.MessageBox(0, u'You are not the owner of this computer，system will lock after a few seconds!', 'Face_ID', win32con.MB_ICONWARNING)
				break
		else:
			pass
		# add the trying times
		count = count + 1
		time.sleep(0.1)

def sys_monitor():
	'''
	monitor the system status, once the face_id threading finished, exit the whole program
	'''
	global flag, log_status
	while True:
		if flag:
			time.sleep(2)
			cam.release()
			time.sleep(1)
			if log_status:
				pass
			else:
				os.system('rundll32.exe user32.dll,LockWorkStation')
			break
		else:
			pass
		time.sleep(0.5)

if __name__ == '__main__':
	t = threading.Thread(target=face_ID)

	# If the main program finished, the face_id program shall be finished!
	t.setDaemon(True) 

	# Start face_id threading
	t.start()

	# Monitor the program
	sys_monitor()

	

