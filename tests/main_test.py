from openai import AzureOpenAI

client = AzureOpenAI(api_key="your-azure-api-key",
azure_endpoint="http://localhost:8000",
api_version="2023-05-15")

# Configure the OpenAI library
  # Adjust to your Azure FastAPI server address

def test_chat_completion():
    data = {
        "model": "gpt-3.5-turbo",
        # "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }

    chat_completion = client.chat.completions.create(**data)

    assert chat_completion.choices[0].message.role == "assistant", "No assistant response"
    assert "Los Angeles Dodgers" in chat_completion.choices[0].message.content, "Incorrect or missing information"
    print(f"response={chat_completion}")


def test_regular_completion():
    data = {
        "deployment_id": "your-deployment-id",
        "model": "text-davinci-003",
        "prompt": "Who won the world series in 2020?"
    }

    regular_completion = client.completions.create(**data)

    assert "Los Angeles Dodgers" in regular_completion.choices[0].text.strip(), "Incorrect or missing information"
    print(f"response={regular_completion}")


test_chat_completion()
test_regular_completion()
