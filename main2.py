import cv2
import streamlit as st
import os
from datetime import datetime  # Import datetime to generate timestamp
from predict2 import predict_frames_from_folder

# Import the predict_video function from predict.py


# Function to save a frame with timestamp
def save_frame(frame):
    # Use datetime to generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join("frames", f"frame_{timestamp}.jpg")
    cv2.imwrite(filename, frame)


# Create the 'frames' directory if it doesn't exist
if not os.path.exists("frames"):
    os.makedirs("frames")

# Initialize session states
if "capture" not in st.session_state:
    st.session_state.capture = False

# UI
st.title("Violence Detection with ML & OpenCV ")

# Placeholder for displaying messages
message_placeholder = st.empty()

# Container for the video feed
video_container = st.empty()

# Buttons for starting and stopping video capture
col1, col2, col3 = st.columns(
    3
)  # Adjust to add an extra column for the "Predict" button
with col1:
    if st.button("Start"):
        # Reinitialize
        st.session_state.capture = True
        message_placeholder.empty()
        if not hasattr(st.session_state, "cap") or not st.session_state.cap.isOpened():
            st.session_state.cap = cv2.VideoCapture(
                1
            )  # Make sure to use the correct camera index
        st.rerun()

with col2:
    if st.button("Stop"):
        st.session_state.capture = False
        if hasattr(st.session_state, "cap"):
            st.session_state.cap.release()
        message_placeholder.success("Video capturing has been stopped.")

# Predict button
# with col3:
#     if st.button("Predict"):
#         # Call the predict_video function and display its output
#         # # Specify the path to your folder containing frames
#         frames_folder_path = "frames"
#         prediction = predict_frames_from_folder(frames_folder_path)  # Assuming predict_video() is properly defined in predict.py
#         # Display the prediction result beautifully
#         st.markdown("### Prediction Result")
#         st.write(prediction)  # Customize this part based on how you want to display the prediction

# Predict button
with col3:
    if st.button("Predict"):
        # Call the predict_video function and display its output
        # Specify the path to your folder containing frames
        frames_folder_path = "frames"
        st.markdown("### Prediction Result")
        st.text("\n")  # Add a newline for spacing, if needed
        prediction = predict_frames_from_folder(
            frames_folder_path
        )  # Assuming predict_video() is properly defined in predict


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

        # Save the frame using the new timestamp naming convention
        save_frame(frame)
