# Carmine Silano
# Feb 4, 2025

# This file is to make requests to an ollama server running locally

import requests
import json
OMODEL="dolphin3"
OSTREAM=False

PREPROMPT = []
# Load the JSON configuration file
with open("preprompts.json", "r") as file:
    PREPROMPT = json.load(file)

def query_ollama(prompt, preload):
   
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "prompt": PREPROMPT[preload] + prompt,
        "model": OMODEL,  
        "stream": OSTREAM
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")

# For testing
if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    try:
        reply = query_ollama(user_prompt)
        print("Response:", reply)
    except Exception as e:
        print("An error occurred:", e)
