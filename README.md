# Ollama AI 模型管理器

## 📋 项目简介

**Ollama AI 模型管理器**是一个功能强大的桌面应用程序，专门用于管理和操作 Ollama 本地 AI 模型。通过简洁直观的图形界面，用户可以轻松地下载、运行、管理和与各种 AI 模型进行交互，无需记忆复杂的命令行指令。

![界面预览](https://img.shields.io/badge/界面-简洁友好-blue)
![平台支持](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-green)
![Python版本](https://img.shields.io/badge/Python-3.7+-orange)

## ✨ 主要功能

### 🔄 **模型管理**
- **查看模型列表**：快速浏览已下载的所有 AI 模型
- **一键下载**：支持多种热门模型（llama3.2、phi3、mistral等）
- **删除模型**：清理不再需要的模型，释放磁盘空间

### 💬 **对话交互**
- **实时对话**：与选定的 AI 模型进行自然语言对话
- **多模型支持**：支持所有 Ollama 兼容的模型
- **对话历史**：记录和管理对话内容
- **智能退出**：支持多种退出方式（/bye、Ctrl+D等）

### ⚙️ **服务管理**
- **一键启动**：自动启动 Ollama 后台服务
- **智能停止**：支持多种停止方式（psutil/系统命令）
- **状态监控**：实时监控服务运行状态
- **错误处理**：自动处理常见错误和异常

### 🔧 **系统工具**
- **环境检查**：自动检测系统环境和依赖
- **路径管理**：查看和验证环境变量配置
- **故障排查**：内置常见问题解决方案

## 🚀 快速开始

### 系统要求
- **操作系统**：Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**：3.7 或更高版本
- **Ollama**：必须预先安装 ([下载地址](https://ollama.com))

## 📖 使用指南

### 首次运行
1. **启动程序**：运行 `OllamaManager.exe` 或 `python ollama_manager.py`
2. **环境检查**：程序会自动检查 Ollama 安装状态
3. **依赖安装**：如果缺少 psutil，程序会询问是否安装
4. **开始使用**：选择需要的功能开始操作

### 常用快捷键
- **Ctrl+C**：退出当前操作或程序
- **数字键 0-9**：快速选择菜单选项
- **Enter**：确认选择或输入
- **/bye**：退出对话模式

## 🎯 功能详解

### 1. 模型下载
支持多种热门模型的快速下载：
```
推荐模型：
  • llama3.2:1b    - 1B参数，最小最快
  • phi3:mini      - 3.8B，性能优秀（推荐）
  • qwen2.5:0.5b   - 0.5B，中文优化最小
  • llama3.2       - 8B，标准版本
  • mistral        - 7B，法语优化
  • gemma2:2b      - 2B，谷歌轻量版
```

### 2. 对话系统
```python
# 对话功能特性：
- 支持所有 Ollama 模型
- 实时流式输出
- 对话历史记录
- 智能退出机制
- 错误自动恢复
```

### 3. 服务管理
```bash
# 支持的停止方式：
有 psutil：    优雅终止进程
无 psutil：    使用系统命令
Windows：      taskkill / wmic
macOS/Linux：  pkill / killall
```

## 依赖关系
```yaml
必需依赖:
  - Python 3.7+
  - Ollama (AI引擎)
  - subprocess (系统调用)

推荐依赖:
  - psutil 5.9.0+ (进程管理)
  
可选依赖:
  - pyinstaller (打包工具)
```

## 🔧 配置说明

### 配置文件
程序支持以下配置方式：
- **自动检测**：智能识别系统环境
- **手动配置**：通过系统设置调整
- **环境变量**：支持自定义路径

## 🐛 故障排除

### 常见问题

#### Q1: 程序无法找到 Ollama
**症状**：提示 "Ollama 未安装或未找到"
**解决方案**：
1. 确认 Ollama 已正确安装
2. 重启终端或电脑
3. 检查环境变量 PATH 设置
4. 重新安装 Ollama

#### Q2: 模型下载速度慢
**症状**：下载过程卡顿或失败
**解决方案**：
1. 检查网络连接
2. 尝试使用代理
3. 选择较小的模型（如 llama3.2:1b）
4. 避开网络高峰时段

#### Q3: 对话功能异常
**症状**：对话时程序崩溃或无响应
**解决方案**：
1. 确保 Ollama 服务正在运行
2. 检查模型是否完整下载
3. 尝试重新启动程序
4. 查看错误日志文件

#### Q4: 无法停止服务
**症状**：停止服务功能无效
**解决方案**：
1. 安装 psutil 模块：`pip install psutil`
2. 手动使用任务管理器终止进程
3. 重启电脑

## 🔄 更新日志

### v2.0 (当前版本)
- ✅ 完整的图形界面菜单系统
- ✅ 智能依赖检查和安装
- ✅ 多平台兼容性改进
- ✅ 错误处理和恢复机制
- ✅ 打包为独立可执行文件

### v1.0
- 🎉 初始版本发布
- 🎉 核心功能实现

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 🙏 致谢

- **Ollama 团队**：提供强大的本地 AI 运行环境
- **Python 社区**：丰富的库和工具支持
- **所有贡献者**：感谢你们的代码、建议和反馈

### 获取帮助
- 📖 **文档**：查看本文档和代码注释
- 🐛 **问题反馈**：提交到 [GitHub Issues](https://github.com/kevincoding03-rgb/ollama-manager/issues)
- 💬 **讨论区**：加入社区讨论
- 📧 **邮件支持**：support@example.com

### 资源链接
- 🌐 **官方网站**：[https://ollama.com](https://ollama.com)
- 📚 **API 文档**：[Ollama API Reference](https://github.com/ollama/ollama)
- 👥 **社区论坛**：[Discord 服务器](https://discord.gg/ollama)
