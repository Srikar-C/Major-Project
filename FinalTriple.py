from imageai.Detection import ObjectDetection
from matplotlib import pyplot as plt
from keras.preprocessing.image import load_img
import cv2
import Challan
def main(FrameNumber):
    persontriplecount=0
    detector= ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("yolov3.pt")
    detector.loadModel()
    input = "OutPut/Finalnew/Full/full-"+str(FrameNumber)+".jpg"
    custom=detector.CustomObjects(person=True)
    plt.show()
    detections=detector.detectObjectsFromImage(custom_objects=custom, input_image=input,output_image_path="OutPut/FinalOutput/Triple.jpg",minimum_percentage_probability=90)
    count=0
    imjh=load_img(input)
    plt.figure()
    plt.imshow(imjh)
    plt.show()
    for eachObject in detections:
        print(eachObject["name"]," : ",eachObject["percentage_probability"]," : ",eachObject["box_points"])
        print("_______________________")
        count+=1
    print("No of person : ",count)
    imjhout=load_img("OutPut/FinalOutput/Triple.jpg")
    plt.figure()
    plt.imshow(imjhout)
    plt.show()
    plt.pause(0.1)
    persontriplecount=count
    if count>=3 :
        print("Triple Riding.")
        print("go for autochallan")
        Challan.main(FrameNumber)
    else:
        print("No Triple Ride")
if __name__=="__main__":
    main()