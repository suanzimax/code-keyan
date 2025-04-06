import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# 弹出文件选择对话框，让用户选择图片文件
root = tk.Tk()
root.withdraw()  # 隐藏主窗口
file_path = filedialog.askopenfilename(title="选择图片文件", 
                                       filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
if not file_path:
    print("未选择文件，程序退出")
    exit()

# 读取选择的图片
img = cv2.imread(file_path)
if img is None:
    print("无法加载图片，请检查文件格式")
    exit()

# 使用 OpenCV 提供的交互窗口让你用鼠标选择区域
roi = cv2.selectROI("Select ROI", img, showCrosshair=True, fromCenter=False)
cv2.destroyAllWindows()

# 提取选中的区域
x, y, w, h = roi
cropped_img = img[y:y+h, x:x+w]

# 将截图调整为指定尺寸，例如 200x200 像素
fixed_size = cv2.resize(cropped_img, (200, 200))

# 保存处理后的图片到当前目录下
cv2.imwrite("output.png", fixed_size)
print("图片已保存为 output.png")
