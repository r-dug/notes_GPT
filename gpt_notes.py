# standard python packages
import os
import sys
import json
import re
from datetime import datetime

# check for required non standard packages, if not found, install then import them.
required_packages = ["openai", "tiktoken"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        os.system(f"pip install {package}")

        os.system(f"pip install {package}")
import tiktoken
from openai import OpenAI

def send(
        text_data=None,
        chat_model="gpt-4-1106-preview",
        max_tokens=120000, 
        lesson = None
        ):
    
    if not text_data:
        return "Error: Text data is missing. Please provide some text data."

    # Initialize the tokenizer
    tokenizer = tiktoken.encoding_for_model(chat_model)

    # Encode the text_data into token integers
    token_integers = tokenizer.encode(text_data)

    # Split the token integers into chunks based on max_tokens
    chunk_size = max_tokens 
    chunks = [
        token_integers[i : i + chunk_size]
        for i in range(0, len(token_integers), chunk_size)
    ]

    # Decode token chunks back to strings
    chunks = [tokenizer.decode(chunk) for chunk in chunks]
    responses = []
    messages = [
        {"role": "system", 
         "content": f"""{sys_prompt}{lesson}.
                        """}
    ]

    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})
        
    # Add the final "ALL PARTS SENT" message
    messages.append({"role": "user", "content": "ALL CHUNKS SENT!!!"})
    response = client.chat.completions.create(model=chat_model, messages=messages)
    final_response = response.choices[0].message.content
    responses.append(final_response)

    return responses
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Use the function
if __name__ == "__main__":

    with open('config.json', 'r') as file:
        config_data = json.load(file)
    OPENAI_API_KEY = config_data['OPENAI_API_KEY']

    sys_prompt_path = config_data['sys_prompt']
    sys_prompt = read_file_content(sys_prompt_path)

    if not OPENAI_API_KEY:
        print("you need to find out how to use the chatGPT API... \nCreate an account there, create an API key, and add that as an environment variable on your machine so you can run this code.")
        exit()
    if not sys_prompt:
        print("you need to change the config file to contain the path to the desired system prompt...")
        exit()

    # Set up your OpenAI API key
    client = OpenAI(
        # This is the default and can be omitted
        api_key=OPENAI_API_KEY,
    )

    target_dir = input("\n\nWhat directory would you like to put the notes in?\nRelative path is fine. enter nothing to save to default notes file\nPath: ")
    start = datetime.now()
    banner = '\n\n'+'*'*100+'\n\n'
    if len(sys.argv) < 2:
        print("Usage: python3 gpt_notes.py [path_transcript_to_send_to_ChatGPT] [path_system_prompt]")
        exit()
    
    # get lecture transcript
    file_path = sys.argv[1]
    file_content = read_file_content(file_path)
    
    # specify name of lesson 
    pattern = r'[^\\\/]*(?=\.\w+$)'
    lesson = re.search(pattern, file_path).group()

    # Send the file content to ChatGPT
    print(f"{banner}fetching notes from ChatGPT API{banner}")
    responses = send(text_data=file_content, lesson=lesson)
    print(f"{banner}Successfully fetched notes from ChatGPT API{banner}")
    
    # first, let's try saving these notes to the directory of the user's choice
    # if that doesn't work or the user didn't select a dir, let's just save it to current dir.
    if target_dir:
        with open(f"{target_dir}{lesson}_notes.html", "w") as f:
            for response in responses:
                f.write(response)
        print(f"{banner}Notes written to {target_dir}{lesson}_notes.html{banner}")
    else:
        with open(f"./../notes/html/{lesson}_notes.html", "w") as f:
            for response in responses:
                f.write(response)
        print(f"{banner}However, notes written to ./../notes/{lesson}_notes.html{banner}")
    
    print(f"Runtime: {datetime.now() - start}")
