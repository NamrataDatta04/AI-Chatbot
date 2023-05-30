import openai
import time
import string
from googlesearch import search

# Set OpenAI API key
openai.api_key = "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"

# Initialize chat messages list
messages = []

# Get system message from user
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")

# Function to process user input data
def process_data(input_data):
    # Convert input to lowercase
    processed_data = input_data.lower()
    
    # Remove punctuation
    processed_data = processed_data.translate(str.maketrans("", "", string.punctuation))
    
    return processed_data

# Function to search Google
def google_search(query):
    results = search(query, num_results=1)
    if results:
        return results[0]
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

        # Get response from OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,  # Controls the randomness of the output
            max_tokens=100,  # Controls the length of the output
            n=1,  # Generate a single response
            stop=None,  # Stop generating after reaching a specific token (optional)
        )

        # Get reply from the response
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")

        # Process user input
        processed_input = process_data(user_input)

        # Search Google if the response is not helpful
        if user_input != reply:
            search_result = google_search(processed_input)
            if search_result:
                messages.append({"role": "system", "content": search_result})
                reply = search_result

        # Append assistant's reply to messages list
        messages.append({"role": "assistant", "content": reply})

    # Ask another question or exit
    print("Press Enter to ask a new question or type 'quit()' to exit.")
    user_input = input()

    if user_input == "quit()":
        break

    # Reset chat messages
    messages = []
    messages.append({"role": "system", "content": system_msg})
