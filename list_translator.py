import webcolors
import json

#file to translate the hex values in class_list.json file to rgb 
class_list=json.load(open('class_list.json')) 
return_list={}
for keysss in class_list.keys():
    c=webcolors.hex_to_rgb(keysss)
    
    return_key='{:03}{:03}{:03}'.format(c[0],c[1],c[2])
    return_list[int(return_key)]=class_list[keysss]


with open('class_list_rgb.json', 'w') as outfile:
    json.dump(return_list, outfile)

