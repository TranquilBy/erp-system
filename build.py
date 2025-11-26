import PyInstaller.__main__
import os
import shutil

def build_exe():
    # 清理之前的构建文件
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # PyInstaller配置
    PyInstaller.__main__.run([
        'click.py',  # 替换为你的Python文件名
        '--onefile',           # 打包成单个exe
        '--windowed',          # 不显示控制台窗口
        '--name=FastErp',      # 生成的exe名称
        '--add-data=logo_icon;logo_icon',  # 包含资源文件夹
        '--add-data=order_img_click;order_img_click',
        '--clean',             # 清理临时文件
        '--noconfirm',         # 覆盖已有的spec文件
    ])

if __name__ == "__main__":
    build_exe()