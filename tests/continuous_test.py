from openai import AzureOpenAI

client = AzureOpenAI(azure_endpoint="http://localhost:8000",
api_version="2023-05-15",
api_key="fake-one",
api_key="fake-one-" + str(np.random.randint(1, 10)))
import numpy as np
from faker import Faker
import time
import random
import threading

from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider

from api.utils.otel_instrumentation import tracer, tokens_counter, prompt_tokens_counter, completion_tokens_counter

RequestsInstrumentor().instrument()


NUM_THREADS = 3
MODELS = ['text-davinci-003', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo']

faker = Faker()
  # Adjust to your Azure FastAPI server address

def make_request():

    num_messages = 100
    # select a random api_key to use

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

            with tracer.start_as_current_span("openai_chat_completion"):
                if model != 'text-davinci-003':
                    data = {
                        "deployment_id": "your-deployment-id",
                        "model": model,
                        "messages": messages
                    }
                    chat_completion = client.chat.completions.create(**data)
                    response_text = chat_completion.choices[0].message.content
                else:
                    data = {
                        "deployment_id": "your-deployment-id",
                        "model": model,  # Specify engine here
                        "prompt": sentence,
                    }
                    chat_completion = client.completions.create(**data)
                    response_text = chat_completion.choices[0].text.strip()

            attributes = {"model": model, "chat_completion_id": chat_completion.id, "api_key": openai.api_key}
            tokens_counter.add(chat_completion.usage.total_tokens, attributes)
            prompt_tokens_counter.add(chat_completion.usage.prompt_tokens, attributes)
            completion_tokens_counter.add(chat_completion.usage.completion_tokens, attributes)

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
