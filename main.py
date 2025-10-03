"""
双AI讨论系统主程序
这是程序的入口点，启动CLI界面
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_interface import main

if __name__ == "__main__":
    main()
