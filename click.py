import tkinter as tk
from tkinter import messagebox, font
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FastErpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastErp")
        self.root.geometry("260x120")  # 增加高度以容纳功能区域
        self.root.resizable(False, False)
        
        # 主题颜色
        self.bg_color = "#f5f7fa"
        self.card_color = "#ffffff"
        self.button_primary = "#0078d4"
        self.button_success = "#107c10"
        self.button_danger = "#c50f1f"
        self.text_primary = "#323130"
        self.text_secondary = "#605e5c"

        self.root.configure(bg=self.bg_color)
        self.root.attributes('-topmost', True)

        # GitHub 信息
        self.github_repo = "TranquilBy/erp-system"
        self.current_version = "v1.2.0"
        self.github_url = "https://github.com/TranquilBy/erp-system"

        # 字体配置
        self.default_font = font.Font(family="Microsoft YaHei", size=9)
        self.bold_font = font.Font(family="Microsoft YaHei", size=10, weight="bold")

        # 加载 logo（保持原有的logo功能）
        self.load_logo()

        # 创建界面
        self.create_widgets()

        self.running = False
        self.root.after(100, self.show_startup_message)

    def load_logo(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            logo_paths = [
                os.path.join(base_path, "logo_icon", "logo.jpg"),
                os.path.join(base_path, "logo_icon", "logo.png"),
                os.path.join(base_path, "logo_icon", "logo.ico"),
                os.path.join(os.path.dirname(sys.executable), "logo_icon", "logo.jpg"),
            ]
            
            logo_path = None
            for path in logo_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path and os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((16, 16), Image.Resampling.LANCZOS)
                self.logo_icon = ImageTk.PhotoImage(logo_image)
                self.root.iconphoto(True, self.logo_icon)  # 重新添加logo
        except Exception as e:
            print(f"加载 logo 时出错: {e}")

    def show_startup_message(self):
        messagebox.showinfo("FastErp", "快速点击工具已启动")

    def create_widgets(self):
        # ========== 顶部栏：设置 + 功能按钮 ==========
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, padx=10, pady=(5, 5))

        # 设置按钮
        self.settings_button = tk.Button(
            top_frame,
            text="✦设置",
            command=self.show_settings_menu,
            font=self.bold_font,
            bg=self.card_color,
            fg=self.text_primary,
            relief='flat',
            bd=1,
            padx=10,
            pady=4,
            cursor='hand2'
        )
        self.settings_button.pack(side=tk.LEFT, padx=(0, 5))

        # 坐标点击按钮
        self.coord_button = tk.Button(
            top_frame,
            text="☭坐标",
            command=self.show_coord_menu,
            font=self.default_font,
            bg=self.card_color,
            fg=self.text_primary,
            relief='flat',
            bd=1,
            padx=10,
            pady=4,
            cursor='hand2'
        )
        self.coord_button.pack(side=tk.LEFT, padx=(5, 5))

        # 图片点击按钮
        self.img_button = tk.Button(
            top_frame,
            text="☁图片",
            command=self.show_img_menu,
            font=self.default_font,
            bg=self.card_color,
            fg=self.text_primary,
            relief='flat',
            bd=1,
            padx=10,
            pady=4,
            cursor='hand2'
        )
        self.img_button.pack(side=tk.LEFT, padx=(5, 0))

        # ========== 功能区域 ==========
        self.function_frame = tk.Frame(self.root, bg=self.bg_color)
        self.function_frame.pack(fill=tk.X, padx=10, pady=(5, 5))

        # 初始化功能区域为空
        self.clear_function_area()

        # ========== 状态区域 ==========
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=self.bold_font,
            fg=self.text_primary,
            bg=self.bg_color
        )
        self.status_label.pack()

        # ========== 创建菜单（保持原有的菜单功能） ==========
        self.settings_menu = tk.Menu(self.root, tearoff=0)
        self.settings_menu.add_command(
            label="关于版本",
            command=self.show_about_version,
            font=self.default_font
        )
        self.settings_menu.add_command(
            label="检查更新",
            command=self.check_update,
            font=self.default_font
        )

        # ========== 创建坐标菜单 ==========
        self.coord_menu = tk.Menu(self.root, tearoff=0)
        coord_tasks = [
            ("📋 订单处理", "订单处理"),
            ("📦 发货单处理", "发货单处理"),
            ("💰 收款单处理", "收款单处理"),
            ("📊 报表生成", "报表生成")
        ]
        for label, task_name in coord_tasks:
            self.coord_menu.add_command(
                label=label,
                command=lambda n=task_name: self.execute_function1(n),
                font=self.default_font
            )

        # ========== 创建图片菜单 ==========
        self.img_menu = tk.Menu(self.root, tearoff=0)
        img_tasks = [
            ("🔍 搜索按钮", "搜索按钮"),
            ("✅ 确认按钮", "确认按钮"),
            ("🔄 刷新按钮", "刷新按钮"),
            ("❌ 关闭按钮", "关闭按钮")
        ]
        for label, task_name in img_tasks:
            self.img_menu.add_command(
                label=label,
                command=lambda n=task_name: self.execute_function2(n),
                font=self.default_font
            )

    def clear_function_area(self):
        for widget in self.function_frame.winfo_children():
            widget.destroy()
        
        # 显示提示信息
        hint_label = tk.Label(
            self.function_frame,
            text="点击上方按钮选择功能",
            font=self.default_font,
            fg=self.text_secondary,
            bg=self.bg_color
        )
        hint_label.pack(expand=True)

    def show_settings_menu(self):
        x = self.settings_button.winfo_rootx()
        y = self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        self.settings_menu.post(x, y)

    def show_coord_menu(self):
        x = self.coord_button.winfo_rootx()
        y = self.coord_button.winfo_rooty() + self.coord_button.winfo_height()
        self.coord_menu.post(x, y)

    def show_img_menu(self):
        x = self.img_button.winfo_rootx()
        y = self.img_button.winfo_rooty() + self.img_button.winfo_height()
        self.img_menu.post(x, y)

    def show_about_version(self):
        messagebox.showinfo("关于版本", f"当前版本：{self.current_version}\n\nFastErp 自动化点击工具")

    def check_update(self):
        thread = threading.Thread(target=self._check_update_task)
        thread.daemon = True
        thread.start()

    def _check_update_task(self):
        try:
            self.root.after(0, lambda: self.status_label.config(text="检查更新中..."))
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(api_url, timeout=10, verify=False)
            if response.status_code != 200:
                self.root.after(0, lambda: messagebox.showerror("错误", f"GitHub API返回错误: {response.status_code}"))
                return

            release_info = response.json()
            latest_tag = release_info.get("tag_name", "")
            latest_version = latest_tag.lstrip("v")

            if version.parse(latest_version) > version.parse(self.current_version.lstrip("v")):
                download_url = None
                for asset in release_info.get("assets", []):
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
                if download_url:
                    self.root.after(0, lambda lv=latest_version, url=download_url: 
                                  self.show_update_dialog(lv, url))
                else:
                    self.root.after(0, lambda lv=latest_version: messagebox.showinfo("更新", f"发现新版本 v{lv}，但未找到.exe文件"))
            else:
                self.root.after(0, lambda cv=self.current_version: messagebox.showinfo("更新", f"当前已是最新版本 {cv}"))
        except Exception as e:
            self.root.after(0, lambda msg=str(e): messagebox.showerror("错误", msg))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    def show_update_dialog(self, latest_version, download_url):
        result = messagebox.askyesno("发现新版本", f"发现新版本 v{latest_version}\n\n是否立即更新？")
        if result:
            self.download_and_update(download_url, latest_version)

    def download_and_update(self, download_url, latest_version):
        try:
            self.root.after(0, lambda: self.status_label.config(text="下载更新中..."))
            response = requests.get(download_url, stream=True, timeout=30, verify=False)
            response.raise_for_status()

            current_executable = sys.executable
            current_dir = os.path.dirname(current_executable)
            new_executable_path = os.path.join(current_dir, f"FastErp_v{latest_version}.exe")

            with open(new_executable_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            update_script = os.path.join(current_dir, "update.bat")
            with open(update_script, 'w', encoding='utf-8') as f:
                f.write(f'''@echo off
timeout /t 1 /nobreak >nul
del "{current_executable}"
move "{new_executable_path}" "{current_executable}"
start "" "{current_executable}"
del "%~f0"
''')

            subprocess.Popen(update_script, shell=True)
            self.root.quit()
        except Exception as e:
            self.root.after(0, lambda msg=str(e): messagebox.showerror("错误", msg))
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    # ========== 原有的功能1：坐标点击（保持原有逻辑） ==========
    def execute_function1(self, task_name):
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text=f"执行中：{task_name}")
        self.root.withdraw()
        
        # 根据任务执行不同的坐标点击
        coord_map = {
            "订单处理": [(329, 443), (443, 329)],
            "发货单处理": [(500, 300), (600, 400)],
            "收款单处理": [(700, 200)],
            "报表生成": [(800, 500), (900, 600)]
        }
        coordinates = coord_map.get(task_name, [(329, 443)])
        
        thread = threading.Thread(target=self._function1_task, args=(coordinates,))
        thread.daemon = True
        thread.start()

    def _function1_task(self, coordinates):
        try:
            pyautogui.MINIMUM_DURATION = 0
            pyautogui.MINIMUM_SLEEP = 0
            pyautogui.PAUSE = 0
            for i in range(5, 0, -1):
                if not self.running: return
                self.root.after(0, lambda x=i: self.status_label.config(text=f"{x}秒后开始..."))
                time.sleep(1)
            
            for i, (x, y) in enumerate(coordinates, 1):
                if not self.running: break
                self.root.after(0, lambda x=i: self.status_label.config(text=f"点击第{x}个坐标"))
                pyautogui.moveTo(x, y, duration=0)
                pyautogui.click()
                if i < len(coordinates): time.sleep(1)
            self.root.after(0, lambda: messagebox.showinfo("完成", "坐标点击成功"))
        except Exception as e:
            self.root.after(0, lambda msg=str(e): messagebox.showerror("错误", f"执行出错: {msg}"))
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
            self.root.after(0, lambda: self.status_label.config(text="就绪"))
            self.show_window()

    # ========== 原有的功能2：图片点击（保持原有逻辑） ==========
    def execute_function2(self, task_name):
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text=f"执行中：{task_name}")
        self.root.withdraw()
        
        # 根据任务查找不同图片
        img_map = {
            "搜索按钮": "search.png",
            "确认按钮": "confirm.png",
            "刷新按钮": "refresh.png",
            "关闭按钮": "close.png"
        }
        img_name = img_map.get(task_name, "btn1.png")
        
        thread = threading.Thread(target=self._function2_task, args=(img_name,))
        thread.daemon = True
        thread.start()

    def _function2_task(self, img_name):
        try:
            for i in range(5, 0, -1):
                if not self.running: return
                self.root.after(0, lambda x=i: self.status_label.config(text=f"{x}秒后开始..."))
                time.sleep(1)
            
            image_paths = [img_name]  # 只查找指定的图片
            for idx, img_name in enumerate(image_paths, 1):
                if not self.running: break
                self.root.after(0, lambda x=idx: self.status_label.config(text=f"查找第{x}张图"))
                found = self._find_and_click_image(img_name, confidence=0.8)
                if not found:
                    self.root.after(0, lambda n=img_name: messagebox.showwarning("警告", f"未找到图片: {n}"))
                    break
                time.sleep(1)
            self.root.after(0, lambda: messagebox.showinfo("完成", "图片点击流程结束"))
        except Exception as e:
            self.root.after(0, lambda msg=str(e): messagebox.showerror("错误", f"执行出错: {msg}"))
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
            self.root.after(0, lambda: self.status_label.config(text="就绪"))
            self.show_window()

    def _find_and_click_image(self, image_name, confidence=0.8):
        try:
            # 确定资源路径
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_path, image_name)
            
            if not os.path.exists(image_path):
                print(f"图片不存在: {image_path}")
                return False

            # 截图屏幕
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 读取模板
            template = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"无法加载模板: {image_path}")
                return False

            # 模板匹配
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= confidence:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.click(center_x, center_y)
                return True
            else:
                return False
        except Exception as e:
            print(f"图像识别出错: {e}")
            return False

    def stop_execution(self):
        self.running = False
        self.update_buttons_state()
        self.status_label.config(text="已停止")
        self.show_window()

    def show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def update_buttons_state(self):
        if self.running:
            self.coord_button.config(state="disabled")
            self.img_button.config(state="disabled")
            self.settings_button.config(state="disabled")
        else:
            self.coord_button.config(state="normal")
            self.img_button.config(state="normal")
            self.settings_button.config(state="normal")

# ========== 启动入口 ==========
def main():
    root = tk.Tk()
    app = FastErpApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()