'''be carefull that the readlines starts indizis start at 0
   remove the \n at the end of each element
   get for each objct class a list e.g car,truck
   in each there is the specific number: corrossponding to the specific object

    """Get current position in bounding box format `(min x, miny, max x,
        max y)`.
    fifth element is the id and 6th is the index to the object itself(car, truck)
   '''

import json
import cv2
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
import webcolors
import argparse
cars ={}
topcars={}
carslen={}
truck={}
# loads class name from a file


parser = argparse.ArgumentParser(description='Get the video path to the ground truth label video.')
parser.add_argument('--input', help='input path')
parser.add_argument('--folder', help='folder path where we save the cutframes.')

args = parser.parse_args()

###############################################################
'''One problem we have is that the picked color is not exactly the one in the clas list.
So we have to find the nearest color to the picked one. We do that by subtracting each RGB Value from each other'''
###############################################################
def finding_nearest_color(color):
    class_list=json.load(open('class_list_rgb.json'))
    diff=255*3
    diff_color=(255,255,255)
    for keysss in class_list.keys():
        #convert string to rgb
        #check the case that the string doesnt have 9 characters because the integer started with a 0
        keysss=str(keysss)
        missingzereos= 9-len(keysss)
        if missingzereos > 0 :
            for i in range(missingzereos):
                keysss= '0' + keysss
        
        key_color=[]
        
        key_color.append(int(keysss[0:3]))
        key_color.append(int(keysss[3:6]))
        key_color.append(int(keysss[6:9]))

        #compare the key color with the color and find the difference

        temp= abs(key_color[0]-color[0])+abs(key_color[1]-color[1])+abs(key_color[2]-color[2])
        if temp <= diff:
            diff=temp
            diff_color=key_color


    return diff_color,diff

###############################################################
'''The Trackinfo.txt has the data from the Track as a txt file embedded. Each line Contains the information about one Frame. EG line 221 contains infortion about frame 221
 In the Line a 6-tupel is saved as follwing the first 4 contain the objects location, the fifth contains the individual tracking number and the sixth identifies the object class(e.g car).
 the trackinfo.txt is created in the object_tracker.py file. it only contains information about the class number 2: (cars) bc the main focus of the project and the dataset is about tracking 
 cars and  Track_only = ["car","truck","bus","bicycle","motorbike"]
 .
 the classes can be found in the YOLO_COCO_CLASSES with the corrosponding numerical index( the file can be found in the model_data/coco/ folder.'''
 ##############################################################

with open('trackinfo.txt') as f:
    content = f.readlines()

##############################################################
''' we now go through each frame and evaluate it.'''
############################################################
frame=1
for ele in content:

    #ele contains all objects in one frame, each described in a 6th tupel, we now evalueate each 6th tupel.
    ele.strip('\n')
    jsonele=json.loads(ele)
    
    for ele2 in jsonele:
        
        '''single objects in one particaluar frame'''
        '''check the last element for the id'''
        
        coordinates=ele2[0:4]
        coordinates.append(frame)
        objectinstance=ele2[4]
        objectid=ele2[5]
        #check if car bc car has the object id 2 in the coco.names file:
        
        if objectid==2:
            if objectinstance in cars.keys(): 
                
                '''side case when there is only one list present
                if len(cars[objectinstance])==5:
                    
                    temp=[]
                    temp.append(cars[objectinstance])
                    temp.append(coordinates)
                    cars[objectinstance]=temp
                else:

                    temp=[]
                    for templist in cars[objectinstance]:
                        temp.append(templist)
                    
                    temp.append(coordinates)
                    
                    cars[objectinstance]=temp'''
                temp=cars[objectinstance]
                temp.extend(coordinates)
                cars[objectinstance]=temp
            else:
                
                cars[objectinstance]=coordinates

            #need the id 5th element as keys in the cars array as key

    frame=frame+1
for car in cars:
    carslen[car]= int(   len(cars[car]) / 5)
    #this counts the amount of frames an object instance appears. We want to only evaluate cars who appear in many frames.


#important is that every 5 variables a new coordiante starts. The structure of one cooordinate is minx, miny,maxx,maxy,and frame number
for x in sorted(carslen, key=carslen.get, reverse=True)[:5]:
    topcars[x]=cars[x]
f.close()

#topcars only contains the top cars ( who seem to appear the longest in the video)


examplecar=topcars[list(topcars)[0]]

examplecar_frames=examplecar[4:][::5] #gives us the frames in which the car apperaes


video_path   = args.input
#checking if the object is in the frame. and if the ground trouth also think that this is the object. Problem is that the object
vid = cv2.VideoCapture(video_path)

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(vid.get(cv2.CAP_PROP_FPS))
counter=1
accuracy=[]

class_list=json.load(open('class_list.json')) # contains the list from a2d2 matching every color in the label video to an object.
while True:
    _, frame = vid.read()
    

    try:
        original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
    
    
    except:
        break
    
    #check if frame number is counter

    #we can do this simpler than a long lookup like this.
    if counter in examplecar_frames:
        #car x is visible in all the frames in the list examplecar_frames. I now check if the current frame in the while Loop is one of the frames in which
        #the car is visible. The four elements before the frame in the array examplecar gives us the position of the boundary box
        index=examplecar.index(counter)
        minx=int(examplecar[index-4])
        miny=int(examplecar[index-3])
        maxx=int(examplecar[index-2])
        maxy=int(examplecar[index-1])
        
        #first value is the height, the second one is the width


        cutframe=frame[miny:maxy,minx:maxx]

        #cv2.imshow('cutframe',cutframe)
        #cv2.imshow('frame',frame)
        #cv2.waitKey(0)
        row, col, chan = cutframe.shape #row is y , col is x
        
        
        if cutframe.size is not 0:
            #path = f"cutframes/object{objectid}/frame{counter}"
            folder_path= f"{args.folder}/frame{counter}.jpg"
            
            #cv2.imwrite('cutframes/object1/frame%d.jpg' % counter, cutframe)
            cv2.imwrite(folder_path, cutframe)
        

        #now that we have the frame we need to evaluate all the cutframes. important is that we find the most prevelent color in the frame
        #https://github.com/tarikd/python-kmeans-dominant-colors/blob/master/utils.py
        '''
        for y in range(row-1):
            for x in range(col-1):
                color, _ =finding_nearest_color(cutframe[y,x])
                #the problem is that this is not the exact color which is in the list. so we use the finding_neare
                hex_color=webcolors.rgb_to_hex(tuple(color))
                #look up the color in the class list and try to see if it is a car.
                if 'Car' in class_list[hex_color]:
                    #the pixel represents a car
                    print("car has been found")
                    accuracy_hit=accuracy_hit+1
                else:   
                    
                    accuracy_miss=accuracy_miss+1
                
        tupeltoappend=(accuracy_hit,accuracy_miss)
        accuracy.append(tupeltoappend)
        '''

                
                
        
        

        
        


    
    counter=counter+1
#print(examplecar_frames)
cv2.destroyAllWindows()

