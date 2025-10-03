"""
AI讨论引擎模块
实现双AI对话的核心逻辑和流程控制
"""

import time
import re
from typing import List, Dict, Tuple, Optional
from config import DiscussionConfig
from api_client import APIClient
import logging

logger = logging.getLogger(__name__)

class DiscussionEngine:
    """AI讨论引擎类"""
    
    def __init__(self, config: DiscussionConfig):
        self.config = config
        self.api_client = APIClient(config)
        self.discussion_history: List[Dict] = []
        self.current_round = 0
        self.is_ended = False
        self.winner = None
        self.end_reason = None
        
    def start_discussion(self) -> bool:
        """开始讨论"""
        try:
            logger.info("开始AI讨论")
            logger.info(f"话题: {self.config.topic}")
            logger.info(f"理性程度: {self.config.rationality_level}")
            logger.info(f"最大轮数: {self.config.max_rounds}")
            
            # 验证配置
            self.config.validate_config()
            
            # 测试API连接
            if not self.api_client.test_connection():
                logger.error("API连接测试失败")
                return False
            
            # 初始化第一轮讨论
            self._initialize_first_round()
            
            return True
            
        except Exception as e:
            logger.error(f"讨论初始化失败: {str(e)}")
            return False
    
    def _initialize_first_round(self):
        """初始化第一轮讨论"""
        self.current_round = 1
        logger.info(f"开始第 {self.current_round} 轮讨论")
        
        # AI-A 首先发言
        system_prompt = self.config.get_system_prompt("AI-A", self.current_round, discussion_history=[], is_first_round=True)
        ai_a_response = self.api_client.generate_response(system_prompt)
        
        # 记录AI-A的发言
        self.discussion_history.append({
            "round": self.current_round,
            "speaker": "AI-A",
            "response": ai_a_response,
            "timestamp": time.time()
        })
        
        logger.info(f"AI-A 第{self.current_round}轮发言: {ai_a_response}")
        
        # 检查是否已经结束
        if self._check_end_condition(ai_a_response, "AI-A"):
            return
    
    def continue_discussion(self) -> bool:
        """继续讨论的下一轮"""
        if self.is_ended:
            return False
        
        if self.current_round >= self.config.max_rounds:
            self._end_discussion("达到最大轮数限制")
            return False
        
        try:
            self.current_round += 1
            logger.info(f"开始第 {self.current_round} 轮讨论")
            
            # 确定当前发言者
            current_speaker = "AI-B" if self.current_round % 2 == 0 else "AI-A"
            
            # 生成系统提示词（传递完整的讨论历史）
            system_prompt = self.config.get_system_prompt(
                current_speaker, 
                self.current_round, 
                discussion_history=self.discussion_history,
                is_first_round=False
            )
            
            # 生成当前AI的回复
            current_response = self.api_client.generate_response(system_prompt)
            
            # 记录当前发言
            self.discussion_history.append({
                "round": self.current_round,
                "speaker": current_speaker,
                "response": current_response,
                "timestamp": time.time()
            })
            
            logger.info(f"{current_speaker} 第{self.current_round}轮发言: {current_response}")
            
            # 检查结束条件
            if self._check_end_condition(current_response, current_speaker):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"第{self.current_round}轮讨论失败: {str(e)}")
            self._end_discussion(f"讨论过程中出现错误: {str(e)}")
            return False
    
    def _check_end_condition(self, response: str, speaker: str) -> bool:
        """检查讨论是否应该结束"""
        response_lower = response.lower()
        
        # 检查是否认输
        surrender_keywords = ["我输了", "我认输", "我承认", "你说得对", "我无法反驳"]
        for keyword in surrender_keywords:
            if keyword in response_lower:
                self._end_discussion(f"{speaker}认输")
                self.winner = "AI-B" if speaker == "AI-A" else "AI-A"
                return True
        
        # 检查是否达到最大轮数
        if self.current_round >= self.config.max_rounds:
            self._end_discussion("达到最大轮数限制")
            return True
        
        # 检查是否陷入僵局（简单检查：最近3轮是否有重复内容）
        if len(self.discussion_history) >= 6:
            recent_responses = [item["response"] for item in self.discussion_history[-6:]]
            if self._check_repetition(recent_responses):
                self._end_discussion("讨论陷入僵局，观点重复")
                return True
        
        return False
    
    def _check_repetition(self, responses: List[str]) -> bool:
        """检查回复是否重复"""
        if len(responses) < 4:
            return False
        
        # 简单的重复检测：检查是否有相同的句子
        sentences = []
        for response in responses:
            # 简单的句子分割
            response_sentences = re.split(r'[。！？]', response)
            sentences.extend([s.strip() for s in response_sentences if s.strip()])
        
        # 检查是否有重复的句子
        unique_sentences = set(sentences)
        repetition_ratio = 1 - (len(unique_sentences) / len(sentences)) if sentences else 0
        
        return repetition_ratio > 0.5  # 如果重复率超过50%，认为陷入僵局
    
    def _end_discussion(self, reason: str):
        """结束讨论"""
        self.is_ended = True
        self.end_reason = reason
        logger.info(f"讨论结束: {reason}")
        
        if self.winner:
            logger.info(f"获胜者: {self.winner}")
    
    def get_discussion_summary(self) -> Dict:
        """获取讨论总结"""
        if not self.is_ended:
            return {"status": "进行中", "current_round": self.current_round}
        
        total_rounds = len(self.discussion_history)
        duration = 0
        if self.discussion_history:
            duration = self.discussion_history[-1]["timestamp"] - self.discussion_history[0]["timestamp"]
        
        return {
            "status": "已结束",
            "total_rounds": total_rounds,
            "winner": self.winner,
            "end_reason": self.end_reason,
            "duration_seconds": round(duration, 2),
            "api_requests": self.api_client.get_stats()["request_count"]
        }
    
    def get_discussion_history(self) -> List[Dict]:
        """获取完整的讨论历史"""
        return self.discussion_history.copy()
    
    def save_discussion(self, filename: str = None) -> str:
        """保存讨论记录到文件"""
        if not filename:
            timestamp = int(time.time())
            filename = f"discussion_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"AI讨论记录\n")
                f.write(f"=" * 50 + "\n")
                f.write(f"话题: {self.config.topic}\n")
                f.write(f"理性程度: {self.config.rationality_level}\n")
                f.write(f"AI-A风格: {self.config.speaking_style_A}\n")
                f.write(f"AI-B风格: {self.config.speaking_style_B}\n")
                f.write(f"=" * 50 + "\n\n")
                
                for item in self.discussion_history:
                    f.write(f"第{item['round']}轮 - {item['speaker']}:\n")
                    f.write(f"{item['response']}\n\n")
                
                # 添加总结
                summary = self.get_discussion_summary()
                f.write(f"=" * 50 + "\n")
                f.write(f"讨论总结:\n")
                f.write(f"总轮数: {summary['total_rounds']}\n")
                f.write(f"结束原因: {summary['end_reason']}\n")
                if summary['winner']:
                    f.write(f"获胜者: {summary['winner']}\n")
                f.write(f"API请求次数: {summary['api_requests']}\n")
            
            logger.info(f"讨论记录已保存到: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"保存讨论记录失败: {str(e)}")
            return ""
