# Using Gemini with API

This directory contains code examples and resources for using Gemini with API.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is the demonstation of using gemini api with the help of API.

## Installation

To install the project and its dependencies, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Obtain your own Gemini API key.
4. Create a `.env` file in the root directory of the project.
5. Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY"
    ```

## Usage

To run any app use the following command :-
    `python3 -m streamlit run app-name.py`
    replace app-name with the name of the app you are running.

The folder all apps has three major files :-
--> 1. qachat.py
            this works like a chat bot. You can ask the question of your own!!.
            You can use this for :-
                -> Brand Extractor
                -> Ask for code
                -> Character designing
                -> To modify the tone of the given text
                And pretty much everything!!!

--> 2. vision.py
            This is an image based chat bot. You can upload a image and it analyses it. You can even give a promt on how to analyse the image.
            You can use this for :-
            -> Generate recipe from a given food image.
            -> Marketing description form an image
            -> Hurricane chart identification
            -> To identify the series in a given image
            -> To identify Objects in the given image.
            -> Description the image
            -> You can ask to write a blog from the image
            
--> 3. sen-analysis.py
            This analyses the sentiment of the given text as POSITIVE, NEGATIVE and NEUTRAL.

## Contributing

You are free add any other different apps. You can use your own fine-tuned model.

## License

License is mentioned in LICENSE file.
