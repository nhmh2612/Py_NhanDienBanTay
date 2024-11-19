import streamlit as st
import cv2
import tempfile
import os
import mediapipe as mp
import pickle
import numpy as np
import time
import pyttsx3

# Tải mô hình đã lưu
model_dict = pickle.load(open('model/model.p', 'rb'))
model = model_dict['model']

# Initialize Mediapipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Khởi tạo pyttsx3
engine = pyttsx3.init()

def SLtoText():
    st.title('Sign Language to Text')
    st.markdown("""
        <style>
            .title {
                color: #4B0082;
                font-size: 32px;
                font-weight: bold;
                text-align: center;
            }
            .output-text {
                font-size: 24px;
                color: #2E8B57;
                text-align: center;
                margin: 20px 0;
            }
            .sidebar-title {
                font-size: 18px;
                font-weight: bold;
                color: #FF6347;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar options
    st.sidebar.markdown('<p class="sidebar-title">Video Input Options</p>', unsafe_allow_html=True)
    use_webcam = st.sidebar.button('Use Webcam')
    record = st.sidebar.checkbox("Record Video")

    st.sidebar.markdown('---')

    # File uploader
    st.sidebar.markdown('<p class="sidebar-title">Upload Video File</p>', unsafe_allow_html=True)
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])

    # Output area
    st.markdown('## Output', unsafe_allow_html=True)

    # Placeholders for text output and video frame
    predicted_char_placeholder = st.empty()  # Placeholder for predicted character
    predicted_string_placeholder = st.empty()  # Placeholder for final predicted text
    stframe = st.empty()  # Placeholder for video frames

    # Temporary file for video upload
    tfflie = tempfile.NamedTemporaryFile(delete=False)

    if not video_file_buffer:
        if use_webcam:
            vid = cv2.VideoCapture(0)  # Use webcam if selected
        else:
            DEMO_VIDEO = 'demo.mp4'
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tfflie.name = DEMO_VIDEO
    else:
        tfflie.write(video_file_buffer.read())
        tfflie.close()  # Close the temporary file after writing
        vid = cv2.VideoCapture(tfflie.name)

    # Check if video is loaded
    if not vid.isOpened():
        st.error("Failed to load the video. Please check the file.")
        return

    # Get video properties
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

    # Prepare output video writer
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    output_file_name = 'output1.mp4'
    out = cv2.VideoWriter(output_file_name, codec, fps_input, (width, height))

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Initialize variables for countdown, prediction, and text output
    countdown_started = False
    countdown_time = 3  # seconds
    final_predicted_text = ""  # To store the final prediction string

    # Video processing loop
    while True:
        ret, img = vid.read()
        if not ret:
            break  # Break the loop if the video ends

        img = cv2.flip(img, 1)  # Flip image horizontally
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing

        # Process the frame to detect hands
        result = hands.process(frame_rgb)

        predicted_character = "No hands detected"  # Default value
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmarks from hand
                x_ = []
                y_ = []
                data_aux = []
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                # Normalize and prepare data for prediction
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))

                # Make prediction
                try:
                    prediction = model.predict([np.asarray(data_aux)])  # Predict character
                    predicted_character = prediction[0]  # Update predicted character
                except Exception:
                    predicted_character = "Prediction Error"

                if not countdown_started:
                    # Start countdown when hand is detected
                    countdown_started = True
                    countdown_start_time = time.time()

        # Handle countdown logic
        if countdown_started:
            elapsed_time = time.time() - countdown_start_time
            if elapsed_time < countdown_time:
                # Show countdown in video
                countdown_text = f"{countdown_time - int(elapsed_time)}"
                cv2.putText(img, countdown_text, (int(width / 2) - 50, int(height / 2)), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 0, 255), 5)
            else:
                # After countdown ends, add the predicted character to the final string
                if predicted_character == "1":
                    final_predicted_text += " "  # Add space if predicted "1"
                elif predicted_character == "2":
                    final_predicted_text = ""  # Clear text if predicted "2"
                elif predicted_character != "No hands detected" and predicted_character != "Prediction Error":
                    final_predicted_text += predicted_character  # Add character to string
                countdown_started = False  # Stop countdown after it reaches 0

        # Display the predicted character
        predicted_char_placeholder.markdown(
            f'<p class="output-text">Predicted Character: {predicted_character}</p>',
            unsafe_allow_html=True
        )

        # Display the full predicted string
        predicted_string_placeholder.markdown(
            f'<p class="output-text">Predicted Text: {final_predicted_text}</p>',
            unsafe_allow_html=True
        )

        # Resize frame for display
        frame = cv2.resize(img, (640, 480))  # Resize frame
        stframe.image(frame, channels='BGR', use_container_width=True)  # Display frame

        # Write the processed frame to output video
        out.write(img)

    # Finished processing
    st.text('Video Processed')

    # Release resources
    vid.release()
    out.release()

    if os.path.exists(output_file_name):
        # Output the video
        with open(output_file_name, 'rb') as output_video:
            out_bytes = output_video.read()
            st.video(out_bytes)
    else:
        st.error("Video output file not found.")

    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button('Read Text Aloud'):
        if final_predicted_text.strip():  # Kiểm tra nếu chuỗi không rỗng
            st.info(f"Reading Text Aloud: {final_predicted_text}")
            engine.say(final_predicted_text)
            engine.runAndWait()
        else:
            st.warning("No text to read!")

SLtoText()
