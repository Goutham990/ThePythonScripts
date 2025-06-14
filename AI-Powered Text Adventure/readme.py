# Infinite Story: The AI Text Adventure

 This is a text adventure game where the storyteller is a powerful AI (OpenAI's GPT model). Unlike traditional text adventures with fixed commands, you can type anything you want to do, and the AI will describe what happens next. The story is generated live, creating a unique and unpredictable experience every time.

## Features
- A truly open-ended adventure. Do anything, go anywhere.
- The AI acts as a creative and responsive Dungeon Master.
- The game state (your story so far) is maintained to provide context for the AI.

## Requirements
1.  Python 3.
2.  An **OpenAI API Key**. You can get one from [platform.openai.com](https://platform.openai.com/).
3.  The necessary Python libraries:
    ```bash
    pip install openai python-dotenv
    ```

## Setup
1.  **Create a `.env` file:** In the same directory as the script, create a file named `.env`.
2.  **Add your API Key:** Inside the `.env` file, add your OpenAI API key like this:
    ```
    OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
    ```
    This keeps your key secret and out of the source code.

## Usage
Simply run the script from your terminal:
```bash
python ai_adventure.py