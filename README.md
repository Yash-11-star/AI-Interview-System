# AI Interview System

Welcome to the AI Interview System repository! This project is designed to conduct automated interviews utilizing speech recognition, machine learning models, and natural language processing techniques. The system allows for interviewee evaluation and prediction.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The AI Interview System is an innovative solution aimed at automating the interview process. It uses speech recognition, text-to-speech, and machine learning models to conduct interviews and analyze interviewee responses.

## Features

- **Speech Recognition:** Utilizes `SpeechRecognition` for listening to and interpreting the interviewee's spoken responses.
- **Machine Learning Models:** Implements machine learning models for predicting code clusters based on provided questions.
- **Interview Evaluation:** Assesses the accuracy of responses using fuzzy text matching and provides a recruitment prediction based on the interviewee's answers.
- **User Interface:** Utilizes `Streamlit` to provide an interactive and user-friendly web interface for interview sessions.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Yash-11-star/AI-Interview-System.git
```

2. Navigate to the project directory:

```bash
cd AI-Interview-System
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Ensure that you have Python and the necessary libraries such as `streamlit`, `SpeechRecognition`, `fuzzywuzzy`, `pandas`, and `numpy`, listed in the `requirements.txt` file.

## Usage

1. Run the Streamlit application:

```bash
streamlit run aap.py
```

2. Access the provided URL to begin the interview process and follow the on-screen instructions.

## File Structure

- `aap.py`: The primary script containing the main functionality of the AI Interview System.
- `Main.py`: Incorporates the machine learning model for predicting code clusters based on questions.
- `Model.py`: Implements the machine learning model for clustering codes and provides a summary of the trained model.

Please refer to the individual scripts for detailed functions and implementation.

## Contributing

Contributions are welcome! Fork the repository, make changes, and create pull requests to enhance the system's functionality or address any issues.
