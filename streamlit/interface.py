import streamlit as st
import time
import os
import speech_recognition as sr
from PIL import Image


# Function to display sign language images
def display_images(text):
    img_dir = "images/"  # Ensure this directory contains images like a.png, b.png, etc., and space.png for space

    # Position to update images
    image_pos = st.empty()

    # Loop through each character in the text and display the corresponding image
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            img_path = os.path.join(img_dir, f"{char}.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                image_pos.image(img, width=300)  # Display image in 'image_pos' container
                time.sleep(2)  # Wait 2 seconds
                image_pos.empty()
        elif char == ' ':
            img_path = os.path.join(img_dir, "space.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                image_pos.image(img, width=300)  # Display image for space
                time.sleep(2)
                image_pos.empty()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # # Kiểm tra các microphone đang có sẵn
    # mic_list = sr.Microphone.list_microphone_names()
    # st.write("Danh sách microphone: ", mic_list)

    with mic as source:
        st.write("Đang lắng nghe... Hãy nói vào micro!")
        recognizer.adjust_for_ambient_noise(source)  # Điều chỉnh cho tiếng ồn xung quanh
        try:
            audio = recognizer.listen(source, timeout=5)  # Lắng nghe trong 5 giây
        except sr.WaitTimeoutError:
            st.error("Không nhận được tín hiệu âm thanh từ microphone!")
            return None
        except sr.RequestError as e:
            st.error(f"Lỗi kết nối: {e}")
            return None

    try:
        # Nhận diện giọng nói bằng Google Web Speech API
        text = recognizer.recognize_google(audio, language='en-US')  # Cần thay đổi ngôn ngữ nếu bạn muốn
        st.markdown(f"<div class='result-text'>Bạn đã nói: '{text}'</div>", unsafe_allow_html=True)
        return text.lower()  # Trả về văn bản nhận diện được
    except sr.UnknownValueError:
        st.error("Không thể nhận diện được giọng nói.")
    except sr.RequestError as e:
        st.error(f"Có lỗi xảy ra: {e}")

# Test call:
# recognized_text = recognize_speech_from_mic()
# print(recognized_text)  # Nếu bạn muốn in kết quả trong terminal


# Main UI function
def speech_to_sign_ui():
    # Custom CSS for the interface
    st.markdown("""
        <style>
            body {
                background: linear-gradient(145deg, #f0f4f8, #ffffff);
                font-family: 'Arial', sans-serif;
            }
            .title {
                font-size: 48px;
                color: #2c3e50;
                text-align: center;
                font-weight: bold;
                margin: 40px 0 20px 0;
                text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            }
            .subtitle {
                font-size: 20px;
                color: #34495e;
                text-align: center;
                margin-bottom: 40px;
                text-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            }
            .button {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 15px 30px;
                text-align: center;
                font-size: 20px;
                border-radius: 30px;
                margin: 10px 0;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            .button:hover {
                background-color: #3498db;
                transform: translateY(-2px);
                box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
            }
            .button:active {
                transform: translateY(1px);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            .intro-image {
                margin: 20px auto;
                display: block;
                width: 70%;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            .result-text {
                font-size: 24px;
                color: #2c3e50;
                text-align: center;
                margin-top: 30px;
                animation: fadeIn 1s ease-in;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .column {
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Main interface
    st.markdown("<div class='title'>Chuyển Đổi Giọng Nói Sang Ngôn Ngữ Ký Hiệu</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Chuyển đổi giọng nói của bạn sang các ký hiệu.</div>", unsafe_allow_html=True)

    # Intro image
    st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj4MsLwQcrXHlHoIezTPh2ba2K7rD3bOC_Tos72H0yjtojxilsCNJszTDuDIxLegfQS9KppgGNdouCx3EbJtaX0mH82X4gEZvGrnhPVyK-dRzPTUi7aXn7jxxVXgcOozxrJ7BA-pg9F7rMMg51qmJuP-AT_kO9RebzDvajBO7KrEmh7NrZtqg-EnFU3/s16000/Traveling%20with%20a%20Disability%20in%20Vietnam%2004.jpg", 
             use_column_width=True, caption="Chào mừng đến với ứng dụng Ngôn Ngữ Ký Hiệu", output_format="PNG")

    # Buttons and text input
    col1, col2 = st.columns(2)

    # Text input section
    with col1:
        st.markdown("<div class='column'>", unsafe_allow_html=True)
        text_input = st.text_input("Nhập văn bản của bạn:")
        if st.button("Hiển thị ngôn ngữ ký hiệu", key='text_input_button'):
            if text_input:
                text_input = text_input.lower()  # Convert to lowercase
                st.markdown(f"<div class='result-text'>Bạn đã nhập: '{text_input}'</div>", unsafe_allow_html=True)
                display_images(text_input)
        st.markdown("</div>", unsafe_allow_html=True)

    # Speech input section
    with col2:
        st.markdown("<div class='column'>", unsafe_allow_html=True)
        if st.button("Bắt đầu nói", key='start_button', help="Nhấn để bắt đầu nhận diện giọng nói"):
            recognized_text = recognize_speech_from_mic()  # Recognize speech from microphone
            if recognized_text:  # If speech is recognized
                display_images(recognized_text)  # Display corresponding sign images
        st.markdown("</div>", unsafe_allow_html=True)


