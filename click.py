import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import os
import cv2
import numpy as np
import sys
from PIL import Image, ImageTk

class FastErpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastErp")
        self.root.geometry("300x280")
        self.root.resizable(False, False)
        
        # 设置窗口置顶
        self.root.attributes('-topmost', True)
        
        # 设置现代主题
        self.set_modern_theme()
        
        # 加载logo
        self.load_logo()
        
        # 创建样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 运行状态
        self.running = False
        
        # 显示启动提示
        self.root.after(100, self.show_startup_message)
        
    def set_modern_theme(self):
        """设置现代主题"""
        self.root.configure(bg='#f8f9fa')
        
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
                self.logo_icon = None
                
        except Exception as e:
            print(f"加载logo时出错: {e}")
            self.logo_icon = None
    
    def show_startup_message(self):
        """显示启动提示"""
        messagebox.showinfo("FastErp", "快速点击工具已启动")
    
    def setup_styles(self):
        # 创建样式对象
        style = ttk.Style()
        
        # 配置现代主题
        style.theme_use('clam')
        
        # 配置标题标签样式
        style.configure("Title.TLabel", 
                        font=('Segoe UI', 18, 'bold'),
                        foreground="#2c3e50",
                        background='#f8f9fa')
        
        # 配置副标题样式
        style.configure("Subtitle.TLabel",
                        font=('Segoe UI', 10),
                        foreground="#7f8c8d",
                        background='#f8f9fa')
        
        # 配置主功能按钮样式
        style.configure("Primary.TButton", 
                        padding=(20, 12),
                        font=('Segoe UI', 11, 'bold'),
                        background="#3498db",
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none")
        
        style.map("Primary.TButton",
                 background=[('active', '#2980b9'), ('pressed', '#2471a3')])
        
        # 配置次要功能按钮样式
        style.configure("Secondary.TButton", 
                        padding=(20, 12),
                        font=('Segoe UI', 11, 'bold'),
                        background="#2ecc71",
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none")
        
        style.map("Secondary.TButton",
                 background=[('active', '#27ae60'), ('pressed', '#229954')])
        
        # 配置停止按钮样式
        style.configure("Danger.TButton", 
                        padding=(15, 8),
                        font=('Segoe UI', 9, 'bold'),
                        background="#e74c3c",
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none")
        
        style.map("Danger.TButton",
                 background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        # 配置状态标签样式
        style.configure("Status.TLabel", 
                        font=('Segoe UI', 9),
                        foreground="#95a5a6",
                        background='#f8f9fa')
        
        # 配置框架样式
        style.configure("Card.TFrame",
                        background="white",
                        relief="solid",
                        borderwidth=1)
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20", style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame, style="Card.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 标题
        title_label = ttk.Label(title_frame, text="FastErp", style="Title.TLabel")
        title_label.pack()
        
        # 副标题
        subtitle_label = ttk.Label(title_frame, text="自动化点击工具", style="Subtitle.TLabel")
        subtitle_label.pack()
        
        # 功能按钮区域
        func_frame = ttk.Frame(main_frame, style="Card.TFrame")
        func_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # 配置grid权重，让两个按钮等宽
        func_frame.columnconfigure(0, weight=1)
        func_frame.columnconfigure(1, weight=1)
        func_frame.rowconfigure(0, weight=1)
        
        # 坐标点击按钮
        self.func1_button = ttk.Button(func_frame, text="坐标点击", 
                                      command=self.execute_function1,
                                      style="Primary.TButton")
        self.func1_button.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        
        # 图片点击按钮
        self.func2_button = ttk.Button(func_frame, text="图片点击", 
                                      command=self.execute_function2,
                                      style="Secondary.TButton")
        self.func2_button.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        
        # 底部控制区域
        bottom_frame = ttk.Frame(main_frame, style="Card.TFrame")
        bottom_frame.pack(fill=tk.X, pady=(15, 0))
        
        # 左下角 - 停止按钮
        self.stop_button = ttk.Button(bottom_frame, text="停止执行", 
                                     command=self.stop_execution,
                                     style="Danger.TButton",
                                     state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 状态区域
        status_frame = ttk.Frame(bottom_frame, style="Card.TFrame")
        status_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # 状态标签
        status_title = ttk.Label(status_frame, text="状态:", style="Status.TLabel")
        status_title.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(status_frame, text="就绪", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
    def execute_function1(self):
        """执行功能1：坐标点击"""
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
            
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text="5秒后开始...")
        
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
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
            self.root.after(0, lambda: self.status_label.config(text="完成"))
    
    def execute_function2(self):
        """执行功能2：图片点击"""
        if self.running:
            messagebox.showwarning("警告", "已有任务正在执行")
            return
            
        self.running = True
        self.update_buttons_state()
        self.status_label.config(text="5秒后开始...")
        
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
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        
        finally:
            self.running = False
            self.root.after(0, self.update_buttons_state)
    
    def stop_execution(self):
        """停止执行"""
        self.running = False
        self.update_buttons_state()
        self.status_label.config(text="已停止")
    
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