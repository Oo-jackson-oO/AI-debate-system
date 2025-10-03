"""
系统配置模块
定义讨论系统的各种配置参数和常量
"""

from config_manager import ConfigManager
from prompt_generator import PromptGenerator

class DiscussionConfig:
    """讨论系统配置类"""
    
    def __init__(self, config_file: str = "config.ini"):
        # 初始化配置管理器
        self.config_manager = ConfigManager(config_file)
        
        # 基础配置（用户使用时配置）
        self.topic = "人工智能是否会取代人类工作"
        self.speaking_style_A = "理性客观，善于分析数据"
        self.speaking_style_B = "感性思考，关注人文关怀"
        self.rationality_level = 7  # 1-10，数值越高越理性
        self.max_rounds = 10
        
        # 从config.ini加载系统配置
        self._load_system_config()
        
        # 初始化提示词生成器
        self.prompt_generator = PromptGenerator(self.config_manager)
        
    def _load_system_config(self):
        """从config.ini加载系统配置"""
        api_config = self.config_manager.get_api_config()
        system_config = self.config_manager.get_system_config()
        
        # 加载API配置
        self.api_base_url = api_config['base_url']
        self.api_key = api_config['api_key']
        self.model = api_config['model']
        self.timeout_seconds = api_config['timeout_seconds']
        
        # 加载系统配置
        self.max_response_length = system_config['max_response_length']
        self.min_response_length = system_config['min_response_length']
        self.log_level = system_config['log_level']
        self.log_file = system_config['log_file']
        self.save_discussion = system_config['save_discussion']
    
    def update_config(self, **kwargs):
        """更新配置参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"警告: 未知配置项 '{key}'")
    
    def validate_config(self):
        """验证配置参数的有效性"""
        if not (1 <= self.rationality_level <= 10):
            raise ValueError("理性程度必须在1-10之间")
        
        if self.max_rounds <= 0:
            raise ValueError("最大轮数必须大于0")
        
        if not self.topic.strip():
            raise ValueError("话题不能为空")
        
        return True
    
    def get_constants(self) -> dict:
        """获取常量字典"""
        return {
            'speaking_style_A': self.speaking_style_A,
            'speaking_style_B': self.speaking_style_B,
            'rationality_level': self.rationality_level,
            'max_rounds': self.max_rounds
        }
    
    def get_variables(self, current_round: int, reply_A: str = "", reply_B: str = "", winner: str = None, discussion_history: list = None) -> dict:
        """获取变量字典"""
        # 如果没有提供reply_A和reply_B，从讨论历史中获取
        if discussion_history and (not reply_A or not reply_B):
            for item in discussion_history:
                if item["speaker"] == "AI-A":
                    reply_A = item["response"]
                elif item["speaker"] == "AI-B":
                    reply_B = item["response"]
        
        return {
            'topic': self.topic,
            'current_round': current_round,
            'reply_A': reply_A,
            'reply_B': reply_B,
            'winner': winner or "null"
        }
    
    def get_system_prompt(self, ai_name: str, current_round: int, discussion_history: list = None, is_first_round: bool = False):
        """生成系统提示词（使用新的提示词生成器）"""
        constants = self.get_constants()
        variables = self.get_variables(current_round, discussion_history=discussion_history)
        
        # 验证变量
        self.prompt_generator.validate_variables(constants, variables)
        
        # 使用新的提示词模板，直接生成提示词
        template_key = 'template_A' if ai_name == 'AI-A' else 'template_B'
        template = self.config_manager.get_prompt_templates()[template_key]
        
        # 合并常量和变量
        all_vars = {**constants, **variables}
        
        # 如果是第一轮，清空reply变量
        if is_first_round:
            all_vars['reply_A'] = ""
            all_vars['reply_B'] = ""
        
        # 执行变量替换
        try:
            prompt = template.format(**all_vars)
            return prompt
        except KeyError as e:
            raise ValueError(f"提示词模板中缺少变量: {e}")
    
    def get_available_variables(self) -> dict:
        """获取可用变量列表"""
        return self.prompt_generator.get_available_variables()
