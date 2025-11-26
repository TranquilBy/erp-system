import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import requests
import subprocess
import sys
import shutil
from packaging import version
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FastErpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastErp")
        self.root.geometry("280x340")
        self.root.resizable(False, False)
        
        # 设置深色背景
        self.root.configure(bg='#2c3e50')
        self.root.attributes('-topmost', True)
        
        # GitHub仓库信息 - 请根据你的实际仓库修改
        self.github_repo = "TranquilBy/erp-system"  # 格式：用户名/仓库名
        self.current_version = "1.0.0"  # 当前版本号
        
        # 加载logo
        self.load_logo()
        
        # 创建界面
        self.create_widgets()
        
        # 运行状态
        self.running = False
        
        # 显示启动提示
        self.root.after(100, self.show_startup_message)
        
    def load_logo(self):
        """加载logo图标"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(script_dir, "logo_icon", "logo.jpg")
            
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_icon = ImageTk.PhotoImage(logo_image)
                self.root.iconphoto(True, self.logo_icon)
            else:
                # 如果找不到logo，创建一个简单的默认图标
                self.logo_icon = None
                print("未找到logo文件，使用默认图标")
                
        except Exception as e:
            print(f"加载logo时出错: {e}")
            self.logo_icon = None
    
    def show_startup_message(self):
        """显示启动提示"""
        messagebox.showinfo("FastErp", "快速点击工具已启动")
    
    def create_widgets(self):
        # 顶部按钮区域 - 包含关于更新按钮
        top_frame = tk.Frame(self.root, bg='#2c3e50')
        top_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # 关于更新按钮
        self.update_button = tk.Button(
            top_frame,
            text="关于更新",
            command=self.check_update,
            font=('Arial', 8),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            bd=1,
            padx=8,
            pady=4,
            cursor='hand2',
            highlightthickness=0
        )
        self.update_button.pack(side=tk.LEFT)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 标题
        title_label = tk.Label(
            title_frame, 
            text="FastErp", 
            font=('Arial', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(
            title_frame, 
            text="自动化点击工具", 
            font=('Arial', 9),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # 功能按钮区域 - 垂直排列
        func_frame = tk.Frame(main_frame, bg='#2c3e50')
        func_frame.pack(fill=tk.X, pady=5)
        
        # 坐标点击按钮
        self.func1_button = tk.Button(
            func_frame, 
            text="坐标点击", 
            command=self.execute_function1,
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=1,
            padx=20,
            pady=10,
            cursor='hand2',
            highlightthickness=0
        )
        self.func1_button.pack(fill=tk.X, pady=5)
        
        # 图片点击按钮
        self.func2_button = tk.Button(
            func_frame, 
            text="图片点击", 
            command=self.execute_function2,
            font=('Arial', 10, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            bd=1,
            padx=20,
            pady=10,
            cursor='hand2',
            highlightthickness=0
        )
        self.func2_button.pack(fill=tk.X, pady=5)
        
        # 停止按钮
        self.stop_button = tk.Button(
            main_frame, 
            text="停止执行", 
            command=self.stop_execution,
            font=('Arial', 9, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            bd=1,
            padx=20,
            pady=8,
            cursor='hand2',
            state="disabled",
            highlightthickness=0
        )
        self.stop_button.pack(pady=10)
        
        # 状态区域
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 状态标签
        status_title = tk.Label(
            status_frame, 
            text="状态:", 
            font=('Arial', 9),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        status_title.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            status_frame, 
            text="就绪", 
            font=('Arial', 9, 'bold'),
            fg='#3498db',
            bg='#2c3e50'
        )
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def check_update(self):
        """检查更新"""
        # 检查GitHub仓库是否配置
        if self.github_repo == "your-username/your-repo":
            messagebox.showinfo("关于", 
                              f"FastErp v{self.current_version}\n\n"
                              "GitHub仓库未配置，无法检查更新。\n"
                              "请在代码中配置正确的GitHub仓库信息。")
            return
            
        thread = threading.Thread(target=self._check_update_task)
        thread.daemon = True
        thread.start()
    
    def _check_update_task(self):
        """检查更新的后台任务"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="检查更新中..."))
            
            # 获取最新版本信息 - 添加verify=False绕过SSL验证
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(api_url, timeout=10, verify=False)
            response.raise_for_status()
            release_info = response.json()
            
            latest_version = release_info.get("tag_name", "").lstrip("v")
            release_name = release_info.get("name", "未知版本")
            release_body = release_info.get("body", "无更新说明")
            
            if not latest_version:
                error_msg = "无法获取最新版本信息"
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
                self.root.after(0, lambda: self.status_label.config(text="就绪"))
                return
            
            # 比较版本
            if version.parse(latest_version) > version.parse(self.current_version):
                # 有新版本
                download_url = None
                for asset in release_info.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                
                if download_url:
                    self.root.after(0, lambda lv=latest_version, rn=release_name, rb=release_body, url=download_url: 
                                  self.show_update_dialog(lv, rn, rb, url))
                else:
                    self.root.after(0, lambda lv=latest_version: messagebox.showinfo(
                        "更新", f"发现新版本 {lv}，但未找到可下载的exe文件"))
            else:
                self.root.after(0, lambda cv=self.current_version: messagebox.showinfo(
                    "更新", f"当前已是最新版本 v{cv}"))
                
        except requests.exceptions.Timeout:
            error_msg = "请求超时，请检查网络连接"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        except requests.exceptions.SSLError:
            error_msg = "SSL证书验证失败，请检查网络设置"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求失败: {str(e)}"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        except Exception as e:
            error_msg = f"检查更新时出错: {str(e)}"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))
    
    def show_update_dialog(self, latest_version, release_name, release_body, download_url):
        """显示更新对话框"""
        result = messagebox.askyesno(
            "发现新版本",
            f"发现新版本: {release_name} (v{latest_version})\n\n更新内容:\n{release_body}\n\n是否立即更新?"
        )
        
        if result:
            # 开始下载更新
            self.download_and_update(download_url, latest_version)
    
    def download_and_update(self, download_url, latest_version):
        """下载并更新"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="下载更新中..."))
            
            # 下载新版本 - 添加verify=False
            response = requests.get(download_url, stream=True, timeout=30, verify=False)
            response.raise_for_status()
            
            # 获取当前exe路径
            current_exe = sys.executable
            current_dir = os.path.dirname(current_exe)
            new_exe_path = os.path.join(current_dir, f"FastErp_v{latest_version}.exe")
            
            # 保存下载的文件
            with open(new_exe_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # 创建更新脚本
            update_script = os.path.join(current_dir, "update.bat")
            with open(update_script, 'w', encoding='utf-8') as f:
                f.write(f'''@echo off
timeout /t 1 /nobreak >nul
del "{current_exe}"
move "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
''')
            
            # 执行更新脚本并退出当前程序
            subprocess.Popen(update_script, shell=True)
            self.root.after(0, self.root.quit)
            
        except Exception as e:
            error_msg = f"更新失败: {str(e)}"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
            self.root.after(0, lambda: self.status_label.config(text="就绪"))
    
    def execute_function1(self):
        """执行功能1：坐标点击"""
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
            
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text="5秒后开始...")
        
        # 隐藏窗口
        self.root.withdraw()
        
        thread = threading.Thread(target=self._function1_task)
        thread.daemon = True
        thread.start()
        
    def _function1_task(self):
        """功能1的后台任务"""
        try:
            # 设置瞬间点击
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0
            pyautogui.PAUSE = 0
            
            # 5秒预备时间
            for i in range(5, 0, -1):
                if not self.running:
                    self.show_window()
                    return
                self.root.after(0, lambda x=i: self.status_label.config(text=f"{x}秒后开始..."))
                time.sleep(1)
            
            # 定义两个坐标点
            coordinates = [(329, 443), (443, 329)]
            
            for i, (x, y) in enumerate(coordinates, 1):
                if not self.running:
                    break
                    
                self.root.after(0, lambda x=i: self.status_label.config(text=f"点击第{x}个坐标"))
                
                # 瞬间移动到坐标并点击
                pyautogui.moveTo(x, y, duration=0)
                pyautogui.click()
                
                # 每次点击间隔1秒
                if i < len(coordinates):
                    time.sleep(1)
                
            self.root.after(0, lambda: messagebox.showinfo("完成", "坐标点击成功"))
                
        except Exception as e:
            error_msg = f"执行出错: {str(e)}"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
            self.root.after(0, lambda: self.status_label.config(text="完成"))
            # 任务完成后显示窗口
            self.show_window()
    
    def execute_function2(self):
        """执行功能2：图片点击"""
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
            
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text="5秒后开始...")
        
        # 隐藏窗口
        self.root.withdraw()
        
        thread = threading.Thread(target=self._function2_task)
        thread.daemon = True
        thread.start()
        
    def _convert_image_with_pil(self, image_path):
        """使用PIL读取图片并转换为OpenCV格式"""
        try:
            pil_image = Image.open(image_path)
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            numpy_image = np.array(pil_image)
            opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            return opencv_image
        except Exception as e:
            print(f"PIL转换失败: {e}")
            return None
    
    def _check_image_file(self, image_path):
        """检查图片文件是否可读"""
        if not os.path.exists(image_path):
            return False, "文件不存在"
        
        file_size = os.path.getsize(image_path)
        if file_size == 0:
            return False, "文件为空"
        
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return False, "不支持的图片格式"
        
        try:
            img = cv2.imread(image_path)
            if img is not None:
                return True, "OpenCV直接读取成功"
        except:
            pass
        
        pil_img = self._convert_image_with_pil(image_path)
        if pil_img is not None:
            return True, "使用PIL转换成功"
        
        return False, "所有读取方法都失败"
    
    def _find_image_opencv(self, template_path, timeout=5):
        """使用OpenCV查找图片"""
        start_time = time.time()
        
        is_ok, message = self._check_image_file(template_path)
        if not is_ok:
            raise Exception(f"图片文件检查失败: {message}")
        
        template = cv2.imread(template_path)
        if template is None:
            template = self._convert_image_with_pil(template_path)
            if template is None:
                raise Exception(f"无法读取图片: {template_path}")
        
        while time.time() - start_time < timeout:
            if not self.running:
                return None
                
            try:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                thresholds = [0.8, 0.7, 0.6, 0.5]
                for threshold in thresholds:
                    if max_val >= threshold:
                        h, w = template.shape[:2]
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        return (center_x, center_y, max_val)
                
            except Exception as e:
                print(f"图片识别过程中出错: {e}")
            
            time.sleep(0.3)
        
        return None
    
    def _function2_task(self):
        """功能2的后台任务"""
        try:
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0
            pyautogui.PAUSE = 0
            
            # 5秒预备时间
            for i in range(5, 0, -1):
                if not self.running:
                    self.show_window()
                    return
                self.root.after(0, lambda x=i: self.status_label.config(text=f"{x}秒后开始..."))
                time.sleep(1)
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image1_path = os.path.join(script_dir, "order_img_click", "all.png")
            image2_path = os.path.join(script_dir, "order_img_click", "orders.png")
            
            for image_name, image_path in [("all.png", image1_path), ("orders.png", image2_path)]:
                is_ok, message = self._check_image_file(image_path)
                if not is_ok:
                    self.root.after(0, lambda name=image_name, msg=message: 
                                  messagebox.showerror("错误", f"{name}文件问题:\n{msg}"))
                    self.running = False
                    self.root.after(0, self.update_buttons_state)
                    self.show_window()
                    return
            
            images_to_find = [
                ("all.png", image1_path),
                ("orders.png", image2_path)
            ]
            
            all_found = True
            
            for image_name, image_path in images_to_find:
                if not self.running:
                    break
                    
                self.root.after(0, lambda name=image_name: self.status_label.config(text=f"查找{name}"))
                
                result = self._find_image_opencv(image_path, timeout=5)
                
                if result:
                    center_x, center_y, confidence = result
                    pyautogui.moveTo(center_x, center_y, duration=0)
                    pyautogui.click()
                    
                    if image_name == "all.png":
                        time.sleep(1)
                else:
                    all_found = False
                    self.root.after(0, lambda name=image_name: messagebox.showerror("错误", 
                        f"未找到{name}"))
                    break
            
            if all_found:
                self.root.after(0, lambda: messagebox.showinfo("完成", "图片点击成功"))
                self.root.after(0, lambda: self.status_label.config(text="完成"))
            else:
                self.root.after(0, lambda: self.status_label.config(text="识别失败"))
                    
        except Exception as e:
            error_msg = f"执行出错: {str(e)}"
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", msg))
        
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
            # 任务完成后显示窗口
            self.show_window()
    
    def stop_execution(self):
        """停止执行"""
        self.running = False
        self.update_buttons_state()
        self.status_label.config(text="已停止")
        # 停止执行时也显示窗口
        self.show_window()
    
    def show_window(self):
        """显示窗口并置顶"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def update_buttons_state(self):
        """更新按钮状态"""
        if self.running:
            self.func1_button.config(state="disabled")
            self.func2_button.config(state="disabled")
            self.stop_button.config(state="normal")
        else:
            self.func1_button.config(state="normal")
            self.func2_button.config(state="normal")
            self.stop_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = FastErpApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()