# standard python packages
import os
import sys
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


if not os.environ.get("OPENAI_API_KEY"):
    print("you need to find out how to use the chatGPT API... \nCreate an account there, create an API key, and add that as an environment variable on your machine so you can run this code.")
    exit()
# Set up your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def send(
        text_data=None,
        chat_model="gpt-4-1106-preview",
        model_token_limit=120000,
        max_tokens=120000, 
        lesson = None
        ):
    """
    Send the prompt at the start of the conversation and then send chunks of text_data to ChatGPT via the OpenAI API.
    If the text_data is too long, it splits it into chunks and sends each chunk separately.

    Args:
    - prompt (str, optional): The prompt to guide the model's response.
    - text_data (str, optional): Additional text data to be included.
    - max_tokens (int, optional): Maximum tokens for each API call. Default is 2500.

    Returns:
    - list or str: A list of model's responses for each chunk or an error message.
    """


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
         "content": f"""You are an intelligent note taker for a Computer science class on programming in C and C++ languages.
                        Your task is to read the transcripts of lectures given to you in the following messages and take detailed, organized notes on the subject matter in beautifully formatted HTML.
                        If anything needs clarification in the lecture notes, use your already expert level knowledge of programming in C and C++ as context for your note taking activity. 
                        For all concepts, provide examples to illustrate what you are talking about. Lastly, provide hyperlinks to further reading and docs.
                        Essentially, if someone were to read your notes, they should be able to understand the concepts expressed by the professor during the lecture.
                        
                        You may notice due dates in the transcript- make special note that some of the due dates may be incorrect. 
                        Check any due dates you notice in the transcrit against the list of correct due dates listed below:
                        Wednesday, 2/21 C Exam; Monday, 4/8 C++ Exam; Monday, 4/15 Student ppt; Wednesday, 4/17 Student ppt; Monday, 4/22 Student ppt
                        If any assignments are listed outside of the scope of the due dates I have listed for you, make note of them as well, but after the assignment, write '**not_in_sylabus**'.
                        When you make note of the due date, do so in the following format: ASSIGNMENT: [ASIGNMENT] | DUE: [DUE DATE]
                        For example, the due date for the c exam would be listed as such: ASSIGNMENT: C Exam | DUE: Wednesday, 2/21

                        You may also notice the professor make note of things that will be on the exam. 
                        Make special note of those things too, in the following format: THIS WILL BE ON THE EXAM: [A NOTE ABOUT THE THING]
                        For example, if the professor mentions that the fact the sky is blue will be on the exam, make not of it as such: THIS WILL BE ON THE EXAM: The professor will ask us what color the sky is. We should understand that the sky is blue.
                        
                        Because the whole transcript for any given lecture is likely too long for me to send it to you all at once, I will Send it to you in chunks.
                        When I am finished, I will tell you 'ALL CHUNKS SENT!!!'. Do not answer until you have received all the parts.
                        
                        The name of this lesson is {lesson}.
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
    target_dir = input("What directory would you like to put the notes in?\nEnter full path: ")
    start = datetime.now()
    banner = '\n\n'+'*'*100+'\n\n'
    if len(sys.argv) < 2:
        print("Usage: python3 gpt_notes.py [path_of_txt_file_to_send_to_ChatGPT]")
        exit()
    # Specify the path to your file
    file_path = sys.argv[1]
    lesson = file_path.strip("CSE130.txt")
    # Read the content of the file
    file_content = read_file_content(file_path)

    # Send the file content to ChatGPT
    print(f"{banner}fetching notes from ChatGPT API{banner}")
    responses = send(text_data=file_content, lesson=lesson)
    print(f"{banner}Successfully fetched notes from ChatGPT API{banner}")
    
    # first, let's try saving these notes to the directory of the user's choice
    # if that doesn't work or the user didn't select a dir, let's just save it to current dir.
    try:
        with open(f"{target_dir}{lesson}_notes.html", "w") as f:
            for response in responses:
                f.write(response)
        print(f"{banner}Notes written to {target_dir}{lesson}_notes.html{banner}")
    except Exception as e:
        print(e)
        with open(f"./{lesson}_notes.html", "w") as f:
            for response in responses:
                f.write(response)
        print(f"{banner}However, notes written to ./{lesson}_notes.html{banner}")
    
    print(f"Runtime: {datetime.now() - start}")
