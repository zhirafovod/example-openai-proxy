import openai
import numpy as np
from faker import Faker
import time
import random
import threading

NUM_THREADS = 3
MODELS = ['text-davinci-003', 'text-curie-003', 'gpt-3.5-turbo']

faker = Faker()
openai.api_type = "azure"
openai.api_base = "http://localhost:8000"  # Adjust to your Azure FastAPI server address
openai.api_version = "2023-05-15"


def make_request():
    openai.api_key = "fake-one"

    num_messages = np.random.randint(1, 5)
    # select a random api_key to use
    openai.api_key = "fake-one-" + str(np.random.randint(1, 10))

    for _ in range(num_messages):  # 5 tests
        model = np.random.choice(MODELS)
        
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        num_messages = np.random.randint(1, 6)  # Randomly generate a number of messages from 1 to 5

        for _ in range(num_messages):
            num_words = np.random.randint(1, 4)  # Randomly generate a length from 1 to 3
            sentence = faker.sentence(nb_words=num_words, variable_nb_words=False)
            messages.append({"role": "user", "content": sentence})
            
            data = {
                "deployment_id": "your-deployment-id",
                "model": model,
                "messages": messages
            }

            chat_completion = openai.ChatCompletion.create(**data)
            print(f"Response from {model}: {chat_completion.choices[0].message['content']}")
            
            # Append assistant's response to the messages for the next query
            messages.append({"role": "assistant", "content": chat_completion.choices[0].message['content']})

            # Random delay between 30 and 90 seconds
            time_delay = random.randint(30, 90)
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