#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama AI 模型管理器 - 整合版（带询问安装）
"""

import os
import sys
import subprocess
import platform
import time
from datetime import datetime

# 全局变量
HAS_PSUTIL = False
PSUTIL_VERSION = None

# ============ 第一部分：基础函数 ============
def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印程序头"""
    print("=" * 60)
    print("          Ollama AI 模型管理器 v2.0")
    print("=" * 60)
    print(f"系统: {platform.system()} {platform.release()}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_ollama():
    """检查 Ollama 是否安装"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip() if result.stdout else "已安装"
            return True, version
        else:
            return False, "命令执行失败"
    except FileNotFoundError:
        return False, "未安装"
    except subprocess.TimeoutExpired:
        return True, "检查超时"
    except Exception as e:
        return False, f"错误: {str(e)[:30]}"

# ============ 第二部分：初始化检查 ============
def initialize_program():
    """初始化程序 - 检查并询问是否安装"""
    clear_screen()
    print_header()
    print("\n🔍 正在初始化系统...\n")
    
    # 1. 检查 Ollama（必需）
    print("1. 检查 Ollama...")
    ollama_installed, ollama_status = check_ollama()
    
    if not ollama_installed:
        print(f"   ❌ {ollama_status}")
        print("\n⚠️  错误: Ollama 未安装或未找到!")
        print("\n请先执行以下步骤:")
        print("1. 访问 https://ollama.com/download")
        print("2. 下载并安装 Ollama")
        print("3. 将 Ollama 添加到系统 PATH")
        print("4. 重启本程序")
        print("\n按回车键退出程序...")
        input()
        return False
    
    print(f"   ✅ {ollama_status}")
    
    # 2. 检查 psutil（可选，询问是否安装）
    print("\n2. 检查 psutil...")
    global HAS_PSUTIL, PSUTIL_VERSION
    
    try:
        import psutil
        HAS_PSUTIL = True
        PSUTIL_VERSION = psutil.__version__
        print(f"   ✅ 已安装 (版本: {PSUTIL_VERSION})")
        
    except ImportError:
        HAS_PSUTIL = False
        PSUTIL_VERSION = None
        print("   ⚠️  未安装")
        
        # 询问用户是否要安装
        ask_install_psutil()
    
    # 显示初始化结果
    print("\n" + "=" * 60)
    print("✅ 初始化完成!")
    print("=" * 60)
    
    if not HAS_PSUTIL:
        print("\n💡 提示: 部分功能受限")
        print("可在系统设置中查看安装说明")
    
    time.sleep(2)
    return True

def ask_install_psutil():
    """询问用户是否安装 psutil"""
    print("\n" + "=" * 50)
    print("是否要安装 psutil 以获得完整功能？")
    print("=" * 50)
    print("\npsutil 提供更好的:")
    print("  • 进程管理功能")
    print("  • 系统状态监控")
    print("\n安装选项:")
    print("  1. 自动安装 (推荐)")
    print("  2. 查看手动安装说明")
    print("  3. 跳过，使用基本功能")
    print()
    
    while True:
        try:
            choice = input("请选择 [1-3]: ").strip()
            
            if choice == "1":
                if try_install_psutil():
                    # 安装成功，重新导入
                    try:
                        import psutil
                        global HAS_PSUTIL, PSUTIL_VERSION
                        HAS_PSUTIL = True
                        PSUTIL_VERSION = psutil.__version__
                        print(f"\n🎉 psutil {PSUTIL_VERSION} 安装成功！")
                        time.sleep(2)
                    except:
                        print("\n⚠️  安装成功但导入失败，请重启程序")
                break
                
            elif choice == "2":
                show_manual_installation_guide()
                # 返回后继续询问
                print("\n请选择安装方式:")
                print("  1. 自动安装 (推荐)")
                print("  2. 查看手动安装说明")
                print("  3. 跳过，使用基本功能")
                print()
                continue
                
            elif choice == "3":
                print("\n⚠️  已跳过安装，部分功能受限")
                print("可在系统设置中重新安装")
                break
                
            else:
                print("❌ 无效选择，请输入 1-3")
                
        except KeyboardInterrupt:
            print("\n\n已取消安装")
            break

def try_install_psutil():
    """尝试安装 psutil"""
    print("\n正在尝试安装 psutil...")
    
    python_exe = sys.executable
    print(f"使用 Python: {python_exe}")
    print()
    
    # 尝试不同的安装方法
    methods = [
        ("标准安装", [python_exe, "-m", "pip", "install", "psutil"]),
        ("用户目录安装", [python_exe, "-m", "pip", "install", "--user", "psutil"]),
    ]
    
    # 添加国内镜像源
    mirror_sources = [
        ("清华镜像", "https://pypi.tuna.tsinghua.edu.cn/simple"),
        ("阿里镜像", "https://mirrors.aliyun.com/pypi/simple/"),
        ("豆瓣镜像", "https://pypi.douban.com/simple/"),
    ]
    
    for mirror_name, mirror_url in mirror_sources:
        methods.append((f"{mirror_name}镜像", 
                       [python_exe, "-m", "pip", "install", "psutil", "-i", mirror_url]))
    
    for i, (method_name, cmd) in enumerate(methods, 1):
        print(f"尝试方法 {i}/{len(methods)}: {method_name}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=90
            )
            
            if result.returncode == 0:
                print(" ✅ 成功")
                return True
            else:
                print(" ❌ 失败")
                
        except subprocess.TimeoutExpired:
            print(" ⏰ 超时")
        except Exception as e:
            print(f" ❌ 错误: {str(e)[:50]}")
    
    print("\n❌ 所有安装方法都失败了")
    return False

def show_manual_installation_guide():
    """显示手动安装指南"""
    clear_screen()
    print_header()
    print("\n📖 psutil 手动安装指南")
    print("=" * 60)
    
    print("\n方法1: 使用 pip 命令")
    print("-" * 40)
    print("打开命令提示符或终端，输入:")
    print()
    print("  pip install psutil")
    print()
    
    print("\n方法2: 使用国内镜像加速（推荐）")
    print("-" * 40)
    print("国内用户可以使用以下镜像源:")
    print()
    print("  # 清华大学镜像")
    print("  pip install psutil -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print()
    print("  # 阿里云镜像")
    print("  pip install psutil -i https://mirrors.aliyun.com/pypi/simple/")
    print()
    print("  # 豆瓣镜像")
    print("  pip install psutil -i https://pypi.douban.com/simple/")
    print()
    
    print("\n安装后，请重启本程序")
    print("=" * 60)
    input("\n按回车键返回...")

# ============ 第三部分：主菜单系统 ============
def print_menu():
    """打印主菜单"""
    clear_screen()
    print_header()
    
    # 检查 Ollama 状态
    ollama_installed, ollama_status = check_ollama()
    
    # 显示状态
    print(f"\n📊 系统状态:")
    print(f"   Ollama: {'✅' if ollama_installed else '❌'} {ollama_status}")
    
    if HAS_PSUTIL:
        print(f"   psutil: ✅ 已安装 (v{PSUTIL_VERSION})")
    else:
        print(f"   psutil: ⚠️  未安装 (部分功能受限)")
    
    print("\n" + "=" * 40)
    print("         主菜单")
    print("=" * 40)
    print()
    print(" 1. 🚀 启动 Ollama 服务")
    print(" 2. 🛑 停止 Ollama 服务")
    print(" 3. 📋 查看模型列表")
    print(" 4. 💬 与模型对话")
    print(" 5. ⬇️  下载新模型")
    print(" 6. 🗑️  删除模型")
    print(" 7. 🔍 检查系统状态")
    print(" 8. 📁 打开模型文件夹")
    print(" 9. ⚙️  系统设置")
    print(" 0. 🚪 退出程序")
    print()
    print("=" * 40)

# ============ 第四部分：核心功能函数 ============
def start_service():
    """启动 Ollama 服务"""
    clear_screen()
    print_header()
    print("\n🚀 启动 Ollama 服务\n")
    
    # 检查是否已经在运行
    if is_ollama_running():
        print("⚠️  Ollama 服务已经在运行!")
        input("\n按回车键返回菜单...")
        return
    
    print("将在新窗口中启动服务...")
    print("请勿关闭服务窗口!")
    print()
    
    try:
        if platform.system() == "Windows":
            subprocess.Popen(
                ["start", "cmd", "/k", "ollama serve"],
                shell=True
            )
        else:
            subprocess.Popen(
                ["xterm", "-e", "ollama serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        print("✅ 服务启动命令已发送")
        print("正在等待服务初始化...")
        
        for i in range(5, 0, -1):
            print(f"等待 {i} 秒...", end='\r')
            time.sleep(1)
        
        print("\n\n✅ Ollama 服务应该已经启动")
        print("如果遇到问题，请手动检查服务窗口")
        
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        print("\n请尝试手动启动:")
        print("1. 打开命令提示符")
        print("2. 输入: ollama serve")
        print("3. 保持窗口打开")
    
    input("\n按回车键返回菜单...")

def is_ollama_running():
    """检查 Ollama 是否在运行"""
    if HAS_PSUTIL:
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    return True
        except:
            pass
    
    # 备用检查方法（不使用 psutil）
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["tasklist", "/fi", "imagename eq ollama.exe"],
                capture_output=True,
                text=True
            )
            return "ollama.exe" in result.stdout
        else:
            result = subprocess.run(
                ["pgrep", "-f", "ollama"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
    except:
        return False

def stop_service():
    """停止 Ollama 服务"""
    clear_screen()
    print_header()
    print("\n🛑 停止 Ollama 服务\n")
    
    if not is_ollama_running():
        print("ℹ️  Ollama 服务未在运行")
        input("\n按回车键返回菜单...")
        return
    
    stopped = False
    
    # 如果有 psutil，使用更优雅的方式
    if HAS_PSUTIL:
        stopped = stop_with_psutil()
    else:
        # 使用系统命令
        stopped = stop_with_system_commands()
    
    if stopped:
        print("\n✅ Ollama 服务已停止")
    else:
        print("\n⚠️  无法自动停止服务")
        print("\n请尝试手动操作:")
        if platform.system() == "Windows":
            print("1. 按 Ctrl+Shift+Esc 打开任务管理器")
            print("2. 找到 'ollama.exe' 进程")
            print("3. 右键点击 → 结束任务")
        else:
            print("1. 打开终端")
            print("2. 运行: pkill ollama")
            print("3. 或运行: killall ollama")
    
    input("\n按回车键返回菜单...")

def stop_with_psutil():
    """使用 psutil 停止服务"""
    try:
        import psutil
        stopped_count = 0
        
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    print(f"  正在停止进程 {proc.info['pid']}...")
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except:
                        proc.kill()
                    stopped_count += 1
            except:
                continue
        
        return stopped_count > 0
    except Exception as e:
        print(f"  使用 psutil 失败: {str(e)}")
        return False

def stop_with_system_commands():
    """使用系统命令停止服务"""
    system = platform.system()
    
    try:
        if system == "Windows":
            print("  尝试 taskkill...")
            result = subprocess.run(
                ["taskkill", "/f", "/im", "ollama.exe"],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode != 0:
                print("  尝试 WMIC...")
                subprocess.run(
                    ["wmic", "process", "where", "name='ollama.exe'", "delete"],
                    capture_output=True,
                    timeout=5
                )
            
        elif system == "Darwin":  # macOS
            print("  尝试 pkill...")
            subprocess.run(["pkill", "-f", "ollama"], timeout=5)
            
        else:  # Linux
            print("  尝试 pkill...")
            subprocess.run(["pkill", "ollama"], timeout=5)
            subprocess.run(["killall", "ollama"], timeout=5)
        
        return True
        
    except Exception as e:
        print(f"  系统命令失败: {str(e)}")
        return False

def list_models():
    """列出所有模型"""
    clear_screen()
    print_header()
    print("\n📋 获取模型列表...\n")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            print("=" * 50)
            print("            已下载模型")
            print("=" * 50)
            print(result.stdout)
            print("=" * 50)
            
            # 统计模型数量
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                model_count = len(lines) - 1
                print(f"\n📊 总计: {model_count} 个模型")
            else:
                print("\n📊 总计: 0 个模型")
        else:
            print("❌ 未找到任何模型")
            print("\n💡 提示: 使用选项 5 下载新模型")
            
    except subprocess.TimeoutExpired:
        print("❌ 获取模型列表超时")
        print("请检查 Ollama 服务是否运行")
    except Exception as e:
        print(f"❌ 获取模型列表失败: {str(e)}")
    
    input("\n按回车键返回菜单...")

def chat_with_model():
    """与模型对话"""
    clear_screen()
    print_header()
    print("\n💬 模型对话模式\n")
    
    # 先获取模型列表
    print("正在获取可用模型...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=8
        )
        
        if result.returncode == 0 and result.stdout:
            print("\n📋 可用模型:")
            print("-" * 40)
            print(result.stdout)
            print("-" * 40)
        else:
            print("⚠️  没有找到模型，请先下载模型")
            input("\n按回车键返回菜单...")
            return
            
    except Exception as e:
        print(f"❌ 获取模型列表失败: {str(e)}")
        input("\n按回车键返回菜单...")
        return
    
    # 获取用户输入的模型名称
    print()
    model_name = input("请输入要对话的模型名称: ").strip()
    
    if not model_name:
        print("❌ 模型名称不能为空")
        input("\n按回车键返回菜单...")
        return
    
    clear_screen()
    print_header()
    print(f"\n🤖 正在启动 {model_name} 对话...")
    print("=" * 60)
    print("提示:")
    print("  • 输入 '/bye' 或 '/exit' 退出对话")
    print("  • 输入 '/help' 查看帮助")
    print("  • 按 Ctrl+D 强制退出")
    print("=" * 60)
    print("\n开始对话:\n")
    
    try:
        # 直接运行对话
        process = subprocess.run(
            ["ollama", "run", model_name],
            text=True,
            encoding='utf-8'
        )
        
        if process.returncode != 0:
            print(f"\n❌ 对话异常结束 (代码: {process.returncode})")
            
    except KeyboardInterrupt:
        print("\n\n🛑 对话被用户中断")
    except FileNotFoundError:
        print(f"\n❌ 找不到模型 '{model_name}'")
        print("请检查模型名称是否正确")
    except Exception as e:
        print(f"\n❌ 对话过程出错: {str(e)}")
    
    print("\n" + "=" * 60)
    input("\n按回车键返回菜单...")

def download_model():
    """下载新模型"""
    clear_screen()
    print_header()
    print("\n⬇️  下载新模型\n")
    
    print("推荐模型列表（模型名的后缀表示有多少个指令，指令越多，功能越强）:")
    print("-" * 50)
    print(" 1. llama3.2:1b     - 1B参数，最小最快")
    print(" 2. phi3:mini       - 3.8B，性能优秀（推荐）")
    print(" 3. qwen2.5:0.5b    - 0.5B，中文优化最小")
    print(" 4. llama3.2        - 8B，标准版本")
    print(" 5. mistral         - 7B，法语优化")
    print(" 6. gemma2:2b       - 2B，谷歌轻量版")
    print(" 7. 输入自定义模型   - 若不知道其他模型，请访问 https://ollama.com/library 后将您要下载的模型的完整名称填写到下方")
    print("-" * 50)
    print()
    
    choice = input("请选择 (1-7): ").strip()
    
    model_map = {
        '1': 'llama3.2:1b',
        '2': 'phi3:mini',
        '3': 'qwen2.5:0.5b',
        '4': 'llama3.2',
        '5': 'mistral',
        '6': 'gemma2:2b'
    }
    
    if choice in model_map:
        model_name = model_map[choice]
    elif choice == '7':
        model_name = input("\n请输入完整的模型名称: ").strip()
    else:
        print("❌ 无效选择")
        input("\n按回车键返回菜单...")
        return
    
    if not model_name:
        print("❌ 模型名称不能为空")
        input("\n按回车键返回菜单...")
        return
    
    clear_screen()
    print_header()
    print(f"\n⬇️  正在下载模型: {model_name}")
    print("=" * 60)
    print("注意:")
    print("  • 下载时间取决于模型大小和网络速度")
    print("  • 大模型可能需要数十分钟")
    print("  • 按 Ctrl+C 可以取消下载")
    print("=" * 60)
    print()
    
    try:
        # 显示实时进度
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8'
        )
        
        print("下载进度:")
        print("-" * 40)
        
        # 读取输出
        for line in process.stdout:
            line = line.strip()
            if line:
                print(f"  {line}")
        
        process.wait()
        
        if process.returncode == 0:
            print("-" * 40)
            print(f"\n🎉 下载完成! 模型 '{model_name}' 已成功安装")
        else:
            print("\n❌ 下载失败")
            print("可能的原因:")
            print("  • 网络连接问题")
            print("  • 模型名称错误")
            print("  • 磁盘空间不足")
            
    except KeyboardInterrupt:
        print("\n\n🛑 下载已取消")
    except Exception as e:
        print(f"\n❌ 下载出错: {str(e)}")
    
    input("\n按回车键返回菜单...")

def delete_model():
    """删除模型"""
    clear_screen()
    print_header()
    print("\n🗑️  删除模型\n")
    
    print("正在获取模型列表...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=8
        )
        
        if result.returncode == 0 and result.stdout:
            print("\n当前模型:")
            print("-" * 40)
            print(result.stdout)
            print("-" * 40)
        else:
            print("❌ 没有找到可删除的模型")
            input("\n按回车键返回菜单...")
            return
            
    except Exception as e:
        print(f"❌ 获取模型列表失败: {str(e)}")
        input("\n按回车键返回菜单...")
        return
    
    print()
    model_name = input("请输入要删除的模型名称: ").strip()
    
    if not model_name:
        print("❌ 模型名称不能为空")
        input("\n按回车键返回菜单...")
        return
    
    # 确认删除
    print()
    confirm = input(f"⚠️  确定要永久删除模型 '{model_name}' 吗？ (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("删除操作已取消")
        input("\n按回车键返回菜单...")
        return
    
    print(f"\n正在删除模型 '{model_name}'...")
    
    try:
        result = subprocess.run(
            ["ollama", "rm", model_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ 模型 '{model_name}' 已成功删除")
        else:
            print(f"❌ 删除失败: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ 删除操作超时")
    except Exception as e:
        print(f"❌ 删除出错: {str(e)}")
    
    input("\n按回车键返回菜单...")

def check_system_status():
    """检查系统状态"""
    clear_screen()
    print_header()
    print("\n🔍 系统状态检查\n")
    
    print("=" * 50)
    print("          系统信息")
    print("=" * 50)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"系统架构: {platform.machine()}")
    print(f"Python版本: {platform.python_version()}")
    print()
    
    # 检查 Ollama
    ollama_installed, ollama_status = check_ollama()
    print(f"Ollama状态: {'✅' if ollama_installed else '❌'} {ollama_status}")
    
    # 检查进程（如果有 psutil）
    if HAS_PSUTIL:
        try:
            import psutil
            ollama_count = 0
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    ollama_count += 1
            
            if ollama_count > 0:
                print(f"Ollama进程: ✅ 运行中 ({ollama_count} 个进程)")
            else:
                print("Ollama进程: ❌ 未运行")
        except:
            print("Ollama进程: ⚠️  检查失败")
    else:
        print("Ollama进程: ⚠️  psutil未安装，无法检查")
    
    print("=" * 50)
    
    input("\n按回车键返回菜单...")

def open_model_folder():
    """打开模型文件夹"""
    clear_screen()
    print_header()
    print("\n📁 打开模型文件夹\n")
    
    # Ollama 默认存储路径
    home = os.path.expanduser("~")
    possible_paths = []
    
    if platform.system() == "Windows":
        possible_paths = [
            os.path.join(home, ".ollama"),
            os.path.join(home, "AppData", "Local", "Ollama"),
            os.path.join(home, "AppData", "Local", "Programs", "Ollama"),
        ]
    elif platform.system() == "Darwin":  # macOS
        possible_paths = [
            os.path.join(home, ".ollama"),
            os.path.join(home, "Library", "Application Support", "ollama"),
        ]
    else:  # Linux
        possible_paths = [
            os.path.join(home, ".ollama"),
            "/usr/share/ollama",
            "/var/lib/ollama",
        ]
    
    print("正在查找 Ollama 文件夹...")
    print()
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到: {path}")
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", path])
                else:
                    subprocess.run(["xdg-open", path])
                print(f"已打开文件夹")
                found = True
                break
            except Exception as e:
                print(f"打开失败: {str(e)}")
    
    if not found:
        print("\n⚠️  未找到 Ollama 文件夹")
        print("\n可能的原因:")
        print("1. Ollama 未安装")
        print("2. 还没有下载任何模型")
    
    input("\n按回车键返回菜单...")

def system_settings():
    """系统设置"""
    clear_screen()
    print_header()
    print("\n⚙️  系统设置\n")
    
    print("1. 重新安装 psutil")
    print("2. 测试 Ollama 连接")
    print("3. 查看环境变量")
    print("4. 查看安装说明")
    print("5. 返回主菜单")
    print()
    
    choice = input("请选择: ").strip()
    
    if choice == "1":
        reinstall_psutil()
    elif choice == "2":
        test_ollama_connection()
    elif choice == "3":
        show_environment_variables()
    elif choice == "4":
        show_manual_installation_guide()
        system_settings()
    elif choice == "5":
        return
    else:
        print("❌ 无效选择")
        time.sleep(1)
        system_settings()

def reinstall_psutil():
    """重新安装 psutil"""
    clear_screen()
    print_header()
    print("\n🔄 重新安装 psutil\n")
    
    global HAS_PSUTIL, PSUTIL_VERSION
    
    # 检查当前状态
    if HAS_PSUTIL:
        print(f"当前已安装: psutil v{PSUTIL_VERSION}")
        print("\n是否要重新安装/更新？ (y/N): ", end="")
        confirm = input().strip().lower()
        if confirm not in ['y', 'yes']:
            system_settings()
            return
    
    print("\n开始安装...")
    
    if try_install_psutil():
        # 尝试导入
        try:
            import psutil
            HAS_PSUTIL = True
            PSUTIL_VERSION = psutil.__version__
            print(f"\n✅ 安装成功！版本: {PSUTIL_VERSION}")
            print("部分功能已解锁 ✓")
            time.sleep(2)
        except:
            print("\n⚠️  安装成功但导入失败")
            print("请重启程序")
    else:
        print("\n❌ 安装失败")
        print("请查看手动安装说明")
    
    input("\n按回车键返回设置...")
    system_settings()

def test_ollama_connection():
    """测试 Ollama 连接"""
    clear_screen()
    print_header()
    print("\n🔗 测试 Ollama 连接\n")
    
    print("1. 测试基本连接...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Ollama 版本: {result.stdout.strip()}")
        else:
            print(f"   ❌ 命令失败: {result.stderr}")
    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
    
    print("\n2. 测试服务运行状态...")
    if is_ollama_running():
        print("   ✅ Ollama 服务正在运行")
    else:
        print("   ❌ Ollama 服务未运行")
    
    print("\n3. 测试模型列表...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=8
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                print(f"   ✅ 找到 {len(lines)-1} 个模型")
            else:
                print("   ✅ 连接成功，但无模型")
        else:
            print("   ❌ 获取模型列表失败")
    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
    
    input("\n按回车键返回设置...")
    system_settings()

def show_environment_variables():
    """显示环境变量"""
    clear_screen()
    print_header()
    print("\n🌐 环境变量检查\n")
    
    print("正在检查系统 PATH...")
    print("-" * 60)
    
    # 获取 PATH 环境变量
    path_value = os.environ.get('PATH', '')
    paths = path_value.split(';' if platform.system() == 'Windows' else ':')
    
    # 检查 ollama 是否在 PATH 中
    ollama_found = False
    ollama_paths = []
    
    for i, p in enumerate(paths, 1):
        # 清理路径
        p_clean = p.strip()
        if not p_clean:
            continue
            
        # 检查是否包含 ollama
        if 'ollama' in p_clean.lower():
            ollama_found = True
            ollama_paths.append(p_clean)
            print(f"{i:3d}. ✅ {p_clean}")
        else:
            # 只显示前20个非ollama路径
            if i <= 20:
                print(f"{i:3d}.    {p_clean}")
    
    if len(paths) > 20 and not ollama_found:
        print(f"... 还有 {len(paths)-20} 个路径")
    
    print("-" * 60)
    
    # 更详细的检查
    print("\n🔍 详细检查结果:")
    print("-" * 40)
    
    # 方法1：检查环境变量
    print("1. PATH环境变量检查:")
    if ollama_found:
        print(f"   ✅ 找到 {len(ollama_paths)} 个包含 'ollama' 的路径")
        for path in ollama_paths:
            print(f"      📍 {path}")
    else:
        print("   ❌ 未在PATH中找到 'ollama'")
    
    # 方法2：尝试运行 ollama 命令
    print("\n2. 命令可执行性检查:")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["where", "ollama"],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            result = subprocess.run(
                ["which", "ollama"],
                capture_output=True,
                text=True,
                timeout=5
            )
        
        if result.returncode == 0:
            print(f"   ✅ 系统找到 ollama: {result.stdout.strip()}")
        else:
            print("   ❌ 系统找不到 ollama 命令")
    except Exception as e:
        print(f"   ⚠️  检查命令失败: {str(e)}")
    
    # 方法3：检查常见安装位置
    print("\n3. 常见安装位置检查:")
    common_paths = []
    
    if platform.system() == "Windows":
        common_paths = [
            r"C:\Program Files\Ollama",
            r"C:\Program Files (x86)\Ollama",
            os.path.join(os.environ.get('ProgramFiles', ''), "Ollama"),
            os.path.join(os.environ.get('ProgramFiles(x86)', ''), "Ollama"),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), "Programs", "Ollama"),
            os.path.join(os.environ.get('APPDATA', ''), "Local", "Programs", "Ollama"),
        ]
    elif platform.system() == "Darwin":  # macOS
        common_paths = [
            "/usr/local/bin",
            "/opt/homebrew/bin",
            "/Applications/Ollama.app/Contents/MacOS",
            os.path.expanduser("~/.local/bin"),
            os.path.expanduser("~/Applications/Ollama.app/Contents/MacOS"),
        ]
    else:  # Linux
        common_paths = [
            "/usr/local/bin",
            "/usr/bin",
            "/bin",
            "/opt/ollama",
            os.path.expanduser("~/.local/bin"),
            os.path.expanduser("~/bin"),
        ]
    
    found_common = False
    for path in common_paths:
        if os.path.exists(os.path.join(path, "ollama" if platform.system() != "Windows" else "ollama.exe")):
            found_common = True
            print(f"   ✅ 找到: {path}")
            break
    
    if not found_common:
        print("   ⚠️  未在常见位置找到")
    
    # 方法4：直接测试 ollama 命令
    print("\n4. 直接测试 ollama 命令:")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ ollama 命令可执行: {result.stdout.strip()}")
        else:
            print(f"   ⚠️  ollama 命令返回错误: {result.stderr[:50]}")
    except FileNotFoundError:
        print("   ❌ 找不到 ollama 命令")
    except Exception as e:
        print(f"   ⚠️  测试失败: {str(e)}")
    
    print("-" * 40)
    
    # 总结和建议
    print("\n📋 总结:")
    if ollama_found or found_common:
        print("   ✅ Ollama 应该已在 PATH 中或可访问")
    else:
        print("   ⚠️  Ollama 可能未正确添加到 PATH")
        print("\n💡 建议:")
        print("   1. 重启终端/命令提示符")
        print("   2. 重启电脑")
        print("   3. 检查 Ollama 安装是否完整")
        print("   4. 手动将 Ollama 安装目录添加到 PATH")
    
    input("\n按回车键返回设置...")
    system_settings()

# ============ 第五部分：主程序 ============
def main():
    """主程序"""
    # 初始化程序（检查并询问安装）
    if not initialize_program():
        return
    
    # 主循环
    while True:
        try:
            print_menu()
            choice = input("\n请输入选项 [0-9]: ").strip()
            
            if choice == "0":
                # 直接退出
                clear_screen()
                print_header()
                print("\n👋 感谢使用 Ollama AI 模型管理器！")
                print("再见！\n")
                time.sleep(1)
                return  # 直接返回，退出程序
                
            elif choice == "1":
                start_service()
            elif choice == "2":
                stop_service()
            elif choice == "3":
                list_models()
            elif choice == "4":
                chat_with_model()
            elif choice == "5":
                download_model()
            elif choice == "6":
                delete_model()
            elif choice == "7":
                check_system_status()
            elif choice == "8":
                open_model_folder()
            elif choice == "9":
                system_settings()
            else:
                print("❌ 无效选项，请输入 0-9 之间的数字")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 检测到 Ctrl+C，正在退出...")
            time.sleep(1)
            return  # 直接返回，退出程序
            
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            input("\n按回车键继续...")

# ============ 程序入口 ============
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序崩溃: {str(e)}")
        input("\n按回车键退出...")
    finally:
        sys.exit(0)  # 确保程序退出