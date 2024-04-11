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



# Prediction Text For Debugging 
prediction_text = False


# UI

st.set_page_config(
    page_title="Realtime Violence Detection 🔴",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("D A S H B O A R D 📱")
# st.header('D A S H B O A R D 📱', divider='rainbow')


# Model Path
MODEL_PATH = ""

# Add Dropdown for model selection
# model_selection = st.selectbox(
#     "Select Your Desired Model🌈",
#     ("BILSTM_RESNET_MODEL", "BILSTM_VGG16T_MODEL", "MoBiLSTM_model"),
#     index=0,  # Default selection is the first model
# )

# Add a condition to render the model selection dropdown or show the selected model based on the capture state
if not st.session_state.capture:
    # Add Dropdown for model selection
    model_selection = st.selectbox(
        "Select Your Desired Model🌈",
        ("BILSTM_RESNET_MODEL", "BILSTM_VGG16T_MODEL", "MoBiLSTM_model"),
        index=0,  # Default selection is the first model
    )
else:
    # If capture has started, show the selected model as text (or a disabled input if you prefer)
    st.text(f"Selected Model: {st.session_state.model_selection}")
    # Ensure the model_selection is stored in session state after selection
    model_selection = st.session_state.model_selection

# Store the selected model in the session state when not capturing to preserve selection after start
if not st.session_state.capture:
    st.session_state.model_selection = model_selection


# Assuming models are stored in a 'models' folder and are named 'model1.h5', 'model2.h5', 'model3.h5'
MODEL_PATH = f"models/{model_selection.replace(' ', '')}.h5"


print("Selected 🔷 Model ", model_selection)

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


# with col2:
#     if st.button("Stop"):
#         st.session_state.capture = False
#         if hasattr(st.session_state, "cap"):
#             st.session_state.cap.release()
#         message_placeholder.success("Video capturing has been stopped.")


# CODE ADDED BY SID TO ENSURE THAT STOP BUTTON IS ONLY AVAILABLE IS START BTN IS PRESSED

with col2:
    # Only show the "Stop" button if st.session_state.capture is True, indicating the "Start" button has been pressed
    if st.session_state.capture:
        if st.button("Stop"):
            st.session_state.capture = False
            if hasattr(st.session_state, "cap"):
                st.session_state.cap.release()
            message_placeholder.success("Video capturing has been stopped.")


# dir_path = "frames"
# with col3:
#     if os.path.exists(dir_path):
#         # Display a button in the Streamlit app to delete the directory
#         if st.button("Delete Directory"):
#             # Attempt to delete the directory
#             try:
#                 shutil.rmtree(dir_path)
#                 st.success(f'Directory "{dir_path}" has been deleted successfully.')
#             except Exception as e:
#                 st.error(f"Error: {e}")
#     else:
#         st.write(f'Directory "{dir_path}" does not exist.')


# Col3 is edited by Sid for better performance and Exception Handling.
dir_path = "frames"
with col3:
    if os.path.exists(dir_path):
        # Conditionally show the "Delete Directory" button based on capture state
        if not st.session_state.capture:
            if st.button("Delete Directory"):
                try:
                    shutil.rmtree(dir_path)
                    st.success(f'All "{dir_path}" has been deleted successfully.')
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            # When capturing is active, indicate that the "Delete Directory" button is unavailable
            st.text("Delete (Unavailable while Rec🔴)")
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

            # Below Code is Commented by Me for Exception Handling
            # prediction = predict_frames_from_folder(frames_folder_path, MODEL_PATH)
            # prediction_placeholder.markdown("### Prediction Result")
            # prediction_placeholder.write(prediction)

            # Code With Exception Handling
            prediction = predict_frames_from_folder(frames_folder_path, MODEL_PATH)
            prediction_text = prediction
            prediction_placeholder.markdown("### Prediction Result")
            print("For Debugging",prediction_text)
            prediction_placeholder.write(prediction)
            st.session_state.last_prediction = prediction


with st.sidebar:
    if prediction_text:
        st.markdown("### Last Prediction Result")
        st.markdown(":blue["+prediction_text+"]")
        
    else:
        st.markdown("### Last Prediction Result")
        st.markdown(":green[No Prediction Dude!]")
