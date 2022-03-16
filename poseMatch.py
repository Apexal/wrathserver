import cv2
import numpy as np
from turtle import pos
from PIL import Image, ImageDraw, ImageFilter

person="images\output-resized.png"
pose="poses\light_punch\light_punch_pose_frame_0.png"

imPerson=Image.open(person)
imPose=Image.open(pose)

#poseWidth, poseHeight = imPose.size
#personWidth, personHight = imPerson.size

imPose.paste(imPerson,(0,0),imPerson)
imPose.save("fit.png", quality=95)

image = cv2.imread(person)
print("person: "+str(np.sum(image == 0)))
print("total: "+str(np.sum(image)))
image = cv2.imread(pose)
print("###############")
print("pose: "+str(np.sum(image == 0)))
print("total: "+str(np.sum(image)))

imgaPose=imPose.convert("RGBA")
datas=imgaPose.getdata()

transparentCount=0
nontransparentCount=0
blackCount=0
for item in datas:
    if(item[0]==0 and item[1]==0 and item[2]==0):
        blackCount+=1
    if(item[3]==0):
        transparentCount+=1
    else:
        nontransparentCount+=1
print("transparent "+str(transparentCount))
print("nontransparent "+str(nontransparentCount))
print("real total "+str(nontransparentCount+transparentCount))
print("Black pixels "+str(blackCount))
print("###############")
image = cv2.imread("fit.png")
print("fit: "+str(np.sum(image == 0)))
print("total: "+str(np.sum(image)))
'''
pose
fit
person
'''
#count = cv2.countNonZero(image)
