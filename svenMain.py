#this is a main file, to get the whole workflow of Sven Leschbers anfaenger Praktikum.
import os
import pathlib

videos = sorted(os.listdir('./IMAGES/'))
videos.remove('.DS_Store')
videos.remove('temptrack.mp4')

for i in range (0,len(videos),2):
#for i in range(2,4,2):
    

    video = videos[i]
    video_label = videos[i+1]

    print(video)
    print(video_label)
    
    #repeat this process for every video we have in the folder IMAGES. In it we have follwing structure: the main video has the end video and the ground truth has the ending video video_label.
    #the video with the tracking information doesnt concern us so we always save it in the same file
    tracked_video = "./IMAGES/temptrack.mp4"
    track_command = f"python3 object_tracker.py --input ./IMAGES/{video} --output {tracked_video}"
    #print(track_command)
    #os.system(track_command)

    #we first use the file object_tracker.py to use the predefined tracking functions and librarys to work. It takes as a paramter the path to a video. It returns a txt file in the folder
    #called 'trackinfo.txt'


    #we then call the svenTrack.py file which analyses and evalueates the trackinfo.txt file to find the tracks which last the longest and are potentatilly the most interesting to further examine.
    #the sven Track file also needs to the ground truth video.
    #This file creates subfolders in the folder cutframes which contain the frames, in which the car is tracked. We also give a parameter which specifies the folder in which the cutframes are saved
    #to.


    cut_videoname= video[:-4]
    track_command= f"python3 svenTrack.py --input ./IMAGES/{video_label} --folder ./cutframes/{cut_videoname}/"
    #have to create a the folder in which it is saved.
    pathlib.Path(f"./cutframes/{cut_videoname}/").mkdir(parents=True, exist_ok=True)

    #os.system(track_command)

    #After that we use the svenFrameEval.py which creates histogramms for each cutframe containing the most prominent color.
    #we need the name of the folder, in which the cutframes are in as a paramter
    histo_command= f"python3 cutframes/svenFrameEval.py --input {cut_videoname}"
    pathlib.Path(f"./cutframes/{cut_videoname}/histogramms/").mkdir(parents=True, exist_ok=True)
    #os.system(histo_command)

    #we then use the file svenHistoWorker.py which looks at the histogramms and uses the prominent find nearest color function, to assing an object to an histogramm. The results are saved in the 
    #histsummary.txt The file accepts the path towards the histogramm folder.

    summary_command= f"python3 svenHistoWorker.py --input cutframes/{cut_videoname}/histogramms --name {cut_videoname}"

    os.system(summary_command)
    # lastly we use the svenHistosummaryVis.py

    '''

    20180810_142822_video.mp4
    20180810_142822_video_label.mp4
    Traceback (most recent call last):
    File "cutframes/color_kmeans.py", line 22, in <module>
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.error: OpenCV(4.1.2) /Users/travis/build/skvark/opencv-python/opencv/modules/imgproc/src/color.cpp:182: error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'

    Traceback (most recent call last):
    File "svenHistoWorker.py", line 80, in <module>
        histoSummary.append(f"{singlePath} {finding_class_list_entry(color)}")
    File "svenHistoWorker.py", line 58, in finding_class_list_entry
        return class_list[color_string]
    KeyError: '000255255'
    20180925_101535_video.mp4
    20180925_101535_video_label.mp4
    Traceback (most recent call last):
    File "cutframes/color_kmeans.py", line 22, in <module>
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.error: OpenCV(4.1.2) /Users/travis/build/skvark/opencv-python/opencv/modules/imgproc/src/color.cpp:182: error: (-215:Assertion failed) !_src.empty() in function 'cvtColor'


'''
    
    