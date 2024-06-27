import cv2
import imutils
import time
from alert import send_email_alert

# Initialize the webcam
cap = cv2.VideoCapture(0)
first_frame = None

# Define the cooldown period (in seconds)
cooldown_period = 60
last_sent = 0

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    text = "No Motion Detected"
    
    # Resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Initialize the first frame
    if first_frame is None:
        first_frame = gray
        continue
    
    # Compute the absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours on the thresholded image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Motion Detected"
        motion_detected = True
    
    # Check cooldown period before sending an email
    current_time = time.time()
    if motion_detected and (current_time - last_sent) > cooldown_period:
        send_email_alert("Motion Detected", "Motion has been detected on your security camera.")
        last_sent = current_time
    
    # Display the text and the frame
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frame_delta)
    
    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
