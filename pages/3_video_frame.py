import streamlit as st
import cv2
import threading
import time
st.set_page_config(page_title="RTSP Stream Viewer")
# RTSP URL of the video feed
rtsp_url = "rtsp://admin:zmh123456@192.168.1.64:554"
# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    st.error("Error opening video stream.")
else:
    # Read the first frame
    ret, frame = cap.read()
    # Get the dimensions of the frame
    height, width, channels = frame.shape
    # Create a Streamlit canvas to display the video feed
    canvas = st.empty()

    # Continuously read and display frames from the video feed
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Error reading frame from video stream.")
            break
        # Resize the frame to fit the Streamlit canvas
        resized_frame = cv2.resize(frame, (int(width / 2), int(height / 2)))
        # Display the resized frame on the Streamlit canvas
        canvas.image(resized_frame, channels="BGR")
    # Release the VideoCapture object and close the Streamlit app
    cap.release()
    st.info("Video stream stopped.")
