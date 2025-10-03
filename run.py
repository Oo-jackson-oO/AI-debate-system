#!/usr/bin/env python3
"""
快速启动脚本
提供多种启动选项
"""

import sys
import os

def show_menu():
    """显示启动菜单"""
    print("""
🤖 双AI讨论系统 - 启动菜单
================================
1. 启动完整系统 (推荐)
2. 运行系统测试
3. 查看配置示例
4. 退出
================================
""")

def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("请选择操作 (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 启动AI讨论系统...")
                from cli_interface import main as cli_main
                cli_main()
                break
                
            elif choice == "2":
                print("\n🧪 运行系统测试...")
                from test_system import run_all_tests
                run_all_tests()
                input("\n按回车键继续...")
                
            elif choice == "3":
                print("\n📋 配置示例:")
                from example_config import print_config_examples
                print_config_examples()
                input("\n按回车键继续...")
                
            elif choice == "4":
                print("\n👋 再见！")
                break
                
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 程序出错: {e}")
            break

if __name__ == "__main__":
    main()
