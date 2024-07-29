import cv2
import matplotlib.pyplot as plt
from imageai.Detection import VideoObjectDetection
import os
camera = "newinput_Trim.mp4"
# execution = os.getcwd()
color_index = {'motorbike' : 'red'}
resized = True
count = 0
import FinalTriple
import FinalHelmet
def bikedetect(frame_number,output_array,output_count,returned_frame):
    print("Bike Frame  :  ",frame_number)
    if 'motorbike' in output_count and output_count['motorbike'] > 0 :
    #     plt.rcParams["figure.figsize"]=(25,3)
    #     plt.clf()
    #
        this_colors=[]
        labels=[]
        sizes=[]
        counter=0
    #
        for eachItem in output_count:
            counter+=1
            labels.append(eachItem+" = "+str(output_count[eachItem]))
            sizes.append(output_count[eachItem])
            this_colors.append(color_index[eachItem])
        #
        global resized
        global count
    #
        if (resized == False):
            manager = plt.get_current_fig_manager()
            manager.resize(w=500,h=1000)
            resized = True
        for item in output_array:
            x1 = item['box_points'][0]
            y1 = item['box_points'][1]
            x2 = item['box_points'][2]
            y2 = item['box_points'][3]
            if(y2-y1 > 150 and y2>150 and (x2-x1)>50):
                new_frame = returned_frame[max(int(y1-(y2-y1)*0.9),0):y2,x1:x2]
                helmet_image = returned_frame[max(int(y1/4-(y2/4-y1/4)*(0.8/4)),0):y1,x1:x2]
                bike_image = returned_frame[y1:y2,x1:x2]
                count+=1
                cv2.imwrite("OutPut/Finalnew/Bike/bike-"+str(count)+".jpg",bike_image)
                cv2.imwrite("OutPut/Finalnew//Rider/rider-" + str(count) + ".jpg", helmet_image)
                cv2.imwrite("OutPut/Finalnew/Full/full-"+str(count)+".jpg",new_frame)
                plt.title("frame number  " + str(frame_number))
                plt.imshow(new_frame)
                print("Going for Helmet detection")
                FinalHelmet.main(count)
                print("Going for Triple raid detection")
                FinalTriple.main(count)
            plt.pause(0.1)
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("yolov3.pt")
detector.loadModel()
custom_bikes = detector.CustomObjects(motorbike=True)
plt.show()
print("Starting The Bike Detection : ")
detector.detectObjectsFromVideo(custom_objects=custom_bikes,
                                input_file_path="./InputVideos/RoadVideo02.mp4",
                                output_file_path="OutPut/newoutput/bikeride",
                                frames_per_second=1,
                                per_frame_function=bikedetect,
                                minimum_percentage_probability=70,
                                return_detected_frame=True,
                                frame_detection_interval=20)
