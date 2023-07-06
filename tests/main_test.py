import openai

# Configure the OpenAI library
openai.api_type = "azure"
openai.api_key = "your-azure-api-key"
openai.api_base = "http://localhost:8000"  # Adjust to your Azure FastAPI server address
openai.api_version = "2023-05-15"

def test_chat_completion():
    data = {
        "deployment_id": "your-deployment-id",
        "model": "gpt-3.5-turbo",
        # "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }

    chat_completion = openai.ChatCompletion.create(**data)

    assert chat_completion['choices'][0]['message']['role'] == "assistant", "No assistant response"
    assert "Los Angeles Dodgers" in chat_completion['choices'][0]['message']['content'], "Incorrect or missing information"
    print(f"response={chat_completion}")

test_chat_completion()