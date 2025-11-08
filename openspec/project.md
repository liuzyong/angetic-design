# Project Context

## Purpose
Angelic Design is an AI-powered design assistant project that provides tools to enhance productivity through AI integration. The project focuses on creating utilities that can automatically process and improve text content using various AI models.

## Tech Stack
- Python 3.x
- Langchain for AI model integration
- OpenAI, Anthropic, and Google AI models
- PyAutoGUI for GUI automation
- Pyperclip for clipboard operations
- dotenv for configuration management

## Project Conventions

### Code Style
- Follow PEP 8 Python style guide
- Use descriptive variable and function names in English
- Include docstrings for all functions and classes
- Use type hints where appropriate
- Keep functions focused and single-purpose

### Architecture Patterns
- Modular design with separate modules for different functionalities
- Configuration management through environment variables
- Class-based architecture for complex components
- Separation of concerns between AI processing, GUI interaction, and business logic

### Testing Strategy
- Manual testing for GUI automation features
- Unit tests for core logic functions
- Integration testing for AI model interactions

### Git Workflow
- Feature branches for new developments
- Pull requests for code review
- Semantic commit messages
- Main branch for stable releases

## Domain Context
The project provides AI-powered text transformation capabilities that can:
1. Capture selected text from any application
2. Process the text through AI models
3. Replace the original text with AI-enhanced content

## Important Constraints
- Cross-platform compatibility (Windows, macOS, Linux)
- Minimal dependencies to reduce installation complexity
- Security considerations for API key management
- Performance optimization for responsive user experience

## External Dependencies
- OpenAI API
- Anthropic API
- Google AI API
- Various Langchain components for AI integration
