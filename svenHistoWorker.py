#This part of my project evaluates the Histogramm and looks at the accuracy
#https://stackoverflow.com/questions/2270874/image-color-detection-using-python
import os
import cv2
from PIL import Image
import json


import argparse


parser = argparse.ArgumentParser(description='create histogramms from the cutframes')
parser.add_argument('--input', help='folder path. in which the histogramms are located')
parser.add_argument('--name', help='name of the histosummarytxt')

args = parser.parse_args()

#histoPath= 'cutframes/object1/histogramms'
histoPath=args.input
def finding_nearest_color(color):
    class_list=json.load(open('class_list_rgb.json'))
    diff=255*3
    diff_color=(255,255,255)
    for keysss in class_list.keys():
        #convert string to rgb
        #check the case that the string doesnt have 9 characters because the integer started with a 0
        saved_key= keysss
        keysss=str(keysss)
        keysss = keysss.zfill(9)
        key_color=[]
        
        key_color.append(int(keysss[0:3]))
        key_color.append(int(keysss[3:6]))
        key_color.append(int(keysss[6:9]))


        #compare the key color with the color and find the difference

        temp= abs(key_color[0]-color[0])+abs(key_color[1]-color[1])+abs(key_color[2]-color[2])
        if temp <= diff:
            diff=temp
            diff_color=keysss

    #diff color is a string so we have to convert it back. 
    
    return_value=(diff_color[0:3],diff_color[3:6],diff_color[6:9])
    return return_value


def clear_string(color_string):
    #we have two cases red is
    returnstring=''
    split_string = color_string.split("-")
    #['', 'r123', 'g456', 'b789']
    #if the colors dont contain 3 digits then we have to do fillings with the zero.
    for substring in split_string:
        if substring.startswith("r") or substring.startswith("g") or substring.startswith("b"):
            color= substring[0]
            substring = substring[1:]
            if len(substring) != 3 :
                substring= substring.zfill(3)
            
            returnstring += substring

    return returnstring


def finding_class_list_entry(color):
    class_list=json.load(open('class_list_rgb.json'))
    color_string=f"-r{color[0]}-g{color[1]}-b{color[2]}"
    new_class_list={}
    for key in class_list:
        new_key = key.zfill(9)
        new_class_list[new_key]=class_list[key]
        #class_list[new_key]= class_list.pop(key)
    
    #the problem we have is that the keys in the class list are not 9 characters long. If thats the case, we need to fill them from the front
    #we need to take the string which has the shape like this r123g456b789 and remove the r g b letters while ensuring that the following 3 leters are numbers.
    
    return new_class_list[clear_string(color_string)]


files= os.listdir(histoPath)

histoSummary=[]
for histogramm in files :
    if histogramm.endswith(".jpg"):
        #the dominant color is in the middle of the frame.
        
        singlePath= f"{histoPath}/{histogramm}"
        
        class_list=json.load(open('class_list_rgb.json'))
        
        im = Image.open(singlePath, 'r')
        width, height = im.size
        pixel_values = list(im.getdata())
        color=pixel_values[width*int(height/2)+int(width/2)]
        
        color =finding_nearest_color(color)
        
        color_string=f"{color[0]}{color[1]}{color[2]}"
        
        histoSummary.append(f"{singlePath} {finding_class_list_entry(color)}")

with open(f"histoSummary/{args.name}_histosummary.txt", 'w') as f:
    for item in histoSummary:
        f.write("%s\n" % item)      
