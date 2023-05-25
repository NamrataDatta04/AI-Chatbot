import openai
import time
import string
from functools import lru_cache

# Set OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Initialize chat messages list
messages = []

# Get system message from user
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")

# List to store response times for monitoring
response_times = []

# Function to process user input data
@lru_cache(maxsize=128)  # Caching function results
def process_data(input_data):
    # Convert input to lowercase
    processed_data = input_data.lower()
    
    # Remove punctuation
    processed_data = processed_data.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize the input
    tokens = processed_data.split()
   
    return processed_data

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

        # Get response from OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        end_time = time.time()  # Stop measuring response time
        response_time = end_time - start_time  # Calculate response time
        response_times.append(response_time)  # Store response time for monitoring

        # Get reply from the response
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")

        # Process user input
        processed_input = process_data(user_input)

        # Cache frequently accessed results
        processed_result = process_data.cache_info()
        if processed_result.hits > 10:
            pass
        
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
                openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": correct_response}
                    ]
                )
    
    # Ask another question or exit
    print("Press Enter to ask a new question or type 'quit()' to exit.")
    user_input = input()

    if user_input == "quit()":
        break

    # Reset chat messages
    messages = []
    messages.append({"role": "system", "content": system_msg})
