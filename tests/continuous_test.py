import openai
import numpy as np
from faker import Faker
import time
import random
import threading

NUM_THREADS = 3
MODELS = ['text-davinci-003', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo']

faker = Faker()
openai.api_type = "azure"
openai.api_base = "http://localhost:8000"  # Adjust to your Azure FastAPI server address
openai.api_version = "2023-05-15"


def make_request():
    openai.api_key = "fake-one"

    num_messages = 100
    # select a random api_key to use
    openai.api_key = "fake-one-" + str(np.random.randint(1, 10))

    while True:
        model = np.random.choice(MODELS)
        
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        conversation_length = np.random.randint(1, 6)  # Randomly generate a number of messages from 1 to 5

        for n in range(conversation_length):
            num_messages -= 1
            if num_messages <= 0:
                print("successfully generated all messages")
                exit(0)
            num_words = np.random.randint(1, 4)  # Randomly generate a length from 1 to 3
            sentence = faker.sentence(nb_words=num_words, variable_nb_words=False)
            messages.append({"role": "user", "content": f"""Respond only with 3 words or less to this sentence="{sentence}"."""})
            
            if model != 'text-davinci-003':
                data = {
                    "deployment_id": "your-deployment-id",
                    "model": model,
                    "messages": messages
                }
                chat_completion = openai.ChatCompletion.create(**data)
                response_text = chat_completion.choices[0].message['content']
            else:
                data = {
                    "deployment_id": "your-deployment-id",
                    "model": model,  # Specify engine here
                    "prompt": sentence,
                }
                chat_completion = openai.Completion.create(**data)
                response_text = chat_completion.choices[0].text.strip()

            # Random delay between 30 and 90 seconds
            time_delay = random.randint(30, 90)
            
            print(f"Response from {model} to conversation message {n} with sentence {sentence} was: {response_text}\nWaiting for {time_delay} seconds to generate message {num_messages}")
            
            # Append assistant's response to the messages for the next query
            messages.append({"role": "assistant", "content": response_text})

            time.sleep(time_delay)

# Run the function in 5 threads
threads = []
for _ in range(NUM_THREADS):
    t = threading.Thread(target=make_request)
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()
