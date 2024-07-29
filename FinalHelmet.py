import glob
import itertools
import re
import json
import time
from keras import backend as k
from keras.preprocessing.image import load_img
import cv2
import numpy as np
import Challan

frame=None
frame_count=0
frame_count_out=0
confThreshold=0.5
nmsThreshold=0.4
inpWeight=416
inpHeight=416
a=0
nh=[]
classesfile="configuration/helmet.names"

with open(classesfile,'rt') as f:
    classes=f.read().rstrip('\n').split('\n')

modelConfiguration='configuration/yolov3-helmet.cfg'
modelWeights='configuration/yolov3-helmet.weights'

net=cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
layersNames=net.getLayerNames()

# Create a dictionary where the keys are the layer indices and the values are the layer names
layer_dict = {layer_index: layer_name for layer_index, layer_name in enumerate(layersNames, start=1)}

# Get the indices of the output layers
output_layer_indices = net.getUnconnectedOutLayers()
# Use these indices to obtain the corresponding layer names
output_layer = [layer_dict[i] for i in output_layer_indices]
helmetdefaultsList=[]
def drawPred(classId, conf, left, top, right, bottom):
    global frame_count
# Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    label = '%.2f' % conf
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    #print(label)            #testing
    #print(labelSize)        #testing
    #print(baseLine)         #testing

    label_name,label_conf = label.split(':')    #spliting into class & confidance. will compare it with person.
    if label_name == 'Helmet':
                                            #will try to print of label have people.. or can put a counter to find the no of people occurance.
                                        #will try if it satisfy the condition otherwise, we won't print the boxes or leave it.
        cv2.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)
        frame_count+=1


    #print(frame_count)
    if(frame_count> 0):
        return frame_count

def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    global frame_count_out
    frame_count_out=0
    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []               #have to fins which class have hieghest confidence........=====>>><<<<=======
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                #print(classIds)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    count_person=0 # for counting the classes in this loop.
    for i in indices:

        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
               #this function in  loop is calling drawPred so, try pushing one test counter in parameter , so it can calculate it.
        frame_count_out = drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
         #increase test counter till the loop end then print...

        #checking class, if it is a person or not

        my_class='helmet'                   #======================================== mycode .....
        unknown_class = classes[classId]

        if my_class == unknown_class:
            count_person += 1
    #if(frame_count_out > 0):
    return frame_count_out
def main(FrameNumber):
        count=0
        input = "OutPut/Finalnew/Rider/rider-" + str(FrameNumber) + ".jpg"

        frame1 = cv2.imread(input)
        h,w,c=frame1.shape
        if h>100:
            frame=cv2.resize(frame1,(125,125))
            frame_count =0

            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWeight, inpHeight), [0,0,0], 1, crop=False)

            # Sets the input to the network
            net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = net.forward(output_layer)

            # Remove the bounding boxes with low confidence
            a=postprocess(frame, outs)

            frame=cv2.resize(frame,(300,300))
            cv2.imshow('frame',frame)
            cv2.imwrite("OutPut/newoutput/newhelmet/helmet-" + str(count) + ".jpg", frame)
            # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
            t, _ = net.getPerfProfile()
            #print(t)
            label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
            #print(label)
            cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            cv2.waitKey(1)
            #print(label)
            if(a>0):
                print("Helmet detected")
            else:
                print("No Helmet detected")
                Challan.main(FrameNumber)
        else :
            print("Input Image is not suitable for detection.")
if __name__=="__main__":
    main()





