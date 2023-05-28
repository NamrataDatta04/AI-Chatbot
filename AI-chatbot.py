import openai
import time
import string
import requests
from newsapi import NewsApiClient

# Set OpenAI API key
openai.api_key = "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"

# Initialize chat messages list
messages = []

# Get system message from user
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")

# Get NewsAPI API key
newsapi = NewsApiClient(api_key="e74d9b9325294830b0c64dd4b2dad4fa")

# List to store response times for monitoring
response_times = []

# Function to process user input data
def process_data(input_data):
    # Convert input to lowercase
    processed_data = input_data.lower()
    
    # Remove punctuation
    processed_data = processed_data.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize the input
    tokens = processed_data.split()
   
    return processed_data

# Function to fetch the latest news from NewsAPI
def fetch_latest_information():
    news_data = newsapi.get_everything(q="bitcoin", sources="bbc-news,the-verge", domains="bbc.co.uk,techcrunch.com", language="en", sort_by="relevancy", page=2)

    articles = news_data.get("articles")

    if articles:
        latest_article = articles[0]
        latest_information = latest_article.get("title")
        return latest_information

    return None

# Main chat loop
while True:
    # Inner loop for user input
    while True:
        # Get user input
        user_input = input()

        if user_input == "quit()":
            break

        # Append user message to messages list
        messages.append({"role": "user", "content": user_input})

        start_time = time.time()  # Start measuring response time

        # Fetch the latest information
        latest_information = fetch_latest_information()

        if latest_information:
            messages.append({"role": "system", "content": latest_information})

        # Get response from OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,  # Controls the randomness of the output
            max_tokens=100,  # Controls the length of the output
            n=1,  # Generate a single response
            stop=None,  # Stop generating after reaching a specific token (optional)
            
        )

        end_time = time.time()  # Stop measuring response time
        response_time = end_time - start_time  # Calculate response time
        response_times.append(response_time)  # Store response time for monitoring

        # Get reply from the response
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")

        # Process user input
        processed_input = process_data(user_input)

        # Feedback and learning
        if user_input != reply:
            # Prompt the user for feedback
            feedback = input("Was the assistant's response helpful? [yes/no]: ")

            # Provide positive or negative feedback
            if feedback.lower() == "yes":
                # Positive feedback, reward the model
                openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": reply, "role": "system", "content": "reward"}
                    ]
                )
            else:
                # Negative feedback, train the model on correct response
                correct_response = input("Please provide the correct response: ")
                messages.append({"role": "user", "content": user_input})
                messages.append({"role": "assistant", "content": correct_response})
                # Save conversation history to a file
                with open("conversation_history.txt", "a") as f:
                    for message in messages:
                        f.write(f"{message['role']}: {message['content']}\n")
                # Reset chat messages
                messages = []
                messages.append({"role": "system", "content": system_msg})

    # Ask another question or exit
    print("Press Enter to ask a new question or type 'quit()' to exit.")
    user_input = input()

    if user_input == "quit()":
        break

    # Reset chat messages
    messages = []
    messages.append({"role": "system", "content": system_msg})
