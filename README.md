# 双AI讨论系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

*让两个AI进行自然、有趣的日常讨论*

[快速开始](#快速开始) • [功能特点](#功能特点) • [项目架构](#项目架构) • [使用指南](#使用指南)

</div>

## 📖 项目简介

双AI讨论系统是一个基于Python开发的智能对话平台，实现了两个AI之间的自然讨论功能。系统支持自定义话题、AI风格和讨论规则，能够模拟真实朋友间的轻松对话，并在适当时候智能结束讨论。

### 🎯 核心价值

- **自然对话**：模拟真实朋友间的日常讨论，避免生硬的学术辩论
- **智能交互**：AI能够看到对方的发言，做出有针对性的回应
- **灵活配置**：支持多种说话风格和理性程度设置
- **优雅结束**：AI会在无法继续有效讨论时主动认输

## ✨ 功能特点

| 功能模块 | 描述 | 特色 |
|---------|------|------|
| 🤖 **双AI对话** | 两个AI就指定话题进行深度讨论 | 支持reply_A/reply_B变量，AI能看到对方发言 |
| ⚙️ **灵活配置** | 可自定义话题、AI风格、理性程度等参数 | 实时配置，无需重启程序 |
| 🎯 **智能结束** | AI会在无法继续辩论时自动认输 | 多种结束条件：认输、轮数限制、陷入僵局 |
| 📊 **详细统计** | 提供讨论轮数、时长、API使用等统计信息 | 完整的讨论分析和性能监控 |
| 💾 **记录保存** | 支持将讨论记录保存为文本文件 | 包含完整讨论内容和元数据 |
| 🎨 **美观界面** | 彩色命令行界面，提升用户体验 | 跨平台兼容，支持Windows/Linux/macOS |
| 🔄 **动态变量** | 支持运行时变量替换和情境感知 | 智能提示词生成，适应不同讨论阶段 |

## 🚀 快速开始

### 环境要求

- **Python**: 3.7 或更高版本
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **网络**: 稳定的互联网连接（用于API调用）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd AI讨论赛
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动程序**
```bash
python run.py
```

### 依赖包说明

| 包名 | 版本 | 用途 |
|------|------|------|
| `openai` | ≥1.0.0 | OpenAI API客户端，支持多种AI模型 |
| `colorama` | ≥0.4.6 | 跨平台彩色终端输出 |
| `python-dotenv` | ≥1.0.0 | 环境变量管理 |

## 📁 项目架构

```
AI讨论赛/
├── 🚀 启动层
│   ├── main.py              # 主程序入口
│   └── run.py               # 快速启动脚本
├── 🎨 界面层
│   └── cli_interface.py     # 命令行用户界面
├── ⚙️ 业务层
│   ├── discussion_engine.py # 讨论引擎核心逻辑
│   └── api_client.py        # API客户端
├── 🔧 配置层
│   ├── config.py           # 配置管理主类
│   ├── config_manager.py   # 配置文件管理器
│   └── prompt_generator.py # 提示词生成器
├── 📋 数据层
│   ├── config.ini          # 系统配置文件
│   └── requirements.txt    # 依赖包列表
└── 📚 文档层
    ├── README.md           # 项目说明
    └── ARCHITECTURE.md     # 架构文档
```

### 核心模块说明

| 模块 | 职责 | 关键功能 |
|------|------|----------|
| **discussion_engine.py** | 讨论引擎 | 管理讨论流程、控制轮次、检测结束条件 |
| **api_client.py** | API客户端 | 处理AI模型交互、错误处理、连接测试 |
| **config.py** | 配置管理 | 参数验证、提示词生成、变量管理 |
| **cli_interface.py** | 用户界面 | 交互式配置、彩色输出、结果展示 |
| **prompt_generator.py** | 提示词生成 | 动态变量替换、情境感知、模板管理 |

## 📖 使用指南

### 基本使用流程

1. **启动系统**
   ```bash
   python run.py
   ```

2. **配置讨论参数**
   - 选择或自定义讨论话题
   - 设置AI-A和AI-B的说话风格
   - 调整理性程度（1-10分）
   - 设定最大讨论轮数

3. **开始讨论**
   - 系统自动进行AI对话
   - 实时观看讨论过程
   - 查看讨论统计结果

### 配置参数详解

#### 讨论参数

| 参数 | 说明 | 建议值 | 示例 |
|------|------|--------|------|
| **话题** | 讨论的主题内容 | 有争议性的话题 | "人工智能是否会取代人类工作" |
| **AI-A风格** | 第一个AI的说话风格 | 与AI-B形成对比 | "理性客观，善于分析数据" |
| **AI-B风格** | 第二个AI的说话风格 | 与AI-A形成对比 | "感性思考，关注人文关怀" |
| **理性程度** | 1-10分，数值越高越理性 | 7-8分 | 8 |
| **最大轮数** | 讨论的最大轮数限制 | 8-12轮 | 10 |

#### 系统配置 (config.ini)

```ini
[API]
base_url = https://ark.cn-beijing.volces.com/api/v3
api_key = your-api-key-here
model = doubao-seed-1-6-250615
timeout_seconds = 30

[PROMPTS]
prompt_template_A = 【角色】你是一位喜欢和朋友讨论话题的普通人...
prompt_template_B = 【角色】你是一位喜欢和朋友讨论话题的普通人...

[SYSTEM]
max_response_length = 80
min_response_length = 20
log_level = INFO
save_discussion = true
```

### 动态变量系统

系统支持以下动态变量，在讨论过程中自动更新：

#### 常量变量（初始设置）
- `{speaking_style_A}`: AI A的说话风格
- `{speaking_style_B}`: AI B的说话风格
- `{rationality_level}`: 理性程度（1-10）
- `{max_rounds}`: 最大讨论轮数

#### 运行时变量（每轮更新）
- `{topic}`: 当前讨论话题
- `{current_round}`: 当前讨论轮次
- `{reply_A}`: AI A的最新发言
- `{reply_B}`: AI B的最新发言
- `{winner}`: 赢家标识（null/AI_A/AI_B/tie）

### 使用技巧

#### 🎯 优化讨论质量

1. **理性程度设置**
   - 7-8分：平衡理性与感性，适合大多数话题
   - 9-10分：高度理性，适合技术或学术话题
   - 5-6分：更偏向感性，适合人文或艺术话题

2. **风格差异化**
   - 让两个AI有不同的观点倾向
   - 例如：技术专家 vs 哲学家，数据分析师 vs 心理学家

3. **话题选择**
   - 选择有争议性的话题能产生更精彩的讨论
   - 避免过于技术性或过于简单的话题

#### ⏱️ 控制讨论长度

1. **轮数设置**
   - 简单话题：6-8轮
   - 复杂话题：10-12轮
   - 深度讨论：15轮以上

2. **结束条件**
   - AI主动认输
   - 达到最大轮数限制
   - 讨论陷入僵局（重复观点）

#### 💾 保存和回顾

- 讨论结束后可选择保存记录
- 保存文件包含完整讨论内容和统计信息
- 支持后续分析和分享

## 🔧 高级配置

### 自定义提示词模板

您可以通过修改 `config.ini` 中的提示词模板来自定义AI的行为：

```ini
[PROMPTS]
prompt_template_A = 【角色】你是一位喜欢和朋友讨论话题的普通人(AI_A)...
prompt_template_B = 【角色】你是一位喜欢和朋友讨论话题的普通人(AI_B)...
```

### 环境变量配置

可以通过环境变量设置API密钥：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 日志配置

系统支持不同级别的日志记录：

```ini
[SYSTEM]
log_level = INFO  # DEBUG, INFO, WARNING, ERROR
log_file = discussion.log
```

## 🐛 故障排除

### 常见问题及解决方案

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| **API连接失败** | 网络问题或API密钥错误 | 检查网络连接，验证API密钥 |
| **讨论质量不佳** | 配置参数不当 | 调整理性程度，修改AI风格 |
| **程序运行缓慢** | 网络延迟或API限制 | 检查网络状况，适当减少轮数 |
| **提示词生成错误** | 模板格式问题 | 检查config.ini中的模板格式 |
| **讨论无法结束** | 结束条件设置问题 | 调整最大轮数或理性程度 |

### 调试模式

启用详细日志输出：

```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from cli_interface import main
main()
"
```

### 性能优化

1. **减少API调用延迟**
   - 使用更快的网络连接
   - 适当调整超时设置

2. **优化讨论质量**
   - 选择合适的理性程度
   - 设置合理的最大轮数

3. **内存管理**
   - 定期清理讨论历史
   - 限制单次讨论的最大轮数

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 如何贡献

1. **Fork** 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 **Pull Request**

### 贡献类型

- 🐛 **Bug修复**: 修复已知问题
- ✨ **新功能**: 添加新特性
- 📚 **文档改进**: 完善文档
- 🎨 **界面优化**: 改进用户体验
- ⚡ **性能优化**: 提升系统性能

### 开发环境设置

```bash
# 克隆项目
git clone <repository-url>
cd AI讨论赛

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/
```

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 🙏 致谢

- 感谢所有贡献者的努力
- 感谢开源社区的支持
- 特别感谢AI模型提供商的API服务

## 📞 联系我们

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: your-email@example.com

---

<div align="center">

**🌟 如果这个项目对您有帮助，请给我们一个Star！**

*让AI讨论变得更加有趣和智能* 🚀

</div>