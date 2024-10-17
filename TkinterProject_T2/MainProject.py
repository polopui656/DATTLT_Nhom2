
import tkinter as tk
from tkinter import ttk
import random
import time

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Title")
win.geometry("1024x768")

# Hàm cho nút Generate
def generate():
    global data
    chart_area.delete("all")  # Xóa nội dung cũ
    data = [random.randint(1, 100) for _ in range(10)]  # Tạo 10 số ngẫu nhiên
    draw_bars(data)

# hàm cho chức năng vẽ bar chart cho thuật toán
def draw_bars(data):
    chart_area.delete("all")
    max_value = max(data)
    bar_width = 50
    spacing = 10
    for i, value in enumerate(data):
        x0 = i * (bar_width + spacing)
        y0 = 600 - (value / max_value * 500)  # Tính chiều cao của cột
        x1 = x0 + bar_width
        y1 = 600
        chart_area.create_rectangle(x0, y0, x1, y1, fill="blue")
        chart_area.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), anchor=tk.S)

# Thuật toán Merge Sort
def merge_sort(data):
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        draw_bars(merged + left[i:] + right[j:])
        win.update_idletasks()
        time.sleep(speed_control.get() / 1000)

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

# Thuật toán Quick Sort
def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        draw_bars(data)
        win.update_idletasks()
        time.sleep(speed_control.get() / 300)  # Thêm độ trễ dựa trên giá trị của thanh trượt
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

# Thuật toán Selection Sort
def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if data[j] < data[min_index]:
                min_index = j
        # Hoán đổi vị trí
        data[i], data[min_index] = data[min_index], data[i]
        draw_bars(data)
        win.update_idletasks()
        time.sleep(speed_control.get() / 1000)

#Phân vùng cho Quick Sort
def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            #draw_bars(data)
            #win.update_idletasks()
            #time.sleep(speed_control.get() / 1000)  # Thêm độ trễ dựa trên giá trị của thanh trượt
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1


# Chức năng thực hiện sorting
def start_quick_sort():
    quick_sort(data, 0, len(data) - 1)
    draw_bars(data)

def start_select_sort():
    selection_sort(data)
    draw_bars(data)

def start_merge_sort():
    merge_sort(data)
    draw_bars(data)

# Thêm nút Generate
generate_button = ttk.Button(win, text="Generate", command=generate)
generate_button.pack()

# Vùng biểu đồ cột
chart_area = tk.Canvas(win, bg='white')
chart_area.pack(fill=tk.BOTH, expand=True)

# Thêm các nút thuật toán sắp xếp ở dưới cùng
merge_button = ttk.Button(win, text="Merge", command=start_merge_sort)
bubble_button = ttk.Button(win, text="Bubble")
quick_button = ttk.Button(win, text="Quick", command=start_quick_sort)
selection_button = ttk.Button(win, text="Selection", command=start_select_sort)

merge_button.pack(side=tk.LEFT)
bubble_button.pack(side=tk.LEFT)
quick_button.pack(side=tk.LEFT)
selection_button.pack(side=tk.LEFT)

# Điều khiển thanh trượt (slider)
slider_frame = tk.Frame(win)
slider_frame.pack()
slider_label = tk.Label(slider_frame, text='AR:')
slider_label.pack(side=tk.LEFT)
slider_control = ttk.Scale(slider_frame, from_=0, to=100)
slider_control.pack(side=tk.LEFT, padx=30)

speed_label = tk.Label(slider_frame, text='  Speed:')
speed_label.pack(side=tk.BOTTOM)
speed_control = ttk.Scale(slider_frame, from_=0, to=100)
speed_control.pack(side=tk.LEFT)

# Bắt đầu giao diện
win.mainloop()
