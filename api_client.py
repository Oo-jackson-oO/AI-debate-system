"""
API客户端模块
处理与OpenAI API的交互
"""

import os
import time
from openai import OpenAI
from config import DiscussionConfig
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """API客户端类，负责与AI模型的交互"""
    
    def __init__(self, config: DiscussionConfig):
        self.config = config
        self.client = OpenAI(
            base_url=config.api_base_url,
            api_key=config.api_key
        )
        self.request_count = 0
        
    def generate_response(self, system_prompt: str, user_message: str = "") -> str:
        """
        生成AI回复
        
        Args:
            system_prompt: 系统提示词
            user_message: 用户消息（可选）
            
        Returns:
            str: AI生成的回复
        """
        try:
            self.request_count += 1
            logger.info(f"发送第 {self.request_count} 次API请求")
            
            # 构建消息列表
            messages = [{"role": "system", "content": system_prompt}]
            
            if user_message:
                messages.append({"role": "user", "content": user_message})
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=150,  # 限制回复长度
                temperature=0.7,  # 控制回复的随机性
                timeout=self.config.timeout_seconds
            )
            
            # 提取回复内容
            ai_response = response.choices[0].message.content.strip()
            
            # 验证回复长度
            if len(ai_response) > self.config.max_response_length:
                ai_response = ai_response[:self.config.max_response_length] + "..."
            elif len(ai_response) < self.config.min_response_length:
                logger.warning(f"回复过短: {ai_response}")
            
            logger.info(f"收到回复: {ai_response[:50]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            return f"抱歉，我遇到了一些技术问题，无法继续讨论。"
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            test_response = self.generate_response(
                "你是一个测试助手，请简单回复'连接成功'。",
                "测试连接"
            )
            return "连接成功" in test_response or len(test_response) > 0
        except Exception as e:
            logger.error(f"连接测试失败: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """获取API使用统计"""
        return {
            "request_count": self.request_count,
            "api_key": self.config.api_key[:10] + "..." if self.config.api_key else "未设置"
        }
