# Angelic Design

An AI-powered design assistant project.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your API keys in the `.env` file

## Configuration

- `.env`: Contains sensitive information like API keys
- `config.py`: Configuration manager that loads settings from `.env`

## Usage

### Main Application
Run the main script:
```bash
python PromptChain.py
```

### Text Transformer Tool
A utility to enhance selected text using AI:

1. Run the text transformer:
   ```bash
   # On Unix-like systems (macOS, Linux)
   ./run_text_transformer.sh
   
   # On Windows
   run_text_transformer.bat
   ```

2. Select any text in any application and press:
   - Windows/Linux: `Ctrl + Shift + Space`
   - macOS: `Cmd + Shift + Space`

3. The selected text will be automatically enhanced by AI and replace the original.

See `README-text-transformer.md` for detailed documentation.