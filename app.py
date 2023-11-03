import streamlit as st
import pyttsx3
import speech_recognition as sr
import threading
import time
from gtts import gTTS
from tempfile import NamedTemporaryFile
import os
import pydub
import csv
import numpy as np
from fuzzywuzzy import fuzz

uploaded_file= None
# Import the necessary functions and data from Main
from Main import model as dec

code = dec.code
df = dec.df

if code in df['Code'].values:
    questions = df[df['Code'] == code]['Question'].values[:5]
    answers = df[df['Code'] == code]['Answer'].values[:5]
else:
    st.write("No matching code found in the DataFrame.")

# Set the speech recognition microphone source
# You may need to adjust this depending on your system's configuration
microphone_source = sr.Microphone()

# Initialize the speech recognition engine once
recognizer = sr.Recognizer()

recognizer_started = False


def start_recognizer():
    global recognizer_started
    with microphone_source as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer_started = True


def speak(text):
    """Speaks the provided text using pyttsx3."""
    with NamedTemporaryFile(suffix=".wav", delete=False) as tts_file:
        tts = gTTS(text=text, lang="en")
        tts.save(tts_file.name)
        audio = pydub.AudioSegment.from_file(tts_file.name)
        audio.export(tts_file.name, format="wav")
        st.audio(tts_file.name, format="audio/wav")
        # os.remove(tts_file.name)


def listen():
    """Listens to user speech and returns the recognized text."""
    if not recognizer_started:
        start_recognizer()

    try:
        with microphone_source as source:
            st.write("Listening...")
            time.sleep(2)  # Wait for 10 seconds before listening
            audio = recognizer.listen(source)
            st.write("Processing speech...")
            text = recognizer.recognize_google(audio)
            st.write("Recognized speech:", text)
            return text
    except sr.UnknownValueError:
        st.write("Speech recognition could not understand audio.")
        return ""
    except sr.RequestError:
        st.write("Could not connect to speech recognition service.")
        return ""


def load_answers_from_csv(file_path):
    answers = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            question = row[0]
            answer = row[1]
            answers[question] = answer
    return answers


def calculate_accuracy(spoken_text, answers):
    accuracy_scores = []
    for question, answer in answers.items():
        similarity_score = fuzz.ratio(spoken_text, answer)
        accuracy_scores.append(similarity_score)
    accuracy = np.mean(accuracy_scores)
    return accuracy


def interview():
    """Conducts an interview by asking questions and recording responses."""
    st.write("Welcome to the interview! Please answer the following questions:")
    answers_given = []

    for i, question in enumerate(questions):
        st.write("Question:", question)
        speak(question)  # Call the speak function with the question
        time.sleep(5)  # Pause for 2 seconds to allow the user to answer
        response = listen()
        while response == "":
            response = listen()  # Wait until the answer is finished
        answers_given.append(response)

    speak("Thank you for your answers. The interview is complete.")

    # Print the user's responses
    for i, answer in enumerate(answers_given):
        st.write("Question:", questions[i])
        st.write("Answer:", answer)
        st.write()

    spoken_text = ' '.join(answers_given)  # Combine the spoken answers into a single text

    # Calculate accuracy
    file_path = '/Users/yashtembhurnikar/Programming/GAIP PROJECT/Scrape/GAIP/Final.csv'  # Replace with the path to your answer dataset CSV file
    answers_dataset = load_answers_from_csv(file_path)
    accuracy = calculate_accuracy(spoken_text, answers_dataset)

    st.write(f"Recruitment Prediction:{accuracy*1000}")

    # Determine if the applicant is recruited based on accuracy threshold
    if accuracy >= 2:
        st.write("Congratulations! You high chances of getting recruited.")
    else:
        st.write("Sorry, you will have to practice more.")

    # Save the uploaded PDF file
    if uploaded_file is not None:
        save_directory = "/Users/yashtembhurnikar/Programming/GAIP PROJECT/Scrape/GAIP"  # Replace with your desired directory path
        filename = "resume.pdf"
        save_path = os.path.join(save_directory, filename)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("Resume saved successfully!")


def main():
    st.title("IntervAI")

    # Add file upload functionality for the resume
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file is not None:
        # Perform operations on the uploaded file, if required
        st.write("File uploaded successfully!")

    interview()


if __name__ == "__main__":
    main()
