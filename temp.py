import streamlit as st
import cv2
import os
import threading
from datetime import datetime
from glob import glob

# Initialize or create 'frames' directory if it doesn't exist
if not os.path.exists("frames"):
    os.makedirs("frames")

# Initialize session state attributes if they don't exist
if 'capture' not in st.session_state:
    st.session_state.capture = False
if 'last_frame' not in st.session_state:
    st.session_state.last_frame = None

# Function to save a frame in BGR format
def save_frame(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join("frames", f"{timestamp}.jpg")
    cv2.imwrite(filename, frame)

def capture_frames():
    cap = cv2.VideoCapture(1)  # Change 0 to 1 if your webcam index is different
    while st.session_state:
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.session_state.last_frame = frame_rgb
            save_frame(frame)
        else:
            print("Failed to capture video")
            st.session_state.capture = False
    cap.release()

# UI Layout
st.title("Video Capture and Prediction App")

# Video container
video_container = st.empty()

# Button row for Start, Stop, and Predict
start_button, stop_button, predict_button = st.columns(3)

# Start button functionality
if start_button.button("Start"):
    st.session_state.capture = True
    # Initialize background thread for video capture if not already running
    if 'thread' not in st.session_state or not st.session_state.thread.is_alive():
        st.session_state.thread = threading.Thread(target=capture_frames, daemon=True)
        st.session_state.thread.start()
    # Predict button should be unavailable when capturing
    predict_button.empty()

# Stop button functionality
if stop_button.button("Stop"):
    st.session_state.capture = False

# Display the last captured frame
if st.session_state.last_frame is not None:
    video_container.image(st.session_state.last_frame, use_column_width=True)

# Display captured frames in a scrollable, collapsible container
frames_files = sorted(glob("frames/*.jpg"), reverse=True)
if frames_files:
    with st.expander("Show Captured Frames", expanded=True):
        cols = st.columns(3)
        for i, frame_file in enumerate(frames_files):
            with cols[i % 3]:
                st.image(frame_file, use_column_width=True)
