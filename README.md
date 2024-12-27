# notes_GPT

## Overview

This repo contains a simple script that can be used to create simple HTML for notes based on transcripts from videos. The prompts can be customised to suit your needs (for example, in this version I instruct the LLM to make special note of due dates for the class). This HTML can be used as sharable media for study purposes, summarizing pertinent information from class lectures. Neat, HUH?

### Stack

<img src=https://cdn.freebiesupply.com/logos/large/2x/python-3-logo-png-transparent.png height=100 />

![Selenium](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Selenium_logo.svg/512px-Selenium_logo.svg.png)

<img src=https://static.vecteezy.com/system/resources/previews/022/227/364/non_2x/openai-chatgpt-logo-icon-free-png.png height=100/>

## Using This Tool

This tool is simple to use from the command line. After cloning this repo and editing the very few config vars (be sure to rename the config file to "config.py" too), one can simply use the commandline to execute the script to scrape the  main script (gpt_notes.py) and enter any pertinent details as arguments. 
### Clone the Repository

  If you are unsure of how to do this, or are new to github, instructions can be found (here)[https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository] from GitHub's documentation.

### Edit the Config

  1) Make sure you rename the file to config.py wo that it is imported into the other python scripts.
  2) You can add an openAI API key here, but it is a bit more secure to store it as an environment variable. Currentlt, this program doesn't handle environment variables, though it would be fairly simple to implement and is on the list of improvements to make.
  3) If you are getting the transcript from panopto, add your username and password. Again, environment variables would be more secure and I've added it to the docket to handle them as the default case.
    - I wrote this as a tool for my classes at UofL, where panopto video is a standard tool, but any transcript saved as a .txt file could be used in the note making script to create HTML
  4) Add a system prompt. Currently, these are saved as text files, then the file is read into memory when running the script to prompt chat. The idea was to save various sys prompts for different purposes to simplify the process of generating these html pages for different classes.

### Fetch the trancript

  Currently the process it to save the transcript to txt file but this can definitely be streamlined by saving the tracript directly to memory... I'm writing the readme long after creating this tool and have since gotten a little... better at programming.
Honestly, I'll need to try this again to refresh my memory on the usage (oops). the notation wasn't great on creation and it's a little unclear. Again, this progream could definitely stand some improvements.

  > Usage: python3 panopto_notes.py <Panopto URL?> <Path to save notes?>

### Generate Notes

  Once the trancript is optained, it can be chunked and sent to an LLM for note creation using the script below.

  > Usage: python3 gpt_notes.py <path_transcript_to_send_to_ChatGPT> <path_system_prompt>

## Example output:

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSE130 Exam 1 Practice Exam</title>
</head>
<body>

<h1>CSE130 Exam 1 Practice Exam</h1>

<h2>Instructions:</h2>
<ol>
  <li>This practice exam is designed to help you prepare for Exam 1 in CSE130.</li>
  <li>Answer all questions to the best of your ability.</li>
  <li>Good luck!</li>
</ol>

<h2>Section 1: True or False (1 mark each)</h2>
<ol>
  <li>True or False: Variables in C can have spaces in their names.</li>
  <li>True or False: Constants in C are mutable.</li>
  <li>True or False: The order of precedence for operations in C follows the acronym PEMDAS.</li>
  <li>True or False: Relational operators in C return Boolean values.</li>
  <li>True or False: The do-while loop is guaranteed to execute at least once.</li>
</ol>

<h2>Section 2: Multiple Choice (1 mark each)</h2>
<ol>
  <li>What does the 'if' statement in C evaluate?
    <ul>
      <li>a) Relational expression</li>
      <li>b) Boolean expression</li>
      <li>c) Arithmetic expression</li>
      <li>d) None of the above</li>
    </ul>
  </li>
  <!-- Repeat for other multiple-choice questions -->
</ol>

<h2>Section 3: Trace Your Code (2 marks each)</h2>
<ol>
  <li>What will be the output of the following code?
    <pre><code>#include &lt;stdio.h&gt;

int main() {
    int x = 5;
    if (x &gt; 3 &amp;&amp; x &lt; 10) {
        printf("x is between 3 and 10");
    } else {
        printf("x is not between 3 and 10");
    }
    return 0;
}</code></pre>
  </li>
  <!-- Repeat for other trace-your-code questions -->
</ol>

<h2>Section 4: Bugging Questions (2 marks each)</h2>
<ol>
  <li>Identify and correct the syntax error(s) in the following code snippet:
    <pre><code>#include &lt;stdio.h&gt;

int main() {
    int x = 10;
    if (x = 5) {
        printf("x is 5");
    } else {
        printf("x is not 5");
    }
    return 0;
}</code></pre>
  </li>
  <!-- Repeat for other bugging questions -->
</ol>

<h2>Section 5: Writing Code (4 marks each)</h2>
<ol>
  <li>Write a C function named `max` that takes two integers as arguments and returns the larger of the two.</li>
  <li>Write a C function named `reverseArray` that takes an array of integers and its size as arguments and reverses the elements in the array.</li>
</ol>

</body>
</html>


## Ideas for Improvement:

### Pending:

1) Clean up code:
  - Config:
    - There is no need to read the config file as JSON. It can simply be saved as a python file and imported.
    - Handle the openAI API key and panopto credentials as environment variables by default.
    - Simplify the sys_prompt env var... there are extra steps here. 
  - panopto_notes:
    - Unneceesary Selenium commands to find body in SSO function. Can be done once.
    - Can the get_title function be simplified? Not sure but it looks prettty verbose.
  - gpt_notes:
    - config as import can reduce verbosity
      - openAi client can be config var now too
