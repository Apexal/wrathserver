import cv2
from imageio import save
import numpy as np
from turtle import pos
from PIL import Image, ImageDraw, ImageFilter
import os

def turnWhite(imageName, newName):
    img = Image.open(imageName+'.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[3]!=0:
            newData.append((255, 255, 255, 255))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(newName+".png", "PNG") 

def countBlackPixel(imageName):
    img= Image.open(imageName)
    img=img.convert("RGBA")
    datas=img.getdata()

    blackCount=0
    for item in datas:
        if(item[0]==0 and item[1]==0 and item[2]==0 and item[3]>0):
            blackCount+=1
    img.close()   
    return blackCount   


'''
Given 2 400x400 Pixel pictures the move will be masked onto the move
'''
def personPoseValid(person, pose):
    #person="images\output-resized.png"
    #pose="poses\light_punch\light_punch_pose_frame_0.png"

    imPerson=Image.open(person)
    imPose=Image.open(pose)

    #imPerson2=imPerson.copy()
    temp=imPose.copy()
    temp.paste(imPerson,(0,0),imPerson)
    temp.save("fit.png", quality=95)

    #image = cv2.imread(person)
    #print("person: "+str(np.sum(image == 0)))
    #print("total: "+str(np.sum(image)))

    #add process to move picture to improve accuracy/allow it to pass
    print("person")
    blackPixels_on_person=countBlackPixel("test.png")
    print(blackPixels_on_person)
    print("pose")
    blackPixels_on_pose=countBlackPixel(pose)
    print(blackPixels_on_pose)
    print("fit")
    blackPixels_on_fit=countBlackPixel("fit.png")
    print(blackPixels_on_fit-blackPixels_on_person)
    print((blackPixels_on_fit-blackPixels_on_person)/blackPixels_on_pose)
    returnPixelValue=temp.convert("RGBA").getdata()
    os.remove("fit.png")


    if((blackPixels_on_fit-blackPixels_on_person)/blackPixels_on_pose<.35):
        #print("yes")
        #print(returnPixelValue[0])
        return (blackPixels_on_fit-blackPixels_on_person)/blackPixels_on_pose, returnPixelValue
    else:
        print("no")
        return -1, []

personPoseValid("images\output-resized.png","poses\light_punch\light_punch_pose_frame_0.png")
#image = cv2.imread(pose)
#print("pose: "+str(np.sum(image == 0)))
#print("total: "+str(np.sum(image)))
'''
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
'''
#print("transparent "+str(transparentCount))
#print("nontransparent "+str(nontransparentCount))
#print("real total "+str(nontransparentCount+transparentCount))
#print("Black pixels "+str(blackCount))
#print("###############")

#image = cv2.imread("fit.png")
#print("fit: "+str(np.sum(image == 0)))
#print("total: "+str(np.sum(image)))
'''
pose
fit
person
'''



#(Left,Top,Right,Bottom)
'''imPerson2=imPerson2.crop((5,5,395,395))
imPerson2=imPerson2.resize((400,400))
imPerson2=imPerson2.crop((5,5,395,395))
imPerson2=imPerson2.resize((400,400))
imPerson2=imPerson2.crop((5,5,395,395))
imPerson2=imPerson2.resize((400,400))'''


#imPerson2.save("test.png",quality=95)
#turnWhite("test","testW")

#whiteChar=Image.open("testW.png")

#current=Image.open("green.png")
#greenControl=current.copy()

#current.paste(whiteChar,(0,0),imPose)
#current.save("fit2.png", quality=95)
#current.save("fit3.png", quality=95)

"""
current=greenControl
current.save("fit2.png", quality=95)
"""

#print(countBlackPixel("fit2"))
#direction=0
#lastCount=countBlackPixel("fit2")

#check if or image is completely in shadow
#(Left,Top,Right,Bottom)
#stuck=0
'''while(countBlackPixel("fit3")>0):
    print(countBlackPixel("fit3"))
    imgKeep=current.copy()
    personKeep=imPerson2.copy()
    current=greenControl
    if(direction==0):
        #Top
        direction+=1
        whiteChar=whiteChar.crop((0,2,400,400))
        whiteChar=whiteChar.resize((400,400))
        imPerson2=imPerson2.crop((0,2,400,400))
        imPerson2=imPerson2.resize((400,400))
        current.paste(whiteChar,(0,0),imPose)
        current.save("fitNew.png",quality=95)
    elif(direction==1):
        #Right
        direction+=1
        whiteChar=whiteChar.crop((0,0,398,400))
        whiteChar=whiteChar.resize((400,400))
        imPerson2=imPerson2.crop((0,0,398,400))
        imPerson2=imPerson2.resize((400,400))
        current.paste(whiteChar,(0,0),imPose)
        current.save("fitNew.png",quality=95)
    elif(direction==2):
        #Bottom
        direction+=1
        whiteChar=whiteChar.crop((0,0,400,398))
        whiteChar=whiteChar.resize((400,400))
        imPerson2=imPerson2.crop((0,0,398,400))
        imPerson2=imPerson2.resize((400,400))
        current.paste(whiteChar,(0,0),imPose)
        current.save("fitNew.png",quality=95)
    else:
        #Left
        direction=0
        whiteChar=whiteChar.crop((2,0,400,400))
        whiteChar=whiteChar.resize((400,400))
        imPerson2=imPerson2.crop((0,0,398,400))
        imPerson2=imPerson2.resize((400,400))
        current.paste(whiteChar,(0,0),imPose)
        current.save("fitNew.png",quality=95)
    
    if(countBlackPixel("fit3")>countBlackPixel("fitNew")):
        current.save("fit3.png",quality=95)
        stuck=0
    else:
        current=imgKeep
        imPerson2=personKeep
        stuck+=1
        if(stuck>=5):
            break
    
current=greenControl
current.paste(imPerson2,(0,0),imPose)
current.save("fitNew.png",quality=95)'''





