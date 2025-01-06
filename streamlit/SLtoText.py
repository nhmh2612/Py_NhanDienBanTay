import streamlit as st
import cv2
import tempfile
import os
import mediapipe as mp

# Initialize Mediapipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def is_letter_a(landmarks):
    """
    Function to check if the hand pose matches the letter "A".
    A basic check for a closed fist with the thumb along the side.
    """
    thumb_tip = landmarks[4]      # Thumb tip
    index_tip = landmarks[8]      # Index finger tip
    middle_tip = landmarks[12]    # Middle finger tip
    ring_tip = landmarks[16]      # Ring finger tip
    pinky_tip = landmarks[20]     # Pinky finger tip

    # Check if all fingers are curled (y-coordinates of tips lower than their base)
    if (index_tip.y > landmarks[5].y and  # Index finger curled
        middle_tip.y > landmarks[9].y and  # Middle finger curled
        ring_tip.y > landmarks[13].y and  # Ring finger curled
        pinky_tip.y > landmarks[17].y and  # Pinky finger curled
        thumb_tip.x < landmarks[3].x):  # Thumb alongside the fist
        return True
    return False

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

    # Create an empty placeholder for output text
    output_text_placeholder = st.empty()

    # Placeholder for video frame
    stframe = st.empty()

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

    # Get video properties
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

    # Prepare output video writer
    codec = cv2.VideoWriter_fourcc(*'mp4v')  # Use * for better readability
    output_file_name = 'output1.mp4'
    out = cv2.VideoWriter(output_file_name, codec, fps_input, (width, height))

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Video processing loop
    while True:
        ret, img = vid.read()
        if not ret:
            break  # Break the loop if the video ends

        img = cv2.flip(img, 1)  # Flip image horizontally
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe processing

        # Process the frame to detect hands
        result = hands.process(frame_rgb)

        # Default output text for each frame
        output_text = "No match for letter A"
        
        # Check if hand landmarks are detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect letter "A" from hand landmarks
                if is_letter_a(hand_landmarks.landmark):
                    output_text = "Letter A detected"

        # Display the detected letter on the screen
        output_text_placeholder.markdown(f'<p class="output-text">{output_text}</p>', unsafe_allow_html=True)

        frame = cv2.resize(img, (640, 480))  # Resize frame
        stframe.image(frame, channels='BGR', use_column_width=True)  # Display frame
        
        # Write the processed frame to output video
        out.write(img)

    # Finished processing
    st.text('Video Processed')

    # Release resources
    vid.release()
    out.release()

    # Check if video output file was created
    if os.path.exists(output_file_name):
        # Output the video
        with open(output_file_name, 'rb') as output_video:
            out_bytes = output_video.read()
            st.video(out_bytes)
    else:
        st.error("Video output file not found.")


