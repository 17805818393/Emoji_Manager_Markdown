import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys

folder_path = ""

def on_closing():
    # 显示一个提示框，询问用户是否要退出程序
    if tk.messagebox.askokcancel("退出", "确定要退出程序吗？"):
        # 关闭整个程序
        sys.exit()

def copy_to_clipboard(filename):
    # 将字符串复制到剪贴板
    # pyperclip.copy(f"![]({folder_path}/{filename})")
    # print(f"已复制：![]({folder_path}/{filename})")
    text = f"![]({folder_path}/{filename})"
    command = f'echo "{text}" | xclip -selection clipboard'
    os.system(command)
    print(text)

def open_folder():
    # 打开文件夹并读取其中的图片文件
    global folder_path
    window = tk.Tk()
    window.withdraw()
    pwd = os.getcwd()
    folder_path = filedialog.askdirectory(title="选择图片文件夹")
    try:
        folder_path = folder_path.replace(pwd + "/","")
    except:
        print(pwd,folder_path)
    if folder_path:
        image_files = [f for f in os.listdir(folder_path) if f.endswith((".png", ".jpg", ".jpeg", ".gif" , ".PNG"))]
        display_images(folder_path, image_files)
    else:
        sys.exit()

def display_images(folder_path, image_files):
    # 创建一个可视化窗口并显示图片
    root = tk.Toplevel()
    root.title("表情浏览器")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

    icon_image = tk.PhotoImage(file="icon.png")
    root.iconphoto(True, icon_image)

    for filename in image_files:
        img = Image.open(os.path.join(folder_path, filename))
        img.thumbnail((100, 100))  # 缩小图片尺寸以适应窗口
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(main_frame, image=photo)
        label.grid(row=image_files.index(filename) // 8, column=image_files.index(filename) % 8)
        
        # 点击图片时将字符串复制到剪贴板
        label.bind("<Button-1>", lambda event, fn=filename: copy_to_clipboard(fn))

        # 保持对PhotoImage对象的引用，防止被垃圾回收
        label.photo = photo
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    open_folder()
