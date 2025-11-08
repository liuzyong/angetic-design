#!/usr/bin/env python3
"""
Text Transformer Application
============================

This application captures selected text, sends it to an AI model for processing,
and replaces the original text with the transformed version.

Features:
- Cross-platform support (Windows, macOS, Linux)
- One-time text transformation with user guidance
- Multiple AI provider support (OpenAI, Anthropic, Google)
- Clipboard-based text manipulation
"""

import os
import sys
import time
import logging
import platform
import pyperclip
import pyautogui
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('text_transformer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TextTransformer:
    """Main class for text transformation application."""
    
    def __init__(self):
        """Initialize the text transformer."""
        self.platform = platform.system().lower()
        logger.info(f"Initialized TextTransformer on {self.platform}")
    
    def get_selected_text(self) -> str:
        """
        Get the currently selected text by simulating Ctrl+C/Cmd+C.
        
        Returns:
            str: The selected text, or empty string if none
        """
        try:
            print("Getting selected text...")
            
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            logger.info(f"Original clipboard content length: {len(original_clipboard)}")
            
            # Clear clipboard
            pyperclip.copy('')
            time.sleep(1)
            
            # Simulate copy shortcut (Ctrl+C on Windows/Linux, Cmd+C on macOS)
            if self.platform == 'darwin':  # macOS
                print("Simulating Cmd+C...")
                # Use keyDown/keyUp approach which works better on macOS
                pyautogui.keyDown('command')
                time.sleep(0.2)
                pyautogui.press('c')
                time.sleep(0.2)
                pyautogui.keyUp('command')
            else:  # Windows/Linux
                print("Simulating Ctrl+C...")
                pyautogui.hotkey('ctrl', 'c')
            
            # Wait for clipboard to update (longer wait time)
            print("Waiting for clipboard to update...")
            time.sleep(3)
            
            # Get the selected text
            selected_text = pyperclip.paste()
            logger.info(f"Selected text length: {len(selected_text)}")
            
            # Restore original clipboard content
            pyperclip.copy(original_clipboard)
            print("Clipboard restored.")
            
            # Print the selected text
            if selected_text:
                print(f"\n--- Selected Text ---\n{selected_text}\n--- End of Selected Text ---\n")
            
            return selected_text
            
        except Exception as e:
            logger.error(f"Error getting selected text: {e}")
            return ""

    def send_to_ai_model(self, text: str) -> str:
        """
        Send text to AI model for processing.
        
        Args:
            text (str): Input text to transform
            
        Returns:
            str: Transformed text from AI model
        """
        try:
            print("Sending text to AI model...")
            
            # Import langchain components only when needed
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage
            
            # Determine which provider to use based on available API keys
            if Config.OPENAI_API_KEY:
                logger.info("Using OpenAI model for text transformation")
                model = ChatOpenAI(
                    temperature=Config.TEMPERATURE,
                    model=Config.OPENAI_MODEL,
                    openai_api_key=Config.OPENAI_API_KEY,
                    base_url=Config.OPENAI_BASE_URL
                )
                prompt = f"Please improve the following text while maintaining its meaning:\n\n{text}"
                
                
            else:
                logger.warning("No API key configured. Returning original text.")
                return text
            
            # Send request to AI model
            response = model.invoke([HumanMessage(content=prompt)])
            transformed_text = response.content.strip()
            
            logger.info("Successfully received response from AI model")
            print("Received response from AI model.")
            
            # Print the transformed text
            if transformed_text:
                print(f"\n--- AI Response ---\n{transformed_text}\n--- End of AI Response ---\n")
            
            return transformed_text
            
        except Exception as e:
            logger.error(f"Error sending text to AI model: {e}")
            return text  # Return original text if AI processing fails

    def replace_selected_text(self, new_text: str) -> bool:
        """
        Replace selected text with new text.
        
        Args:
            new_text (str): Text to replace the selection with
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("Replacing selected text...")
            
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            logger.info(f"Original clipboard content length: {len(original_clipboard)}")
            
            # Copy new text to clipboard
            pyperclip.copy(new_text)
            logger.info(f"New text copied to clipboard (length: {len(new_text)})")
            time.sleep(1)
            
            # Simulate paste shortcut (Ctrl+V on Windows/Linux, Cmd+V on macOS)
            if self.platform == 'darwin':  # macOS
                print("Simulating Cmd+V...")
                # Use keyDown/keyUp approach which works better on macOS
                pyautogui.keyDown('command')
                time.sleep(0.2)
                pyautogui.press('v')
                time.sleep(0.2)
                pyautogui.keyUp('command')
            else:  # Windows/Linux
                print("Simulating Ctrl+V...")
                pyautogui.hotkey('ctrl', 'v')
            
            # Wait for paste to complete
            print("Waiting for paste to complete...")
            time.sleep(3)
            
            # Restore original clipboard content
            pyperclip.copy(original_clipboard)
            print("Clipboard restored.")
            
            logger.info("Successfully replaced selected text")
            return True
            
        except Exception as e:
            logger.error(f"Error replacing selected text: {e}")
            return False

    def transform_selected_text(self) -> bool:
        """
        Main workflow: get selected text, transform it with AI, replace original.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Starting text transformation process")
        print("\n--- Text Transformation Process ---")
        
        # Get selected text
        selected_text = self.get_selected_text()
        if not selected_text.strip():
            logger.warning("No text selected or failed to get selection")
            print("ERROR: No text selected or failed to get selection.")
            return False
        
        print(f"Selected text ({len(selected_text)} chars): '{selected_text[:100]}{'...' if len(selected_text) > 100 else ''}'")
        logger.info(f"Processing text of length: {len(selected_text)}")
        
        # Transform text with AI
        transformed_text = self.send_to_ai_model(selected_text)
        if not transformed_text:
            logger.error("Failed to get transformed text from AI model")
            print("ERROR: Failed to get transformed text from AI model.")
            return False
        
        print(f"Transformed text ({len(transformed_text)} chars): '{transformed_text[:100]}{'...' if len(transformed_text) > 100 else ''}'")
        logger.info(f"Transformed text length: {len(transformed_text)}")
        
        # Replace original text
        success = self.replace_selected_text(transformed_text)
        if success:
            logger.info("Text transformation completed successfully")
            print("SUCCESS: Text transformation completed!")
        else:
            logger.error("Failed to replace selected text")
            print("ERROR: Failed to replace selected text.")
            
        return success

    def run(self):
        """Run the text transformer application."""
        print("=" * 50)
        print("Text Transformer Application")
        print("=" * 50)
        print("INSTRUCTIONS:")
        print("1. Select some text in any application")
        print("2. Switch back to this terminal")
        print("3. Press Enter to start the transformation")
        print("4. QUICKLY switch back to your application (within 5 seconds)")
        print("5. The AI-improved text will automatically replace your selection")
        print()
        print("NOTE: This works best with short to medium-length text selections.")
        print()
        
        # Validate configuration
        try:
            Config.validate()
            logger.info("Configuration validated successfully")
            print("✓ Configuration validated")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            print(f"✗ Configuration error: {e}")
            sys.exit(1)
        
        try:
            input("Press Enter to begin text transformation: ")
        except EOFError:
            print("Beginning text transformation...")
        
        print("\nSwitching to text selection mode in 5 seconds...")
        print("Please select your text NOW in another application!")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\nStarting transformation NOW!")
        
        # Run the transformation
        success = self.transform_selected_text()
        
        print("\n" + "=" * 50)
        if success:
            print("✓ SUCCESS: Text transformation completed!")
            print("Your selected text has been replaced with an AI-improved version.")
        else:
            print("✗ FAILED: Text transformation encountered an error.")
            print("Please check the log file 'text_transformer.log' for details.")
        print("=" * 50)

def main():
    """Main entry point for the application."""
    # Create and run transformer
    transformer = TextTransformer()
    transformer.run()

if __name__ == "__main__":
    main()