import os
import openai
from dotenv import load_dotenv

# --- SETUP ---
# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = api_key

# --- GAME ENGINE ---

def get_ai_response(story_context):
    """
    Sends the story context to the AI and gets the next part of the story.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access and want higher quality
            messages=story_context,
            temperature=0.7,  # A bit of creativity
            max_tokens=250    # Limit the length of the response
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred with the AI model: {e}"

def main():
    """Main game loop."""
    
    # The initial system prompt that sets the stage and rules for the AI
    system_prompt = {
        "role": "system",
        "content": (
            "You are an expert dungeon master for a text-based adventure game. "
            "Describe the world in a fun, creative, and engaging way. "
            "Start by describing the player's initial location. "
            "Your descriptions should be 2-4 sentences long. "
            "Always end your response by asking the player 'What do you do next?'"
        )
    }
    
    # The history of the conversation, starting with the system prompt
    story_history = [system_prompt]
    
    print("--- Welcome to the AI-Powered Infinite Adventure ---")
    print("Type 'quit' or 'exit' to end your journey.\n")

    # Get the initial story setup from the AI
    print("The AI Dungeon Master is conjuring your world...")
    initial_story = get_ai_response(story_history)
    print(f"\n{initial_story}\n")

    # Add the AI's first response to the history
    story_history.append({"role": "assistant", "content": initial_story})

    while True:
        player_action = input("> ")
        
        if player_action.lower() in ["quit", "exit"]:
            print("\nFarewell, adventurer!")
            break
            
        # Add the player's action to the story history
        story_history.append({"role": "user", "content": player_action})
        
        print("\nThe AI Dungeon Master is thinking...")
        
        # Get the AI's response to the player's action
        ai_narrative = get_ai_response(story_history)
        
        print(f"\n{ai_narrative}\n")
        
        # Add the AI's narrative to the history to maintain context
        story_history.append({"role": "assistant", "content": ai_narrative})

        # To prevent the context from getting too long (and expensive),
        # we can trim the history. Let's keep the last 10 exchanges.
        if len(story_history) > 20: # 1 system + 10 user/assistant pairs
            story_history = [system_prompt] + story_history[-20:]


if __name__ == "__main__":
    main()