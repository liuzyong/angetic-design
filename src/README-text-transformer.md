# Text Transformer Application

This application automatically captures selected text, sends it to an AI model for processing, and replaces the original text with the AI-enhanced version using a simple hotkey.

## Features

- Cross-platform support (Windows, macOS, Linux)
- Hotkey activation (Ctrl+Shift+Space by default, Cmd+Shift+Space on macOS)
- Support for multiple AI providers:
  - OpenAI (GPT models)
  - Anthropic (Claude models)
  - Google (Gemini models)
- Secure clipboard handling
- Detailed logging for troubleshooting

## Prerequisites

1. Python 3.7 or higher
2. Required Python packages (automatically installed):
   - pyautogui
   - pyperclip
   - keyboard
   - langchain and provider-specific packages

## Installation

1. Navigate to the project directory:
   ```bash
   cd src
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses the existing configuration system in `config.py`. Make sure to set your API keys in the `.env` file:

```env
# Choose one or more of the following API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional model settings
OPENAI_MODEL=gpt-4
ANTHROPIC_MODEL=claude-3-opus-20240229
GOOGLE_MODEL=gemini-pro

# Optional generation settings
TEMPERATURE=0.7
MAX_TOKENS=2048
```

The application will automatically use the first available API key in the order: OpenAI → Anthropic → Google.

## Usage

1. Run the application:
   ```bash
   python text_transformer.py
   ```

2. Select any text in any application (browser, text editor, etc.)

3. Press the hotkey:
   - Windows/Linux: `Ctrl + Shift + Space`
   - macOS: `Cmd + Shift + Space`

4. The selected text will be automatically:
   - Captured
   - Sent to your configured AI model
   - Replaced with the AI-enhanced version

5. To stop the application, press `Ctrl + C` in the terminal

## How It Works

1. **Text Selection**: The application monitors for the hotkey combination
2. **Capture**: When activated, it simulates a copy command (Ctrl+C/Cmd+C) to capture selected text
3. **Processing**: Sends the text to your configured AI model with a prompt to improve the text
4. **Replacement**: Automatically pastes the AI response, replacing the original text
5. **Clipboard Management**: Preserves your original clipboard content throughout the process

## Customization

### Changing the Hotkey

To modify the hotkey, edit the `hotkey` attribute in the `TextTransformer` class constructor in `text_transformer.py`:

```python
# In the __init__ method of TextTransformer class
self.hotkey = 'ctrl+shift+space'  # Change this to your preferred hotkey
```

Refer to the [keyboard library documentation](https://github.com/boppreh/keyboard) for hotkey syntax.

### Modifying the AI Prompt

To change how the AI processes your text, modify the prompt in the `send_to_ai_model` method:

```python
prompt = f"Please improve the following text while maintaining its meaning:\n\n{text}"
```

## Troubleshooting

### Common Issues

1. **Hotkey not working**:
   - Ensure the application is running
   - Check if another application is using the same hotkey
   - On some Linux systems, you may need to run with sudo for global hotkey detection

2. **Text not being captured**:
   - Make sure text is actually selected before pressing the hotkey
   - Some applications may restrict programmatic clipboard access

3. **AI response not pasting**:
   - The target application may have restrictions on programmatic pasting
   - Try manually pasting (Ctrl+V/Cmd+V) to verify clipboard content

### Logs

The application creates a log file `text_transformer.log` in the same directory with detailed information about each operation. Check this file for debugging information.

## Supported Platforms

- Windows 7 and above
- macOS 10.12 and above
- Linux distributions with X11/Wayland

Note: On Linux, some features may require additional setup depending on your window manager.

## Security

- API keys are loaded from environment variables and never hardcoded
- The application only accesses clipboard content when explicitly triggered
- Original clipboard content is preserved after each operation