import json
import os
import requests
import sys

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama-server:11434")
url = f"{OLLAMA_HOST}/api/chat"

# Define user questions/messages
messages = [
    {"role": "user", "content": "What is 10 divided by 2?"},
    {"role": "user", "content": "Calculate the square root of 81?"},
    {"role": "user", "content": "Ping"},
    {"role": "user", "content": "ping"},
    {"role": "user", "content": "What is the area of a circle with radius 3?"},
    {"role": "user", "content": "What is 2 to the power of 10?"},
    {"role": "user", "content": "Tell me a story."},
    {"role": "user", "content": "Do you have the weather forecast for Galway today?"}
]

# Base URL for Ollama
#url = "http://localhost:11434/api/chat"

print("Streaming response from llama-AI:")

# Loop through each message and send one at a time to get individual responses
for msg in messages:
    print(f"\nUser Input: {msg['content']}")
    payload = {
        "model": "llama-AI",  #custom model name
        "messages": [msg],
        "stream": True
    }

    response = requests.post(url, json=payload, stream=True)

    # Print the streamed answer
    print("Answer: ", end="")
    if response.status_code == 200:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        print(json_data["message"]["content"], end="")
                except json.JSONDecodeError:
                    print(f"\nFailed to parse line: {line}")
        print()  # Newline after each answer
    else:
        print(f"Error {response.status_code}: {response.text}")

if sys.stdin.isatty():
    # Interactive mode
    print("\n🗣️ Now entering interactive mode. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("👋 Exiting chat.")
            break

        payload = {
            "model": "llama-AI",
            "messages": [{"role": "user", "content": user_input}],
            "stream": True
        }

        response = requests.post(url, json=payload, stream=True)

        # Print the streamed answer
        print("Answer: ", end="")
        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_data = json.loads(line)
                        if "message" in json_data and "content" in json_data["message"]:
                            print(json_data["message"]["content"], end="")
                    except json.JSONDecodeError:
                        print(f"\nFailed to parse line: {line}")
            print()  # Newline after each answer
        else:
            print(f"Error {response.status_code}: {response.text}")
