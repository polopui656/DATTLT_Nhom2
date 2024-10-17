import tkinter as tk
from tkinter import ttk
import random
import time

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Title")
width= win.winfo_screenwidth() 
height= win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))

data = []

# Hàm xử lý hiển thị các ô nhập liệu tùy thuộc vào lựa chọn từ dropdown
def on_selection_change(event):
    selected_option = dropdown.get()
    if selected_option == "Random":
        random_frame.pack(side=tk.LEFT, padx=20)
        manual_frame.pack_forget()
    elif selected_option == "Manual":
        manual_frame.pack(side=tk.LEFT, padx=20)
        random_frame.pack_forget()

# Hàm cho nút Generate ngẫu nhiên
def generate_random():
    global data
    chart_area.delete("all")
    try:
        min_val = int(min_entry.get())
        max_val = int(max_entry.get())
        count = int(count_entry.get())
        data = [random.randint(min_val, max_val) for _ in range(count)]  # Tạo số ngẫu nhiên
        draw_bars(data)
    except ValueError:
        pass

# Hàm cho nhập thủ công
def manual_input():
    global data
    chart_area.delete("all")
    try:
        data = list(map(int, manual_entry.get().split(',')))  # Nhập các số và tách bằng dấu phẩy
        draw_bars(data)
    except ValueError:
        pass

# Hàm cho chức năng vẽ bar chart
def draw_bars(data, color_array=None):
    chart_area.delete("all")
    max_value = max(data)
    bar_width = 50
    spacing = 10
    if color_array is None:
        color_array = ['blue' for _ in range(len(data))]
    for i, value in enumerate(data):
        x0 = i * (bar_width + spacing)
        y0 = 600 - (value / max_value * 500)
        x1 = x0 + bar_width
        y1 = 600
        chart_area.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        chart_area.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), anchor=tk.S)
    win.update_idletasks()


# Thuật toán Merge Sort
def merge(leftData, rightData):
    result = []
    i,j = 0,0
    while i < len(leftData) and j < len(rightData):
        if leftData[i] < rightData[j]:
            result.append(leftData[i])
            draw_bars(leftData, ['green' if x == i else 'blue' for x in range(len(leftData))])
            i += 1
        else:
            result.append(rightData[j])
            draw_bars(rightData, ['green' if x == j else 'blue' for x in range(len(rightData))])
            j += 1
        combind = result + leftData[i:] + rightData[j:]
        draw_bars(combind, ['green' if x == len(result) - 1 else 'blue' for x in range(len(combind))])
        time.sleep(speed_control.get() / 1000)

    result += leftData[i:]
    result += rightData[j:]
    draw_bars(result, ['blue' for _ in range(len(result))])

    return result

def merge_sort(data):
    if len(data) <= 1:
        return data
    midpoint = len(data) // 2
    leftData = merge_sort(data[:midpoint])
    rightData = merge_sort(data[midpoint:])
    return merge(leftData, rightData)

# Thuật toán Quick Sort
def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        draw_bars(data, ['green' if x == pi else 'blue' for x in range(len(data))])
        time.sleep(speed_control.get() / 300)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

# Phân vùng cho Quick Sort
def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

# Thuật toán Selection Sort
def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        draw_bars(data,['green'if x == i else 'blue' for x in range(len(data))])
        time.sleep(speed_control.get() / 300)



# Chức năng thực hiện sorting
def start_quick_sort():
    quick_sort(data, 0, len(data) - 1)
    draw_bars(data)

def start_select_sort():
    selection_sort(data)
    draw_bars(data)

def start_merge_sort():
    merge_sort(data)

# Giao diện cho phần nhập
input_frame = tk.Frame(win)
input_frame.pack()

# Dropdown menu cho lựa chọn giữa ngẫu nhiên và nhập thủ công
dropdown_label = tk.Label(input_frame, text="Choose input type:")
dropdown_label.pack(side=tk.LEFT, padx=10)

options = ["Random", "Manual"]
dropdown = ttk.Combobox(input_frame, values=options)
dropdown.set("Random")  # Giá trị mặc định
dropdown.bind("<<ComboboxSelected>>", on_selection_change)
dropdown.pack(side=tk.LEFT)

# Giao diện cho Randoms
random_frame = tk.Frame(input_frame)
min_label = tk.Label(random_frame, text="Min:")
min_label.pack(side=tk.LEFT)
min_entry = tk.Entry(random_frame, width=5)
min_entry.pack(side=tk.LEFT)

max_label = tk.Label(random_frame, text="Max:")
max_label.pack(side=tk.LEFT)
max_entry = tk.Entry(random_frame, width=5)
max_entry.pack(side=tk.LEFT)

count_label = tk.Label(random_frame, text="Count:")
count_label.pack(side=tk.LEFT)
count_entry = tk.Entry(random_frame, width=5)
count_entry.pack(side=tk.LEFT)

generate_random_button = ttk.Button(random_frame, text="Generate Random", command=generate_random)
generate_random_button.pack(side=tk.LEFT, padx=10)

# Giao diện cho Manual
manual_frame = tk.Frame(input_frame)
manual_label = tk.Label(manual_frame, text="Manual Input (vd: 3, 5, 4,...):")
manual_label.pack(side=tk.LEFT)
manual_entry = tk.Entry(manual_frame, width=30)
manual_entry.pack(side=tk.LEFT)

manual_button = ttk.Button(manual_frame, text="Input Numbers", command=manual_input)
manual_button.pack(side=tk.LEFT, padx=10)

# Hiển thị giao diện Random ban đầu
random_frame.pack(side=tk.LEFT, padx = 10)

# Các nút thuật toán sắp xếp
slider_frame = tk.Frame(win)
slider_frame.pack()
merge_button = ttk.Button(slider_frame, text="Merge", command=start_merge_sort)
merge_button.pack(side=tk.LEFT,padx=20)
quick_button = ttk.Button(slider_frame, text="Quick", command=start_quick_sort)
quick_button.pack(side=tk.LEFT,padx=20)
selection_button = ttk.Button(slider_frame, text="Selection", command=start_select_sort)
selection_button.pack(side=tk.LEFT,padx=20 )

# Điều khiển thanh trượt (slider)

slider_label = tk.Label(slider_frame, text='  Speed:')
slider_label.pack(side=tk.LEFT)
speed_control = ttk.Scale(slider_frame, from_=0, to=1000)
speed_control.pack(side=tk.LEFT)

# Vùng biểu đồ cột
chart_area = tk.Canvas(win, bg='white')
chart_area.pack(fill=tk.BOTH, expand=True)
# Bắt đầu giao diện
win.mainloop()
