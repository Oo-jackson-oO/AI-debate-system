"""
提示词生成器
处理动态变量替换和提示词生成
"""

from typing import Dict, Any, Optional
from config_manager import ConfigManager

class PromptGenerator:
    """提示词生成器类"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.prompt_templates = config_manager.get_prompt_templates()
    
    def generate_prompt(self, 
                       ai_name: str, 
                       constants: Dict[str, Any], 
                       variables: Dict[str, Any],
                       context_info: str = "") -> str:
        """
        生成AI提示词
        
        Args:
            ai_name: AI名称 ("AI-A" 或 "AI-B")
            constants: 常量字典 (speaking_style_A, speaking_style_B, rationality_level, max_rounds)
            variables: 变量字典 (topic, current_round, reply_A, reply_B, winner)
            context_info: 上下文信息
            
        Returns:
            str: 生成的提示词
        """
        # 选择对应的模板
        template_key = 'template_A' if ai_name == 'AI-A' else 'template_B'
        template = self.prompt_templates[template_key]
        
        # 合并常量和变量
        all_vars = {**constants, **variables}
        
        # 添加上下文信息
        all_vars['context_info'] = context_info
        
        # 执行变量替换
        try:
            prompt = template.format(**all_vars)
            return prompt
        except KeyError as e:
            raise ValueError(f"提示词模板中缺少变量: {e}")
    
    def generate_first_round_prompt(self, 
                                  ai_name: str, 
                                  constants: Dict[str, Any], 
                                  variables: Dict[str, Any]) -> str:
        """生成第一轮提示词"""
        context_info = "这是第一轮讨论，请基于话题开始你的观点阐述。"
        return self.generate_prompt(ai_name, constants, variables, context_info)
    
    def generate_subsequent_round_prompt(self, 
                                       ai_name: str, 
                                       constants: Dict[str, Any], 
                                       variables: Dict[str, Any],
                                       opponent_name: str,
                                       opponent_reply: str) -> str:
        """生成后续轮次提示词"""
        context_info = f"""
这是第{variables.get('current_round', 1)}轮讨论。

对方{opponent_name}的回复：{opponent_reply}

请基于对方的观点进行回应，可以：
1. 反驳对方的观点
2. 提出新的论据
3. 指出对方逻辑中的问题
4. 如果无法有效反驳，可以承认对方观点的合理性

记住要保持你的说话风格：{constants.get('speaking_style_A' if ai_name == 'AI-A' else 'speaking_style_B', '')}
"""
        return self.generate_prompt(ai_name, constants, variables, context_info)
    
    def generate_situation_aware_prompt(self,
                                      ai_name: str,
                                      constants: Dict[str, Any],
                                      variables: Dict[str, Any],
                                      discussion_history: list) -> str:
        """生成情境感知的提示词"""
        current_round = variables.get('current_round', 1)
        
        # 分析讨论历史
        if len(discussion_history) >= 1:
            # 获取最近的发言
            last_reply = discussion_history[-1]
            opponent_reply = last_reply['response']
            opponent_name = last_reply['speaker']
            
            # 分析讨论趋势
            trend_analysis = self._analyze_discussion_trend(discussion_history)
            
            context_info = f"""
这是第{current_round}轮讨论。

讨论趋势分析：{trend_analysis}

对方{opponent_name}的最新回复：{opponent_reply}

当前局势：
- 讨论已进行{current_round}轮
- 你的说话风格：{constants.get('speaking_style_A' if ai_name == 'AI-A' else 'speaking_style_B', '')}
- 理性程度要求：{constants.get('rationality_level', 7)}/10

请基于当前局势做出回应：
1. 如果对方观点有力，可以承认其合理性
2. 如果发现对方逻辑漏洞，可以指出
3. 如果讨论陷入重复，可以提出新角度
4. 如果无法有效回应，可以认输
"""
        else:
            context_info = "这是讨论的开始，请基于话题阐述你的观点。"
        
        return self.generate_prompt(ai_name, constants, variables, context_info)
    
    def _analyze_discussion_trend(self, discussion_history: list) -> str:
        """分析讨论趋势"""
        if len(discussion_history) < 2:
            return "讨论刚开始"
        
        # 简单的趋势分析
        recent_rounds = len(discussion_history)
        
        if recent_rounds <= 2:
            return "讨论初期，双方正在阐述基本观点"
        elif recent_rounds <= 4:
            return "讨论中期，双方开始深入辩论"
        else:
            return "讨论后期，需要避免重复观点"
    
    def validate_variables(self, constants: Dict[str, Any], variables: Dict[str, Any]) -> bool:
        """验证变量完整性"""
        required_constants = ['speaking_style_A', 'speaking_style_B', 'rationality_level', 'max_rounds']
        required_variables = ['topic', 'current_round']
        
        # 检查常量
        for const in required_constants:
            if const not in constants:
                raise ValueError(f"缺少必需常量: {const}")
        
        # 检查变量
        for var in required_variables:
            if var not in variables:
                raise ValueError(f"缺少必需变量: {var}")
        
        # 验证数值范围
        if not (1 <= constants['rationality_level'] <= 10):
            raise ValueError("理性程度必须在1-10之间")
        
        if constants['max_rounds'] <= 0:
            raise ValueError("最大轮数必须大于0")
        
        if variables['current_round'] <= 0:
            raise ValueError("当前轮次必须大于0")
        
        return True
    
    def get_available_variables(self) -> Dict[str, str]:
        """获取可用变量列表"""
        return {
            'constants': {
                'speaking_style_A': 'AI A的说话风格',
                'speaking_style_B': 'AI B的说话风格',
                'rationality_level': '理性程度 (1-10)',
                'max_rounds': '最大讨论轮数'
            },
            'variables': {
                'topic': '讨论话题',
                'current_round': '当前讨论轮次',
                'reply_A': 'AI A的最新发言',
                'reply_B': 'AI B的最新发言',
                'winner': '赢家标识 (null/AI_A/AI_B/tie)'
            }
        }
