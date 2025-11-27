# build_fixed_icon.py
import os
import shutil
import subprocess
import sys

def build_with_fixed_icon():
    print("=" * 60)
    print("FastErp 打包 - 使用固定图标: logo_icon/logo.ico")
    print("=" * 60)
    
    # 清理之前的构建文件（更彻底）
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✅ 清理文件夹: {folder}")
    
    icon_path = "logo_icon/logo.ico"
    print(f"🖼️  使用的图标: {icon_path}")
    print(f"📁 图标文件存在: {os.path.exists(icon_path)}")

    if not os.path.exists(icon_path):
        print("❌ 错误: 图标文件不存在!")
        print("请确认 logo_icon/logo.ico 文件存在")
        return False

    icon_size = os.path.getsize(icon_path)
    print(f"📏 图标文件大小: {icon_size} 字节")
    if icon_size < 1024:
        print("⚠️  警告: 图标文件可能太小（标准 ICO 通常 >1KB）")

    # 强制使用正斜杠（避免 Windows 反斜杠问题）
    icon_path_forward = icon_path.replace("\\", "/")

    # 构建命令：使用 forward slash + 显式转义（安全）
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=FastErp",
        f"--icon={icon_path_forward}",
        "--add-data", f"logo_icon{os.pathsep}logo_icon",
        "--add-data", f"order_img_click{os.pathsep}order_img_click",
        "--clean",
        "--noconfirm",
        "--noupx",
        "click.py"
    ]

    print("\n🚀 开始打包（使用正斜杠路径）...")
    print("执行命令:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ 打包成功!")
        check_result()
        return True
    else:
        print("❌ 打包失败!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False

def check_result():
    exe_path = os.path.join("dist", "FastErp.exe")
    if os.path.exists(exe_path):
        exe_size = os.path.getsize(exe_path)
        print(f"\n🎉 打包完成!")
        print(f"📁 EXE路径: {exe_path}")
        print(f"📏 文件大小: {exe_size:,} 字节")
        print("🖼️  请右键 → 属性 → 详细信息，检查图标是否生效")
        verify_resources()
    else:
        print("❌ EXE 文件未生成！")

def verify_resources():
    print("\n🔍 验证资源文件是否就位...")
    for folder in ["logo_icon", "order_img_click"]:
        if os.path.isdir(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            print(f"✅ {folder}: {len(files)} 个文件")
        else:
            print(f"❌ {folder} 不存在")

def verify_icon_file():
    print("\n🔍 深度验证图标文件...")
    icon_path = "logo_icon/logo.ico"
    if not os.path.exists(icon_path):
        print("❌ 图标文件缺失")
        return

    # 尝试用 Pillow 验证（如果安装）
    try:
        from PIL import Image
        with Image.open(icon_path) as img:
            print(f"✅ 格式: {img.format}")
            print(f"✅ 尺寸: {img.size}")
            print(f"✅ 模式: {img.mode}")
            # 检查是否为多尺寸 ICO（理想情况）
            if hasattr(img, 'n_frames') and img.n_frames > 1:
                print(f"✅ 多帧图标（含 {img.n_frames} 个尺寸）")
            else:
                print("⚠️  单尺寸图标（建议使用多尺寸 ICO）")
    except ImportError:
        print("ℹ️  Pillow 未安装，跳过图像验证（建议: pip install Pillow）")
    except Exception as e:
        print(f"❌ 图标解析失败: {e}")

    # 检查扩展名
    if not icon_path.lower().endswith('.ico'):
        print("⚠️  文件扩展名不是 .ico")

if __name__ == "__main__":
    verify_icon_file()
    print("\n" + "=" * 60)
    success = build_with_fixed_icon()
    print("\n" + "=" * 60)
    if success:
        print("✅ 打包完成！请检查 dist/FastErp.exe 的图标显示。")
        print("💡 提示：Windows 资源管理器可能缓存图标，可重启 explorer 或换文件名测试。")
    else:
        print("💥 打包失败！请按以下步骤排查：")
        print("1. 确保 logo_icon/logo.ico 是标准 Windows ICO（推荐使用 https://convertio.co/png-ico/ 转换）")
        print("2. 图标应包含至少 32x32 和 256x256 尺寸")
        print("3. 升级 PyInstaller: pip install --upgrade pyinstaller")
        print("4. 尝试手动运行命令查看详细错误")


