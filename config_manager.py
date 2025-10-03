"""
配置管理器
处理config.ini文件的读取和解析
"""

import configparser
import os
from typing import Dict, Any

class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            # 如果配置文件不存在，创建默认配置
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        self.config['API'] = {
            'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
            'api_key': '5ba3ef10-df27-4ac2-bc8e-07f3ab86de79',
            'model': 'doubao-seed-1-6-250615',
            'timeout_seconds': '30'
        }
        
        self.config['PROMPTS'] = {
            'prompt_template_A': '''你是一个参与讨论的AI助手，名字是AI-A。

讨论话题：{topic}
你的说话风格：{speaking_style_A}
理性程度：{rationality_level}/10
当前轮次：{current_round}/{max_rounds}

讨论规则：
1. 每轮发言限制在2-3句话内（约50-80字）
2. 保持简洁明了，避免冗长表达
3. 基于理性程度进行辩论，理性程度越高越客观
4. 当无法在指定理性程度下继续有效辩论时，可以说"我输了"来结束讨论
5. 避免重复之前的观点
6. 保持讨论的连贯性和逻辑性

{context_info}

请开始你的发言：''',
            
            'prompt_template_B': '''你是一个参与讨论的AI助手，名字是AI-B。

讨论话题：{topic}
你的说话风格：{speaking_style_B}
理性程度：{rationality_level}/10
当前轮次：{current_round}/{max_rounds}

讨论规则：
1. 每轮发言限制在2-3句话内（约50-80字）
2. 保持简洁明了，避免冗长表达
3. 基于理性程度进行辩论，理性程度越高越客观
4. 当无法在指定理性程度下继续有效辩论时，可以说"我输了"来结束讨论
5. 避免重复之前的观点
6. 保持讨论的连贯性和逻辑性

{context_info}

请开始你的发言：'''
        }
        
        self.config['SYSTEM'] = {
            'max_response_length': '80',
            'min_response_length': '20',
            'log_level': 'INFO',
            'log_file': 'discussion.log',
            'save_discussion': 'true'
        }
        
        self.config['UI'] = {
            'enable_colors': 'true',
            'show_timestamps': 'true',
            'display_delay': '1.0'
        }
        
        self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取API配置"""
        return {
            'base_url': self.config.get('API', 'base_url'),
            'api_key': self.config.get('API', 'api_key'),
            'model': self.config.get('API', 'model'),
            'timeout_seconds': self.config.getint('API', 'timeout_seconds')
        }
    
    def get_prompt_templates(self) -> Dict[str, str]:
        """获取提示词模板"""
        return {
            'template_A': self.config.get('PROMPTS', 'prompt_template_A'),
            'template_B': self.config.get('PROMPTS', 'prompt_template_B')
        }
    
    def get_system_config(self) -> Dict[str, Any]:
        """获取系统配置"""
        return {
            'max_response_length': self.config.getint('SYSTEM', 'max_response_length'),
            'min_response_length': self.config.getint('SYSTEM', 'min_response_length'),
            'log_level': self.config.get('SYSTEM', 'log_level'),
            'log_file': self.config.get('SYSTEM', 'log_file'),
            'save_discussion': self.config.getboolean('SYSTEM', 'save_discussion')
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """获取界面配置"""
        return {
            'enable_colors': self.config.getboolean('UI', 'enable_colors'),
            'show_timestamps': self.config.getboolean('UI', 'show_timestamps'),
            'display_delay': self.config.getfloat('UI', 'display_delay')
        }
    
    def update_config(self, section: str, key: str, value: str):
        """更新配置项"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save_config()
    
    def get_all_config(self) -> Dict[str, Dict[str, Any]]:
        """获取所有配置"""
        return {
            'API': self.get_api_config(),
            'PROMPTS': self.get_prompt_templates(),
            'SYSTEM': self.get_system_config(),
            'UI': self.get_ui_config()
        }
