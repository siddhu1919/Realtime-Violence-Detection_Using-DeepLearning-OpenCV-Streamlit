import cv2
import streamlit as st
import os


# Function to save a frame in BGR format
def save_frame(frame, frame_count):
    filename = os.path.join("frames", f"frame_{frame_count:03d}.jpg")
    cv2.imwrite(filename, frame)


# Create the 'frames' directory if it doesn't exist
if not os.path.exists("frames"):
    os.makedirs("frames")

# Initialize session states
if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0

if "capture" not in st.session_state:
    st.session_state.capture = False

# UI
st.title("Video Capture with OpenCV")

# Placeholder for displaying messages
message_placeholder = st.empty()

# Container for the video feed
video_container = st.empty()

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start"):
        # Reinitialize
        st.session_state.capture = True
        st.session_state.frame_count = 0
        message_placeholder.empty()
        if not hasattr(st.session_state, "cap") or not st.session_state.cap.isOpened():
            st.session_state.cap = cv2.VideoCapture(1)  # Open default camera
        st.rerun()

with col2:
    if st.button("Stop"):
        st.session_state.capture = False
        if hasattr(st.session_state, "cap"):
            st.session_state.cap.release()
        message_placeholder.success("Video capturing has been stopped.")

# Capture and display loop
if st.session_state.capture:
    while st.session_state.capture:
        ret, frame = st.session_state.cap.read()
        if not ret:
            message_placeholder.error("Failed to capture video.")
            st.session_state.capture = False
            if hasattr(st.session_state, "cap"):
                st.session_state.cap.release()
            break

        # Display the frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_container.image(frame_rgb, channels="RGB", use_column_width=True)

        # Save the frame in BGR format
        save_frame(frame, st.session_state.frame_count)
        st.session_state.frame_count += 1
