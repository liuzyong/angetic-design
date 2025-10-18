import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

class Config:
    """配置类，用于管理应用程序的各种设置"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    # API Endpoints
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
    
    # General Settings
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
    
    @classmethod
    def validate(cls):
        """验证必要的配置是否存在"""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            raise ValueError("至少需要配置一个API密钥")
        
        return True

# 验证配置
try:
    Config.validate()
    config_valid = True
except ValueError as e:
    print(f"配置验证失败: {e}")
    config_valid = False

if __name__ == "__main__":
    print("配置信息:")
    print(f"OpenAI Model: {Config.OPENAI_MODEL}")
    print(f"Anthropic Model: {Config.ANTHROPIC_MODEL}")
    print(f"Temperature: {Config.TEMPERATURE}")
    print(f"Max Tokens: {Config.MAX_TOKENS}")