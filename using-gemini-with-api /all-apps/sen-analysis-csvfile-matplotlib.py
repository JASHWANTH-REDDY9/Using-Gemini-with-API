import os
import pandas as pd
import google.generativeai as genai
import time
from google.api_core.exceptions import ResourceExhausted
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure GenAi with your API key
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Function to load Gemini Pro model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    chat = model.start_chat(history=[
        {"role": "user", "parts": ["Analyze the sentiment of the following Tweets and classify them as POSITIVE, NEGATIVE, or NEUTRAL. \"It's so beautiful today!\""]},
        {"role": "model", "parts": ["POSITIVE"]},
        {"role": "user", "parts": ["\"Senior RSS leader attacks BJP on Lok Sabha election results: 'Those who became arrogant...'\""]},
        {"role": "model", "parts": ["NEGATIVE"]},
        {"role": "user", "parts": ["\"Shiv Sena’s Abdul Sattar worked against the BJP candidate during the Lok Sabha elections, says BJP leader.'\""]},
        {"role": "model", "parts": ["NEGATIVE"]},
        {"role": "user", "parts": ["\"BJP leaders told to prepare for local body polls.\""]},
        {"role": "model", "parts": ["NEUTRAL"]},
        {"role": "user", "parts": ["\"Genuine introspection and strategy needed to revive BJP’s fortunes: Devendra Fadnavis.\""]},
        {"role": "model", "parts": ["NEUTRAL"]},
        {"role": "user", "parts": ["\"Vikravandi bypoll | PMK will contest on behalf of NDA, says T.N. BJP president K. Annamalai.\""]},
        {"role": "model", "parts": ["POSITIVE"]},
    ])
    chat.send_message(question)
    if chat is None:
        return "Error: Unable to initiate chat with Gemini Pro model."
    response = chat.last
    if response is None:
        return "Error: No response received from Gemini Pro model."
    return response.text

# Function to perform sentiment analysis on a dataframe
def perform_sentiment_analysis(df, text_column):
    sentiments = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    retry_limit = 5

    for i, text in enumerate(df[text_column]):
        retry_count = 0
        while retry_count < retry_limit:
            try:
                response_text = get_gemini_response(text)
                if 'positive' in response_text.lower():
                    sentiments['POSITIVE'] += 1
                elif 'negative' in response_text.lower():
                    sentiments['NEGATIVE'] += 1
                else:
                    sentiments['NEUTRAL'] += 1
                break
            except ResourceExhausted:
                retry_count += 1
                wait_time = 2 ** retry_count  # Exponential backoff
                time.sleep(wait_time)
                if retry_count == retry_limit:
                    print("API quota exhausted. Try again later.")
                    return sentiments
            time.sleep(1)  # Add delay between API calls

    total = sentiments['POSITIVE'] + sentiments['NEGATIVE'] + sentiments['NEUTRAL']
    
    sentiment_percentages = {
        'POSITIVE': (sentiments['POSITIVE'] / total) * 100,
        'NEGATIVE': (sentiments['NEGATIVE'] / total) * 100,
        'NEUTRAL': (sentiments['NEUTRAL'] / total) * 100
    }
    
    return sentiment_percentages

# Main function to run sentiment analysis and plot the results
def main():
    file_path = "path to your file"  #only csv file
    text_column = "column name"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    if text_column not in df.columns:
        print(f"Column '{text_column}' not found in the uploaded CSV file.")
        return

    sentiment_percentages = perform_sentiment_analysis(df, text_column)
    
    if sentiment_percentages:
        print("Sentiment Analysis Result:")
        for sentiment, percentage in sentiment_percentages.items():
            print(f"{sentiment}: {percentage:.2f}%")

        # Plotting the results in a pie chart
        labels = sentiment_percentages.keys()
        sizes = sentiment_percentages.values()
        colors = ['#ff9999','#66b3ff','#99ff99']
        explode = (0.1, 0, 0)  # explode 1st slice

        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Sentiment Analysis Results")
        plt.show()

if __name__ == "__main__":
    main()

