import requests
import json
import time

# Set your API key
api_key = 'YOUR_API_KEY'
headers = {
    'Authorization': f'Bearer {api_key}',
    'OpenAI-Beta': 'assistants=v1'
}

# Step 1: Upload the CSV file
file_path = "plots.csv"
with open(file_path, 'rb') as file:
    files = {'file': file, 'purpose': (None, 'assistants')}
    file_response = requests.post('https://api.openai.com/v1/files', headers=headers, files=files)
file_id = file_response.json()['id']

# Step 2: Create a custom assistant
data = {
    "model": "gpt-4-1106-preview",
    "instructions": "Based on the provided CSV propose a list of the most suitable lands for the user based on the provided prompt, and return an array of IDs that are most likely what the user wants. Return only a valid JSON array of IDs, nothing else",
    "tools": [{"type": "code_interpreter"}],
    "file_ids": [file_id]
}
assistant_response = requests.post('https://api.openai.com/v1/assistants', headers=headers, json=data)
assistant_id = assistant_response.json()['id']

# Step 3: Create a Thread
user_message = "I want to find a plot from 800sq m to 1600sq, close to city, I have a budget around 60k euro."
thread_data = {"messages": [{"role": "user", "content": user_message}]}
thread_response = requests.post('https://api.openai.com/v1/threads', headers=headers, json=thread_data)
thread_id = thread_response.json()['id']

# Step 4: Create a Run
run_response = requests.post(f'https://api.openai.com/v1/threads/{thread_id}/runs', headers=headers, json={"assistant_id": assistant_id})
run_id = run_response.json().get('id')

# Polling for run completion
completed = False
while not completed:
    run_status_response = requests.get(f'https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}', headers=headers)
    run_status = run_status_response.json()
    
    if run_status.get('status') == 'completed':
        completed = True
    else:
        time.sleep(5)  # Wait for 5 seconds before polling again

# Step 5: Retrieve the Results
messages_response = requests.get(f'https://api.openai.com/v1/threads/{thread_id}/messages', headers=headers)
for message in messages_response.json()['data']:
    if 'text' in message and 'value' in message['text']:
        content = message['text']['value']
        try:
            ids = json.loads(content)
            if isinstance(ids, list):
                print(ids)
            else:
                print("Response is not in the expected format:", content)
        except json.JSONDecodeError:
            print("Failed to parse JSON from response:", content)
    else:
        print("Message format is unexpected:", message)
