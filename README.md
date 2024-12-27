# notes_GPT

## Overview

This repo contains a simple script that can be used to create simple HTML for notes based on transcripts from videos. The prompts can be customised to suit your needs (for example, in this version I instruct the LLM to make special note of due dates for the class). This HTML can be used as sharable media for study purposes, summarizing pertinent information from class lectures. Neat, HUH?

### Stack

<img src=https://cdn.freebiesupply.com/logos/large/2x/python-3-logo-png-transparent.png height=100 />

![Selenium](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Selenium_logo.svg/512px-Selenium_logo.svg.png)

<img src=https://static.vecteezy.com/system/resources/previews/022/227/364/non_2x/openai-chatgpt-logo-icon-free-png.png height=100/>

## Using This Tool

This tool is simple to use from the command line. After cloningthis repo, one can simply use the commandline to execute the main script (gpt_notes.py) and enter any pertinent details as arguments. 

  > Usage: python3 gpt_notes.py <path_transcript_to_send_to_ChatGPT> <path_system_prompt>


## Improvements:

### Pending:

1) Clean up code:
  - Config:
    - There is no need to read the config file as JSON. It can simply be saved as a python file and imported.
  - panopto_notes:
    - Unneceesary Selenium commands to find body in SSO function. Can be done once.
    - Can the get_title function be simplified? Not sure but it looks prettty verbose.
  - gpt_notes:
    - config as import can reduce verbosity
      - openAi client can be config var now too
