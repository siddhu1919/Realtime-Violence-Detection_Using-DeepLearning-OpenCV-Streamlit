import cv2
import streamlit as st
import os
from datetime import datetime  # Import datetime to generate timestamp
from predict2 import predict_frames_from_folder
import shutil



# Function to save a frame with timestamp
def save_frame(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join("frames", f"frame_{timestamp}.jpg")
    cv2.imwrite(filename, frame)

    # Create the 'frames' directory if it doesn't exist


if not os.path.exists("frames"):
    try:
        os.makedirs("frames")
    except FileExistsError:
        pass  # Directory already exists, do nothing


# Initialize session states
if "capture" not in st.session_state:
    st.session_state.capture = False
if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0  # To count frames for periodic prediction

# UI

st.set_page_config(
   page_title="Realtime Violence Detection 🔴",
   page_icon="🛡️",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.title("D A S H B O A R D 📱")
# st.header('D A S H B O A R D 📱', divider='rainbow')

# Placeholder for displaying messages
message_placeholder = st.empty()

# Container for the video feed
video_container = st.empty()

# Buttons for starting and stopping video capture
col1, col2, col3 = st.columns(
    3
)  # Adjust back to 2 columns, integrate Predict inside Start











with st.sidebar:
        st.image("stop violence.png")
        st.title("Realtime Violence Detection 🔴")






with col1:
    if st.button("Start"):
        # Reinitialize
        st.session_state.capture = True
        st.session_state.frame_count = 0  # Reset frame count on start
        message_placeholder.empty()
        if not hasattr(st.session_state, "cap") or not st.session_state.cap.isOpened():
            st.session_state.cap = cv2.VideoCapture(1)
        # Prediction result placeholder
        prediction_placeholder = st.empty()

with col2:
    if st.button("Stop"):
        st.session_state.capture = False
        if hasattr(st.session_state, "cap"):
            st.session_state.cap.release()
        message_placeholder.success("Video capturing has been stopped.")


dir_path = "frames"
with col3:
    if os.path.exists(dir_path):
        # Display a button in the Streamlit app to delete the directory
        if st.button("Delete Directory"):
            # Attempt to delete the directory
            try:
                shutil.rmtree(dir_path)
                st.success(f'Directory "{dir_path}" has been deleted successfully.')
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.write(f'Directory "{dir_path}" does not exist.')


# Capture and display loop with integrated prediction
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

        # Save the frame using the new timestamp naming convention
        save_frame(frame)
        st.session_state.frame_count += 1

        # Periodic prediction (e.g., for every 100 frames captured)
        if st.session_state.frame_count % 100 == 0:
            frames_folder_path = "frames"
            prediction = predict_frames_from_folder(frames_folder_path)
            prediction_placeholder.markdown("### Prediction Result")
            prediction_placeholder.write(prediction)

