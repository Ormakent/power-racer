import cv2
import numpy as np

#Threshold for each template
threshold=[0.99,0.99,0.99,0.99,0.99,0.99]
#Reads the main image to be matched
img_bgr= cv2.imread('laptwo.jpg')
#Converts it to grayscale
img_gray=cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

#Read the template image for laps 0-5
templates = [ cv2.imread('lap'+str(i)+'.jpg',cv2.IMREAD_GRAYSCALE) for i in range(0,6) ]

#Stores the width and height of templates
w1,h1=templates[0].shape[::-1]
w2,h2=templates[1].shape[::-1]
w3,h3=templates[2].shape[::-1]
w4,h4=templates[3].shape[::-1]
w5,h5=templates[4].shape[::-1]
w6,h6=templates[5].shape[::-1]

#Peforms match operations of each template onto the main image
result1=cv2.matchTemplate(img_gray,templates[0],cv2.TM_CCOEFF_NORMED)
result2=cv2.matchTemplate(img_gray,templates[1],cv2.TM_CCOEFF_NORMED)
result3=cv2.matchTemplate(img_gray,templates[2],cv2.TM_CCOEFF_NORMED)
result4=cv2.matchTemplate(img_gray,templates[3],cv2.TM_CCOEFF_NORMED)
result5=cv2.matchTemplate(img_gray,templates[4],cv2.TM_CCOEFF_NORMED)
result6=cv2.matchTemplate(img_gray,templates[5],cv2.TM_CCOEFF_NORMED)

#Stores coordinates of matching area
#If not empty, then image has been matched
loc1=np.where(result1>=threshold[0])
if loc1[1].size != 0:
    lapnumber = 0
loc2=np.where(result2>=threshold[1])
if loc2[1].size != 0:
    lapnumber = 1
loc3=np.where(result3>=threshold[2])
if loc3[1].size != 0:
    lapnumber = 2
loc4=np.where(result4>=threshold[3])
if loc4[1].size != 0:
    lapnumber = 3
loc5=np.where(result5>=threshold[4])
if loc5[1].size != 0:
    lapnumber = 4
loc6=np.where(result6>=threshold[5])
if loc6[1].size != 0:
    lapnumber = 5

#Draws a rectangle around matched region
for pt1 in zip(*loc1[::-1]):
    cv2.rectangle(img_bgr,pt1,(pt1[0]+w1,pt1[1]+h1),(0,255,0),2)
for pt2 in zip(*loc2[::-1]):
    cv2.rectangle(img_bgr,pt2,(pt2[0]+w2,pt2[1]+h2),(255,0,0),2)
for pt3 in zip(*loc3[::-1]):
    cv2.rectangle(img_bgr,pt3,(pt3[0]+w3,pt3[1]+h3),(0,0,255),2)
for pt4 in zip(*loc4[::-1]):
    cv2.rectangle(img_bgr,pt4,(pt4[0]+w4,pt4[1]+h4),(0,0,255),2)
for pt5 in zip(*loc5[::-1]):
    cv2.rectangle(img_bgr,pt5,(pt5[0]+w5,pt5[1]+h5),(0,0,255),2)
for pt6 in zip(*loc6[::-1]):
    cv2.rectangle(img_bgr,pt6,(pt6[0]+w6,pt6[1]+h6),(0,0,255),2)

#Outputs image and lap number
cv2.imshow("image",img_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(lapnumber)
