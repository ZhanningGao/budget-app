"""
配置文件 - 用于管理API Key等配置
"""
import os
import json

CONFIG_FILE = '.config.json'

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_api_key():
    """获取API Key，优先级：环境变量 > 配置文件"""
    # 优先使用环境变量
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GROQ_API_KEY')
    if api_key:
        return api_key
    
    # 从配置文件读取
    config = load_config()
    return config.get('api_key', '')

def set_api_key(api_key):
    """设置API Key到配置文件"""
    config = load_config()
    config['api_key'] = api_key
    save_config(config)

def get_api_provider():
    """获取API Provider，优先级：环境变量 > 配置文件"""
    provider = os.getenv('API_PROVIDER')
    if provider:
        return provider
    
    config = load_config()
    return config.get('provider', 'openai')

def set_api_provider(provider):
    """设置API Provider到配置文件"""
    config = load_config()
    config['provider'] = provider
    save_config(config)

