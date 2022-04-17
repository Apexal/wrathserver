from errno import EEXIST
from opcode import opname
from tkinter import E
import cv2
import mediapipe as mp
import numpy as np
import math
import json

# variables 
CEF_COUNTER =0
TOTAL_BLINKS =0
# constants
CLOSED_EYES_FRAME =2

# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  

map_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# camera object 
camera = cv2.VideoCapture(0)
# landmark detection function
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
def landmarksDetection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    # list[(x,y), (x,y)....]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv2.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]

    # returning the list of tuples for each landmarks 
    return mesh_coord

# Euclaidean distance 
def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

# Blinking Ratio
def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)
    if(rvDistance==0 or lvDistance==0):
        return -1
    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2
    return ratio 

stage = None
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
	with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:
		# starting Video loop here.
		while cap.isOpened():
			
			ret, frame = cap.read() # getting frame from camera 

			if not ret: 
				break # no more frames break
			#  resizing frame
			image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			image.flags.writeable = False
		
			# Make detection
			results = face_mesh.process(image)
			pose_results = pose.process(image)
		
			# Recolor back to BGR
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

			if results.multi_face_landmarks:
				mesh_coords = landmarksDetection(image, results, False)
				#print(mesh_coords)
				ratio = blinkRatio(image, mesh_coords, RIGHT_EYE, LEFT_EYE)
				if ratio >5.5:
					CEF_COUNTER +=1
				else:
					if CEF_COUNTER>CLOSED_EYES_FRAME:
						TOTAL_BLINKS +=1
						CEF_COUNTER =0
			try:
				landmarks = pose_results.pose_landmarks.landmark

				shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
				shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
				elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
				wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
				elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
				wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
				hipR = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
				kneeR = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
				ankleR = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
				hipL = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
				kneeL = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
				ankleL = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

				angleInfo=[]
				angleValues=[]
				angle1 = calculate_angle(shoulderR, elbowL, wristL)
				angle1Info=["PoseLandmark.RIGHT_SHOULDER","PoseLandmark.LEFT_ELBOW","PoseLandmark.LEFT_WRIST"]
				angle2 = calculate_angle(shoulderR, elbowR, wristR)
				angle2Info=["PoseLandmark.RIGHT_SHOULDER","PoseLandmark.RIGHT_ELBOW","PoseLandmark.RIGHT_WRIST"]
				angle3 = calculate_angle(shoulderL, elbowL, wristL)
				angle3Info=["PoseLandmark.LEFT_SHOULDER","PoseLandmark.LEFT_ELBOW","PoseLandmark.LEFT_WRIST"]
				angle4 = calculate_angle(ankleL, kneeL, hipL)
				angle4Info=["PoseLandmark.LEFT_ANKLE","PoseLandmark.LEFT_KNEE","PoseLandmark.LEFT_HIP"]
				angle5 = calculate_angle(ankleR, kneeR, hipR)
				angle5Info=["PoseLandmark.RIGHT_ANKLE","PoseLandmark.RIGHT_KNEE","PoseLandmark.RIGHT_HIP"]
				angle6 = calculate_angle(shoulderL, elbowR, wristR)
				angle6Info=["PoseLandmark.LEFT_SHOULDER","PoseLandmark.RIGHT_ELBOW","PoseLandmark.RIGHT_WRIST"]
				angle7 = calculate_angle(kneeR, hipR, shoulderR)
				angle7Info=["PoseLandmark.RIGHT_KNEE","PoseLandmark.RIGHT_HIP","PoseLandmark.RIGHT_SHOULDER"]
				angle8 = calculate_angle(kneeL, hipL, shoulderL)
				angle8Info=["PoseLandmark.LEFT_KNEE","PoseLandmark.LEFT_HIP","PoseLandmark.LEFT_SHOULDER"]
				
				angleInfo.append(angle1Info)
				angleInfo.append(angle2Info)
				angleInfo.append(angle3Info)
				angleInfo.append(angle4Info)
				angleInfo.append(angle5Info)
				angleInfo.append(angle6Info)
				angleInfo.append(angle7Info)
				angleInfo.append(angle8Info)

				angleValues.append(angle1)
				angleValues.append(angle2)
				angleValues.append(angle3)
				angleValues.append(angle4)
				angleValues.append(angle5)
				angleValues.append(angle6)
				angleValues.append(angle7)
				angleValues.append(angle8)


				if TOTAL_BLINKS>0:
					#print(angle1)
					poseInfo=[]
					for i in range(len(angleValues)):
						h={}
						h["poseIndex1"]=angleInfo[i][0]
						h["poseIndex2"]=angleInfo[i][1]
						h["poseIndex3"]=angleInfo[i][2]
						if(angleValues[i]+8>180):
							h["angleMax"]=180
						else:
							h["angleMax"]=angleValues[i]+8
						h["angleMin"]=abs(angleValues[i]-8)
						poseInfo.append(h)
					print(poseInfo)
					print(angle2)
					final= json.dumps(poseInfo, indent=2)
					with open("newPose.txt","w") as f:
						f.write(final)
					break
					

			except:
				pass

			cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
			cv2.putText(image, 'STAGE', (5,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
			cv2.putText(image, stage, 
                        (5,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

			
			cv2.putText(image, str(TOTAL_BLINKS),(60,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
			cv2.imshow('IMG', image)
			key = cv2.waitKey(2)
			if key==ord('q') or key ==ord('Q'):
				break
	cv2.destroyAllWindows()
	camera.release()