import os
import sys
import subprocess
import platform
import time
import threading
from datetime import datetime

# 检查并尝试导入 psutil，如果没有则跳过
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("注意: psutil 模块未安装，部分功能可能受限")
    print("可以运行: pip install psutil")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("           Ollama AI 模型管理器 v1.1.7465")
    print("=" * 60)
    print(f"系统: {platform.system()} {platform.release()}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_ollama():
    """检查 Ollama 是否安装"""
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return True, result.stdout.strip() if result.stdout else "已安装"
    except FileNotFoundError:
        return False, "未找到 ollama 命令"
    except subprocess.TimeoutExpired:
        return True, "已安装（检查超时）"
    except Exception as e:
        return False, f"检查失败: {str(e)}"

def print_menu():
    clear_screen()
    print_header()
    
    # 检查 Ollama 状态
    ollama_installed, ollama_status = check_ollama()
    
    print(f"\n状态: Ollama - {'✅' if ollama_installed else '❌'} {ollama_status}")
    
    if HAS_PSUTIL:
        # 检查是否在运行
        running = False
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    running = True
                    break
        except:
            pass
        print(f"服务: {'✅ 运行中' if running else '❌ 未运行'}")
    
    print("\n" + "=" * 40)
    print("        主菜单")
    print("=" * 40)
    print()
    print(" 1. 📦 启动 Ollama 服务")
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

def start_service():
    print("\n🚀 正在启动 Ollama 服务...")
    
    # 检查是否已经在运行
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'ollama' in proc.info['name'].lower():
            print("⚠️  Ollama服务已在运行")
            input("\n按回车键继续...")
            return
    
    # 启动新服务
    try:
        if platform.system() == "Windows":
            # 在Windows上启动
            subprocess.Popen(["ollama", "serve"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # 在Linux/Mac上启动
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
        
        print("✅ Ollama服务已启动")
        time.sleep(2)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
    
    input("\n按回车键继续...")

def stop_service():
    """停止 Ollama 服务 - 兼容打包版本"""
    print("\n🛑 正在停止 Ollama 服务...\n")
    
    stopped = False
    
    # 方法1: 使用 taskkill (Windows)
    if platform.system() == "Windows":
        try:
            # 尝试停止 ollama.exe 进程
            subprocess.run(
                ["taskkill", "/f", "/im", "ollama.exe"],
                capture_output=True,
                timeout=10
            )
            stopped = True
            print("✅ 已发送停止命令")
        except:
            pass
    
    # 方法2: 查找并停止所有 ollama 相关进程
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                    proc.terminate()
                    stopped = True
                    print(f"✅ 停止进程: {proc.info['name']}")
            except:
                continue
    except ImportError:
        print("⚠️  psutil 不可用，使用系统命令")
    
    # 方法3: 使用系统命令 (跨平台)
    if not stopped:
        try:
            if platform.system() == "Windows":
                # 查找并停止所有 ollama 进程
                result = subprocess.run(
                    ["wmic", "process", "where", "name='ollama.exe'", "delete"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["pkill", "-f", "ollama"], timeout=10)
            else:  # Linux
                subprocess.run(["pkill", "ollama"], timeout=10)
                subprocess.run(["killall", "ollama"], timeout=10)
            
            stopped = True
            print("✅ 使用系统命令停止服务")
        except:
            pass
    
    if stopped:
        print("\n✅ Ollama 服务已停止")
    else:
        print("\n⚠️  未找到运行中的 Ollama 服务，或已停止")
    
    input("\n按回车键返回菜单...")

def list_models():
    """列出所有模型"""
    clear_screen()
    print_header()
    print("\n📋 正在获取模型列表...\n")
    
    try:
        result = subprocess.run(["ollama", "list"], 
                              capture_output=True, 
                              text=True,
                              encoding='utf-8',
                              timeout=10)
        
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
            print("\n提示: 使用选项 5 下载新模型")
            
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
        result = subprocess.run(["ollama", "list"], 
                              capture_output=True, 
                              text=True,
                              timeout=8)
        
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
        process = subprocess.run(["ollama", "run", model_name],
                               text=True,
                               encoding='utf-8')
        
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
    print(" 7. 输入自定义模型   - 若不知道其他模型，请访问https://ollama.com/library后填写完整模型名称")
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
        process = subprocess.Popen(["ollama", "pull", model_name],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 bufsize=1,
                                 encoding='utf-8')
        
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
        result = subprocess.run(["ollama", "list"], 
                              capture_output=True, 
                              text=True,
                              timeout=8)
        
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
        result = subprocess.run(["ollama", "rm", model_name], 
                              capture_output=True, 
                              text=True,
                              timeout=30)
        
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
    print(f"当前用户: {os.getlogin()}")
    print()
    
    # 检查 Ollama
    ollama_installed, ollama_status = check_ollama()
    print(f"Ollama状态: {'✅' if ollama_installed else '❌'} {ollama_status}")
    
    # 检查进程
    if HAS_PSUTIL:
        try:
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
    
    # 检查磁盘空间
    try:
        if platform.system() == "Windows":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            total_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p("C:"), 
                None, 
                ctypes.pointer(total_bytes), 
                ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / (1024**3)
            total_gb = total_bytes.value / (1024**3)
            used_percent = (1 - free_gb/total_gb) * 100
            print(f"磁盘空间: C盘 {free_gb:.1f}GB / {total_gb:.1f}GB 可用 ({used_percent:.1f}% 已用)")
        else:
            stat = os.statvfs('/')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
            used_percent = (1 - free_gb/total_gb) * 100
            print(f"磁盘空间: / {free_gb:.1f}GB / {total_gb:.1f}GB 可用 ({used_percent:.1f}% 已用)")
    except:
        print("磁盘空间: ⚠️  检查失败")
    
    print()
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
            os.path.join(os.environ.get('LOCALAPPDATA', ''), "Ollama"),
            os.path.join(os.environ.get('PROGRAMDATA', ''), "Ollama"),
        ]
    elif platform.system() == "Darwin":  # macOS
        possible_paths = [
            os.path.join(home, ".ollama"),
            os.path.join(home, "Library", "Application Support", "ollama"),
            "/usr/local/share/ollama",
        ]
    else:  # Linux
        possible_paths = [
            os.path.join(home, ".ollama"),
            "/usr/share/ollama",
            "/var/lib/ollama",
            "/opt/ollama",
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
        else:
            print(f"❌ 不存在: {path}")
    
    if not found:
        print("\n⚠️  未找到 Ollama 文件夹")
        print("\n可能的原因:")
        print("1. Ollama 未安装")
        print("2. 模型文件夹在非标准位置")
        print("3. 还没有下载任何模型")
        print("\n建议:")
        print("1. 先安装 Ollama")
        print("2. 下载一个模型")
        print("3. 再尝试打开文件夹")
    
    input("\n按回车键返回菜单...")

def system_settings():
    """系统设置"""
    clear_screen()
    print_header()
    print("\n⚙️  系统设置\n")
    
    print("1. 检查依赖安装")
    print("2. 查看环境变量")
    print("3. 查看系统路径")
    print("4. 返回主菜单")
    print()
    
    choice = input("请选择: ").strip()
    
    if choice == "1":
        clear_screen()
        print_header()
        print("\n🔧 检查依赖安装\n")
        
        # 检查 Python 包
        print("Python 包检查:")
        print("-" * 40)
        
        try:
            import psutil
            print("✅ psutil: 已安装")
        except ImportError:
            print("❌ psutil: 未安装")
            print("   安装命令: pip install psutil")
        
        # 检查 Ollama
        print()
        print("Ollama 检查:")
        print("-" * 40)
        ollama_installed, ollama_status = check_ollama()
        print(f"Ollama: {'✅' if ollama_installed else '❌'} {ollama_status}")
        
        if not ollama_installed:
            print("\n💡 安装建议:")
            print("1. 访问: https://ollama.com/download")
            print("2. 下载对应系统的安装包")
            print("3. 安装并重启终端")
        
        input("\n按回车键返回设置...")
        system_settings()
        
    elif choice == "2":
        clear_screen()
        print_header()
        print("\n🌐 环境变量\n")
        
        print("PATH 环境变量:")
        print("-" * 60)
        path_value = os.environ.get('PATH', '')
        paths = path_value.split(';' if platform.system() == 'Windows' else ':')
        
        for i, p in enumerate(paths[:20], 1):  # 只显示前20个
            if 'ollama' in p.lower():
                print(f"{i:2d}. ✅ {p}")
            else:
                print(f"{i:2d}.    {p}")
        
        if len(paths) > 20:
            print(f"... 还有 {len(paths)-20} 个路径")
        
        print("-" * 60)
        input("\n按回车键返回设置...")
        system_settings()
        
    elif choice == "3":
        clear_screen()
        print_header()
        print("\n🗺️  系统路径\n")
        
        print("重要路径:")
        print("-" * 60)
        print(f"当前目录: {os.getcwd()}")
        print(f"用户目录: {os.path.expanduser('~')}")
        print(f"临时目录: {os.environ.get('TEMP', os.environ.get('TMPDIR', '/tmp'))}")
        print(f"程序目录: {sys.executable}")
        
        # 查找可能的 Ollama 安装位置
        print("\nOllama 可能位置:")
        search_paths = ['ollama', 'ollama.exe']
        if platform.system() == 'Windows':
            search_paths.extend([r'C:\Program Files\Ollama', r'C:\Program Files (x86)\Ollama'])
        
        for path in search_paths:
            try:
                result = subprocess.run(["where" if platform.system() == "Windows" else "which", path], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    print(f"✅ {result.stdout.strip()}")
            except:
                pass
        
        print("-" * 60)
        input("\n按回车键返回设置...")
        system_settings()
    
    elif choice == "4":
        return
    
    else:
        print("❌ 无效选择")
        time.sleep(1)
        system_settings()

def main():
    """主函数"""
    # 显示欢迎信息
    clear_screen()
    print_header()
    print("\n🎉 欢迎使用 Ollama AI 模型管理器")
    print("\n正在初始化...")
    
    # 检查 Ollama
    installed, status = check_ollama()
    if not installed:
        print(f"\n⚠️  警告: {status}")
        print("\n使用前请确保:")
        print("1. 已安装 Ollama (https://ollama.com)")
        print("2. 已将 Ollama 添加到系统 PATH")
        print("3. 可能需要重启终端")
    
    time.sleep(2)
    
    # 主循环
    while True:
        try:
            print_menu()
            choice = input("\n请输入选项 [0-9]: ").strip()
            
            if choice == "0":
                clear_screen()
                print_header()
                print("\n👋 感谢使用 Ollama AI 模型管理器！")
                print("再见！\n")
                time.sleep(1)
                break
                
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
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序崩溃: {str(e)}")
        input("\n按回车键退出...")