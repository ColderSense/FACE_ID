# FACE_ID
Face unlock using python on windows10.
There are three chances to capture your face by front camera, once there is no face detected or the
face is not your face ,windows10 system will lock after a few seconds.

# Install related python library
When install face_recognition library, there may be some error, please install cmake and dlib first.
refer web page: 
https://www.jianshu.com/p/eb4bec6459c7

# Requirements
face_recognition
opencv-python
pywin32

pip install -r requirements.txt

# Run the main program.
replace id_card_refer.jpg in directory "images" with your face image, then run the scripts.

python face_id.py


	
	

