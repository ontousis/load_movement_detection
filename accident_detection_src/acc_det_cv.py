import cv2
import numpy as np
import time
from minio import Minio
from pymongo import MongoClient
import yaml
import os
from gpiozero import Buzzer

# Function to detect changes between frames, draw bounding box around the biggest change and record frame in case of changes over a threshold
def detect_changes(pr_lst, frame2, minio_client, bucketname, collection, change_threshold):

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    max_max_area=0
    max_max_contour=None
    fin_cumulative_area=0
    percentage_changed=0
    
    for frame1 in pr_lst:
        # Convert frames to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference between frames
        diff = cv2.absdiff(gray1, gray2)

        # Apply threshold to highlight the differences
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize variables for largest bounding box and cumulative area
        max_area = 0
        max_contour = None
        cumulative_area = 0

        # Find the contour with the largest area and calculate cumulative area
        for contour in contours:
            area = cv2.contourArea(contour)
            cumulative_area += area
            if area > max_area:
                max_area = area
                max_contour = contour
                if max_area>max_max_area:
                    max_max_area = max_area
                    max_max_contour = max_contour
                    fin_cumulative_area=-1
                    
        if fin_cumulative_area==-1:
            fin_cumulative_area=cumulative_area
            
        if max_contour is not None:
            # Calculate percentage of pixels changed
            total_pixels = frame1.shape[0] * frame1.shape[1]
            percentage_changed += (cumulative_area / total_pixels) * 100
            
    # Draw bounding box around the largest change area
    avg_percentage_changed=percentage_changed/len(pr_lst)
    if max_max_contour is not None:
        (x, y, w, h) = cv2.boundingRect(max_max_contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display area of the entire frame and area of bounding box
        cv2.putText(frame2, 'INCODE', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame2, f'Frame Area: {total_pixels} px', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame2, f'Bounding Box Area: {fin_cumulative_area} px', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, cv2.LINE_AA)

        # Display percentage of pixels changed
        cv2.putText(frame2, f'Change: {avg_percentage_changed:.2f}%', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

        # Store the biggest percentage change so far
        global biggest_percentage_change
        if avg_percentage_changed > biggest_percentage_change:
            biggest_percentage_change = avg_percentage_changed

    # Display the biggest percentage change so far
    cv2.putText(frame2, f'Biggest Change: {biggest_percentage_change:.2f}%', (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1, cv2.LINE_AA)
    det=0
    if avg_percentage_changed>=change_threshold:
        t=time.time_ns()//1000000
        cv2.imwrite("potential_accident"+str(t)+".jpg",frame2)
        minio_client.fput_object(bucketname,"potential_accident"+str(t)+".jpg","potential_accident"+str(t)+".jpg")
        url = minio_client.presigned_get_object(bucketname,"potential_accident"+str(t)+".jpg")
        entry={"url":url,"time":time.strftime("%d_%m_%Y_%H_%M_%S"),"movement_detected":str(round(avg_percentage_changed,2))+"%"}
        collection.insert_one(entry)
        os.remove("potential_accident"+str(t)+".jpg")
        det=1
    return frame2, det

# Open camera
camera = cv2.VideoCapture(0)

buzzer = Buzzer(17)

#Ininialize minio client and MongoDb client from config file
with open("config/config.yaml") as cf:
    conf=yaml.safe_load(cf.read())

minio_url=conf["minio_url"]
minio_usr=conf["minio_usr"]
minio_pwd=conf["minio_pwd"]
minio_bucket_name=conf["minio_bucket_name"]
minio_client=Minio(minio_url, access_key=minio_usr, secret_key=minio_pwd, secure=False)

db_usr=conf["mongodb_username"]
db_pwd=conf["mongodb_password"]
db_url="mongodb://"+db_usr+":"+db_pwd+"@"+conf["mongodb_server_ip"]+":"+str(conf["mongodb_server_port"])
client = MongoClient(db_url)
db=client[conf["mongodb_db_name"]]
collection=db[conf["mongodb_collection_name"]]

# Initialize the biggest percentage change
biggest_percentage_change = 0

# Wait for 2 seconds before starting to store the biggest percentage change
time.sleep(2)

#list of previous 3 frames
prev_lst=[]
count=0

#read detection threshold
ch_thr=conf["detection_threshold"]
delay=conf["delay_after_detection_ms"]
# Read the first frame
ret, prev_frame = camera.read()

prev_lst.append(prev_frame)

# Loop through frames
current_time=-1
time_init=0

buzzer_on=0
while True:
    # Read the next frame
    ret, next_frame = camera.read()

    # Set the current frame as the previous frame for the next iteration ()
    prev_frame = next_frame.copy()

    # Detect changes and draw bounding box around the biggest change if some time has passed since the last detection
    det=0
    current_time=time.time_ns()//1000000
    if current_time-time_init>=delay:
    	if buzzer_on==1:
    		buzzer_on=0
    		buzzer.off()
    	result_frame,det = detect_changes(prev_lst, next_frame, minio_client, minio_bucket_name, collection, ch_thr)
    if det:
    	det=0
    	buzzer.on()
    	buzzer_on=1
    	time_init=time.time_ns()//1000000
    	
    #append it to the list of previous frames
    count+=1
    if count<3:
        prev_lst.append(prev_frame)
    else:
        if count==6:
           count=3
        prev_lst[count%3]=prev_frame
# Release camera and close windows
camera.release()
