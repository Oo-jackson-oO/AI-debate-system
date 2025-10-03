"""
命令行界面模块
提供用户友好的CLI交互界面
"""

import os
import sys
import time
from colorama import init, Fore, Back, Style
from config import DiscussionConfig
from discussion_engine import DiscussionEngine
import logging

# 初始化colorama（Windows兼容）
init(autoreset=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discussion.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CLIInterface:
    """命令行界面类"""
    
    def __init__(self):
        self.config = DiscussionConfig()
        self.engine = None
        
    def print_banner(self):
        """打印欢迎横幅"""
        banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}🤖 双AI讨论系统 v1.0
{Fore.CYAN}{'='*60}
{Fore.WHITE}欢迎使用AI讨论系统！两个AI将就指定话题进行理性辩论。
{Fore.CYAN}{'='*60}{Style.RESET_ALL}
"""
        print(banner)
    
    def print_config_menu(self):
        """显示配置菜单"""
        print(f"\n{Fore.GREEN}📋 当前配置:{Style.RESET_ALL}")
        print(f"  话题: {Fore.YELLOW}{self.config.topic}{Style.RESET_ALL}")
        print(f"  AI-A风格: {Fore.BLUE}{self.config.speaking_style_A}{Style.RESET_ALL}")
        print(f"  AI-B风格: {Fore.MAGENTA}{self.config.speaking_style_B}{Style.RESET_ALL}")
        print(f"  理性程度: {Fore.CYAN}{self.config.rationality_level}/10{Style.RESET_ALL}")
        print(f"  最大轮数: {Fore.WHITE}{self.config.max_rounds}{Style.RESET_ALL}")
    
    def get_user_input(self, prompt: str, default: str = None) -> str:
        """获取用户输入"""
        if default:
            user_input = input(f"{Fore.GREEN}{prompt} (默认: {default}): {Style.RESET_ALL}").strip()
            return user_input if user_input else default
        else:
            return input(f"{Fore.GREEN}{prompt}: {Style.RESET_ALL}").strip()
    
    def configure_discussion(self):
        """配置讨论参数"""
        print(f"\n{Fore.YELLOW}⚙️  配置讨论参数{Style.RESET_ALL}")
        print("按回车键使用默认值，或输入新值进行修改")
        
        # 话题配置
        new_topic = self.get_user_input("讨论话题", self.config.topic)
        if new_topic != self.config.topic:
            self.config.topic = new_topic
        
        # AI-A风格配置
        new_style_a = self.get_user_input("AI-A说话风格", self.config.speaking_style_A)
        if new_style_a != self.config.speaking_style_A:
            self.config.speaking_style_A = new_style_a
        
        # AI-B风格配置
        new_style_b = self.get_user_input("AI-B说话风格", self.config.speaking_style_B)
        if new_style_b != self.config.speaking_style_B:
            self.config.speaking_style_B = new_style_b
        
        # 理性程度配置
        try:
            new_rationality = self.get_user_input("理性程度 (1-10)", str(self.config.rationality_level))
            new_rationality = int(new_rationality)
            if 1 <= new_rationality <= 10:
                self.config.rationality_level = new_rationality
            else:
                print(f"{Fore.RED}理性程度必须在1-10之间，使用默认值{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}输入无效，使用默认值{Style.RESET_ALL}")
        
        # 最大轮数配置
        try:
            new_max_rounds = self.get_user_input("最大讨论轮数", str(self.config.max_rounds))
            new_max_rounds = int(new_max_rounds)
            if new_max_rounds > 0:
                self.config.max_rounds = new_max_rounds
            else:
                print(f"{Fore.RED}最大轮数必须大于0，使用默认值{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}输入无效，使用默认值{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✅ 配置完成！{Style.RESET_ALL}")
        self.print_config_menu()
    
    def display_discussion_round(self, round_data: dict):
        """显示单轮讨论"""
        speaker = round_data["speaker"]
        response = round_data["response"]
        round_num = round_data["round"]
        
        # 根据发言者选择颜色
        if speaker == "AI-A":
            color = Fore.BLUE
            icon = "🤖"
        else:
            color = Fore.MAGENTA
            icon = "🤖"
        
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{color}{icon} {speaker} - 第{round_num}轮{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{color}{response}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}")
        
        # 添加延迟以增强用户体验
        time.sleep(1)
    
    def run_discussion(self):
        """运行讨论"""
        print(f"\n{Fore.YELLOW}🚀 开始AI讨论...{Style.RESET_ALL}")
        
        # 初始化讨论引擎
        self.engine = DiscussionEngine(self.config)
        
        # 开始讨论
        if not self.engine.start_discussion():
            print(f"{Fore.RED}❌ 讨论初始化失败！{Style.RESET_ALL}")
            return
        
        # 显示第一轮
        if self.engine.discussion_history:
            self.display_discussion_round(self.engine.discussion_history[-1])
        
        # 继续讨论直到结束
        while not self.engine.is_ended:
            print(f"\n{Fore.YELLOW}⏳ 正在生成下一轮回复...{Style.RESET_ALL}")
            
            if not self.engine.continue_discussion():
                break
            
            # 显示最新一轮
            if self.engine.discussion_history:
                self.display_discussion_round(self.engine.discussion_history[-1])
        
        # 显示讨论结果
        self.display_discussion_result()
    
    def display_discussion_result(self):
        """显示讨论结果"""
        if not self.engine:
            return
        
        summary = self.engine.get_discussion_summary()
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.YELLOW}🏁 讨论结束！{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}")
        
        print(f"{Fore.WHITE}📊 讨论统计:{Style.RESET_ALL}")
        print(f"  总轮数: {Fore.CYAN}{summary['total_rounds']}{Style.RESET_ALL}")
        print(f"  结束原因: {Fore.YELLOW}{summary['end_reason']}{Style.RESET_ALL}")
        
        if summary['winner']:
            winner_color = Fore.GREEN if summary['winner'] == 'AI-A' else Fore.MAGENTA
            print(f"  获胜者: {winner_color}{summary['winner']}{Style.RESET_ALL}")
        else:
            print(f"  获胜者: {Fore.WHITE}平局{Style.RESET_ALL}")
        
        print(f"  讨论时长: {Fore.CYAN}{summary['duration_seconds']}秒{Style.RESET_ALL}")
        print(f"  API请求次数: {Fore.CYAN}{summary['api_requests']}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}{'='*60}")
        
        # 询问是否保存讨论记录
        save_choice = self.get_user_input("\n是否保存讨论记录？(y/n)", "y").lower()
        if save_choice in ['y', 'yes', '是']:
            filename = self.engine.save_discussion()
            if filename:
                print(f"{Fore.GREEN}✅ 讨论记录已保存到: {filename}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ 保存失败{Style.RESET_ALL}")
    
    def show_main_menu(self):
        """显示主菜单"""
        while True:
            print(f"\n{Fore.CYAN}{'='*40}")
            print(f"{Fore.YELLOW}📋 主菜单{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*40}")
            print(f"{Fore.WHITE}1. 开始讨论{Style.RESET_ALL}")
            print(f"{Fore.WHITE}2. 配置参数{Style.RESET_ALL}")
            print(f"{Fore.WHITE}3. 查看当前配置{Style.RESET_ALL}")
            print(f"{Fore.WHITE}4. 退出程序{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*40}")
            
            choice = self.get_user_input("请选择操作 (1-4)", "1")
            
            if choice == "1":
                self.run_discussion()
            elif choice == "2":
                self.configure_discussion()
            elif choice == "3":
                self.print_config_menu()
            elif choice == "4":
                print(f"\n{Fore.YELLOW}👋 感谢使用AI讨论系统！{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}❌ 无效选择，请重新输入{Style.RESET_ALL}")
    
    def run(self):
        """运行CLI界面"""
        try:
            self.print_banner()
            self.print_config_menu()
            
            # 询问是否要修改配置
            modify_config = self.get_user_input("\n是否要修改配置？(y/n)", "n").lower()
            if modify_config in ['y', 'yes', '是']:
                self.configure_discussion()
            
            # 显示主菜单
            self.show_main_menu()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 程序被用户中断，再见！{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"程序运行出错: {str(e)}")
            print(f"\n{Fore.RED}❌ 程序运行出错: {str(e)}{Style.RESET_ALL}")

def main():
    """主函数"""
    cli = CLIInterface()
    cli.run()

if __name__ == "__main__":
    main()
