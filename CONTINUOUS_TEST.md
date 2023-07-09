# Run continuous load test for OpenAI API Proxy

This is a basic description of how you can run a continuous load test for the API proxy using 3 models and both chat/completions and completions OpenAI APIs. 

The test is setup to run 3 pythin async "threads", each sending a small prompt to a randomly selected model, reusing the same conversation id for a conversation of random length (within 1 to 6 messages in a conversation)

## Models
### Completions APIs
[Completion APIs](https://platform.openai.com/docs/api-reference/completions/create) support only "text-davinci-003" model

### Chat Completions APIs
[Chat Completions APIs](https://platform.openai.com/docs/api-reference/chat) support gpt-3.5 family of models, "gpt-3.5-turbo" and "gpt-3.5-turbo-0613" are used in the test

## Run 
### Strart OpenAI Proxy
Ensure proper virtual environment is activated
```bash
source venv/bin/activate
```

Replace "<put-your-openai-key-here>" with a key from [openai api-keys](https://platform.openai.com/account/api-keys)
```bash
export OPENAI_API_KEY="<put-your-openai-key-here>"
```

Run the proxy, pointing it to your collector or OTEL backend - http://localhost:4318 in the example
```bash
OTEL_RESOURCE_ATTRIBUTES=service.name=example-openai-proxy OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"  opentelemetry-instrument --traces_exporter otlp_proto_http,console --metrics_exporter otlp_proto_http,console uvicorn main:app
```

### Run Continuous Load Test
Ensure proper virtual environment is activated
```bash
source venv/bin/activate
```

run the test
```bash
python tests/continuous_test.py
```

# Sample load test output

```bash
 python tests/continuous_test.py
Response from gpt-3.5-turbo to conversation message 0 with sentence Really. was: Yes, indeed.
Waiting for 37 seconds to generate message 99
Response from text-davinci-003 to conversation message 0 with sentence Institution deal provide. was: An institution deal is a contract between a lending institution (e.g
Waiting for 45 seconds to generate message 99
Response from text-davinci-003 to conversation message 0 with sentence Audience once try. was: Audience: Sure!
Waiting for 46 seconds to generate message 99
Response from gpt-3.5-turbo to conversation message 1 with sentence Discussion material. was: Interesting topic.
Waiting for 84 seconds to generate message 98
Response from gpt-3.5-turbo-0613 to conversation message 0 with sentence Probably group program. was: What's the program?
Waiting for 84 seconds to generate message 98
Response from text-davinci-003 to conversation message 0 with sentence Generation. was: h"

#include <sstream>
#include <string>
Waiting for 53 seconds to generate message 98
Response from text-davinci-003 to conversation message 1 with sentence General. was: No olvides leer las Normas del Foro
Waiting for 67 seconds to generate message 97
Response from gpt-3.5-turbo to conversation message 2 with sentence Base section. was: Foundation support.
Waiting for 49 seconds to generate message 97
Response from gpt-3.5-turbo to conversation message 0 with sentence Administration. was: How can I assist?
Waiting for 85 seconds to generate message 97
Response from text-davinci-003 to conversation message 2 with sentence Situation executive leader. was: An executive leader handles the day-to-day operations of an organization
Waiting for 78 seconds to generate message 96
Response from gpt-3.5-turbo to conversation message 3 with sentence Service join help. was: Assistance available!
Waiting for 88 seconds to generate message 96
Response from gpt-3.5-turbo to conversation message 1 with sentence By unit. was: What is it?
Waiting for 48 seconds to generate message 96
Response from text-davinci-003 to conversation message 3 with sentence Fish painting. was: Fish painting is an art in which an artist creates a painting using fish
Waiting for 31 seconds to generate message 95
Response from gpt-3.5-turbo to conversation message 4 with sentence Identify agreement next. was: Confirm details soon.
Waiting for 38 seconds to generate message 95
Response from gpt-3.5-turbo to conversation message 2 with sentence Certainly. was: Of course!
Waiting for 54 seconds to generate message 95
Response from text-davinci-003 to conversation message 4 with sentence Spend perform government. was: Government spending, or public expenditure, is any money spent by the government
Waiting for 61 seconds to generate message 94
Response from text-davinci-003 to conversation message 0 with sentence Physical difficult. was: Physical difficulty refers to a variety of physical health conditions, injuries, and
Waiting for 78 seconds to generate message 94
Response from gpt-3.5-turbo to conversation message 3 with sentence Sign cut professional. was: What's the request?
Waiting for 47 seconds to generate message 94
Response from text-davinci-003 to conversation message 0 with sentence Put create. was: php

<?php
// Get the data from the form
$name
Waiting for 90 seconds to generate message 93
Response from gpt-3.5-turbo to conversation message 4 with sentence Everyone near stuff. was: What's happening?
Waiting for 65 seconds to generate message 93
Response from text-davinci-003 to conversation message 0 with sentence Standard speech exactly. was: Good morning/afternoon/evening ladies and gentlemen. It is
Waiting for 87 seconds to generate message 93
Response from text-davinci-003 to conversation message 1 with sentence However former past. was: It is not possible to answer this question as it does not specify a
Waiting for 55 seconds to generate message 92
Response from text-davinci-003 to conversation message 0 with sentence Raise difference. was: Difference is the amount by which one thing is greater or less than
Waiting for 77 seconds to generate message 92
Response from text-davinci-003 to conversation message 1 with sentence Town. was: TabIndex = 103;
            this.btnAddTown.Text = "
Waiting for 72 seconds to generate message 92
Response from text-davinci-003 to conversation message 2 with sentence Line production go. was: Production go is the necessary step that has to be taken for a product
Waiting for 33 seconds to generate message 91
Response from gpt-3.5-turbo to conversation message 0 with sentence It avoid. was: Avoid it.
Waiting for 36 seconds to generate message 91
Response from text-davinci-003 to conversation message 3 with sentence Network own scientist. was: network

Science Network is an online platform founded with the goal of connecting scientists
Waiting for 50 seconds to generate message 90
Response from gpt-3.5-turbo-0613 to conversation message 0 with sentence Level. was: Same level.
Waiting for 67 seconds to generate message 91
Response from gpt-3.5-turbo to conversation message 1 with sentence See benefit well. was: Benefit is clear.
Waiting for 85 seconds to generate message 90
Response from gpt-3.5-turbo-0613 to conversation message 0 with sentence Tell let establish. was: Establish what?
Waiting for 61 seconds to generate message 89
```
