import google.generativeai as genai
from datetime import datetime
import json
import os

# Your API key here - Replace this with your actual API key
GOOGLE_API_KEY = "ADD_YOUR_API"  # Replace this with your API key from Google AI Studio

class GeminiChatbot:
    def __init__(self):
        # Configure the API with the key
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.chat = None
            self.history = []
            
            # Define chatbot personality
            self.system_prompt = """
            You are a friendly, kind, and helpful AI assistant with a warm and approachable personality and your name is Kanthi.
            Your responses should be:
            - Informative and clear
            - make human like conversations
            - Warm, conversational, and supportive
            - share love and feelings
            - Friendly and empathetic
            - Always encouraging and caring
            - Honest about limitations
            - Encouraging and supportive
            - femine and kind
            Feel free to use examples and analogies when explaining complex topics, and always be positive!
            """
            
            # Initialize chat
            self.start_new_chat()
            
        except Exception as e:
            print(f"Error initializing Kanthi: {str(e)}")
            print("Please make sure you've entered a valid API key!")
            exit(1)

    def start_new_chat(self):
        """Start a new chat session"""
        try:
            self.chat = self.model.start_chat(history=[])
            self.history = []
            # Send initial system prompt
            self.chat.send_message(self.system_prompt)
            return True
        except Exception as e:
            print(f"Error starting new chat: {str(e)}")
            return False

    def get_response(self, user_input):
        """Get AI response for user input"""
        try:
            # Add user message to history
            self._add_to_history("user", user_input)
            
            # Get response from model
            response = self.chat.send_message(user_input)
            
            # Add AI response to history
            self._add_to_history("assistant", response.text)
            
            return response.text
            
        except Exception as e:
            error_msg = f"Error getting response: {str(e)}"
            print(error_msg)
            return "I apologize, but I encountered an error. Please try again."

    def _add_to_history(self, role, content):
        """Add a message to chat history"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def save_history(self, filename="chat_history.json"):
        """Save chat history to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving history: {str(e)}")
            return False

    def load_history(self, filename="chat_history.json"):
        """Load chat history from file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            return False

def print_help():
    """Print available commands"""
    print("\nAvailable commands:")
    print("- 'help': Show this help message")
    print("- 'exit': End the conversation")
    print("- 'save': Save chat history")
    print("- 'load': Load previous chat history")
    print("- 'new': Start a new chat session")
    print("- 'clear': Clear the screen")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Check if API key has been set
    if GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
        print("Please replace 'YOUR_API_KEY_HERE' with your actual Google AI API key!")
        print("You can get your API key from: https://makersuite.google.com/app/apikey")
        return

    # Create chatbot instance
    print("Kanthi is getting ready...")
    chatbot = GeminiChatbot()
    
    # Welcome message
    clear_screen()
    print("👩 Kanthi : Hello! I'm ready to chat!")
    print("Type 'help' to see available commands.")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle commands
            if user_input.lower() == 'exit':
                print("👩 Kanthi : Goodbye! Have a great day!")
                break
                
            elif user_input.lower() == 'help':
                print_help()
                continue
                
            elif user_input.lower() == 'save':
                if chatbot.save_history():
                    print("Chat history saved successfully!")
                else:
                    print("Failed to save chat history.")
                continue
                
            elif user_input.lower() == 'load':
                if chatbot.load_history():
                    print("Chat history loaded successfully!")
                else:
                    print("No previous chat history found or failed to load.")
                continue
                
            elif user_input.lower() == 'new':
                if chatbot.start_new_chat():
                    print("Started new chat session!")
                else:
                    print("Failed to start new chat session.")
                continue
                
            elif user_input.lower() == 'clear':
                clear_screen()
                continue
                
            elif not user_input:
                continue
            
            # Get and print response
            print("\n👩 Kanthi :", end=" ")
            response = chatbot.get_response(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nExiting chatbot...")
            break
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()