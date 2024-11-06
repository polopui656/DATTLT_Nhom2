import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Sorting Algorithm")
width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))

data = []
sort_thread = None
is_paused = False
is_stopped = False

# Hàm cho nút Generate ngẫu nhiên, điền vào Manual Input
def generate_random():
    global data
    try:
        min_val = int(min_entry.get())
        max_val = int(max_entry.get())
        count = int(count_entry.get())
        data = [random.randint(min_val, max_val) for _ in range(count)]
        manual_entry.delete(0, tk.END)
        manual_entry.insert(0, ", ".join(map(str, data)))
    except ValueError:
        pass

# Hàm cho nhập thủ công và hiển thị các số
def manual_input():
    global data
    chart_area.delete("all")
    try:
        data = list(map(int, manual_entry.get().split(",")))
        draw_bars(data)
    except ValueError:
        pass

# Hàm tạm dừng và tiếp tục sorting
def toggle_pause_resume():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text="Resume" if is_paused else "Pause")

# Hàm dừng sorting
def stop_sorting():
    global is_stopped
    is_stopped = True

# Hàm cho chức năng vẽ bar chart
def draw_bars(data, color_array=None):
    chart_area.delete("all")
    max_value = max(data)
    bar_width = 50
    spacing = 10
    bar_positions = []

    if color_array is None:
        color_array = ["blue" for _ in range(len(data))]
    for i, value in enumerate(data):
        x0 = i * (bar_width + spacing)
        y0 = 600 - (value / max_value * 500)
        x1 = x0 + bar_width
        y1 = 600
        color = color_array[i]

        bar = chart_area.create_rectangle(x0, y0, x1, y1, fill=color)
        chart_area.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), anchor=tk.S)
        bar_positions.append((bar, x0, y0, x1, y1))
    win.update_idletasks()
    return bar_positions

# Hàm hoán đổi vị trí của hai thanh với animation mượt mà
def animate_swap(bar_positions, i, j, duration=0.01):
    chart_area.itemconfig(bar_positions[i][0], fill="green")
    chart_area.itemconfig(bar_positions[j][0], fill="green")
    win.update_idletasks()

    x0_i, x1_i = bar_positions[i][1], bar_positions[i][3]
    x0_j, x1_j = bar_positions[j][1], bar_positions[j][3]

    steps = 400
    delta_x_i = (x0_j - x0_i) / steps
    delta_x_j = (x0_i - x0_j) / steps

    for step in range(steps):
        chart_area.move(bar_positions[i][0], delta_x_i, 0)
        chart_area.move(bar_positions[j][0], delta_x_j, 0)
        win.update_idletasks()
        time.sleep(duration / steps)

    bar_positions[i], bar_positions[j] = bar_positions[j], bar_positions[i]
    win.update_idletasks()

# Thuật toán Merge Sort
def merge_sort(data, left, right):
    if left < right:
        m = (left + right) // 2
        merge_sort(data, left, m)
        merge_sort(data, m + 1, right)
        merge(data, left, m, right)        
        draw_bars(data)
        time.sleep(speed_control.get() / 100)
        win.update_idletasks()

def merge(data, left, m, right):
    global is_paused, is_stopped
    bar_positions = draw_bars(data)
    i =left
    j = m + 1
    temp = []

    while is_paused:
        time.sleep(0.1)
    if is_stopped:
        return

    while i <= m and j <= right:
        
        animate_swap(bar_positions, left, j)
        bar_positions = draw_bars(data)
        time.sleep(speed_control.get() / 300)
        win.update_idletasks()

        if data[i] <= data[j]:
            temp.append(data[i])
            i += 1
        else:
            temp.append(data[j])
            j += 1

    while i <= m:
        temp.append(data[i])
        i += 1
        
    while j <= right:
        temp.append(data[j])
        j += 1
        

    for k in range(len(temp)):
        data[left + k] = temp[k]
        bar_positions = draw_bars(data)
        time.sleep(speed_control.get() / 300)
        win.update_idletasks()

# Thuật toán Quick Sort
def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

def partition(data, low, high):
    global is_paused, is_stopped
    bar_positions = draw_bars(data)
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        while is_paused:
            time.sleep(0.1)
        if is_stopped:
            break
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            animate_swap(bar_positions, i, j)
            bar_positions = draw_bars(data)
            time.sleep(speed_control.get() / 300)
            
    data[i + 1], data[high] = data[high], data[i + 1]
    animate_swap(bar_positions, i+1, high)
    bar_positions = draw_bars(data)
    time.sleep(speed_control.get() / 300)
    win.update_idletasks()
    return i + 1

# Thuật toán Selection Sort
def selection_sort(data):
    global is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            while is_paused:
                time.sleep(0.1)
            if is_stopped:
                break
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        animate_swap(bar_positions, i, min_index)
        bar_positions = draw_bars(data)
        time.sleep(speed_control.get() / 300)
        win.update_idletasks()

# Thuật toán Bubble Sort
def bubble_sort(data):
    global is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            while is_paused:
                time.sleep(0.1)
            if is_stopped:
                break
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                animate_swap(bar_positions, j, j + 1)
                bar_positions = draw_bars(data)
                time.sleep(speed_control.get() / 300)

# Chức năng thực hiện sorting theo lựa chọn từ dropdown
def start_sorting():
    global sort_thread, is_paused, is_stopped
    is_paused = False
    is_stopped = False
    selected_algo = algo_dropdown.get()
    
    sort_algorithms = {
        "Merge Sort": lambda: merge_sort(data, 0, len(data) - 1),
        "Quick Sort": lambda: quick_sort(data, 0, len(data) - 1),
        "Selection Sort": lambda: selection_sort(data),
        "Bubble Sort": lambda: bubble_sort(data),
    }

    sort_thread = threading.Thread(target=sort_algorithms[selected_algo])
    sort_thread.start()

# Giao diện cho phần nhập
input_frame = tk.Frame(win)
input_frame.pack()

# Giao diện cho Manual Input
manual_label = tk.Label(input_frame, text="Manual Input:")
manual_label.pack(side=tk.LEFT)
manual_entry = tk.Entry(input_frame, width=30)
manual_entry.pack(side=tk.LEFT)
manual_entry.insert(0, "3, 5, 4, 9, 8, 7, 1, 2, 10, 6")

manual_button = ttk.Button(input_frame, text="Input Numbers", command=manual_input)
manual_button.pack(side=tk.LEFT, padx=10)

# Giao diện cho Random Input
min_label = tk.Label(input_frame, text="Min:")
min_label.pack(side=tk.LEFT)
min_entry = tk.Entry(input_frame, width=5)
min_entry.pack(side=tk.LEFT)
min_entry.insert(0, "1")

max_label = tk.Label(input_frame, text="Max:")
max_label.pack(side=tk.LEFT)
max_entry = tk.Entry(input_frame, width=5)
max_entry.pack(side=tk.LEFT)
max_entry.insert(0, "100")

count_label = tk.Label(input_frame, text="Count:")
count_label.pack(side=tk.LEFT)
count_entry = tk.Entry(input_frame, width=5)
count_entry.pack(side=tk.LEFT)
count_entry.insert(0, "10")

generate_random_button = ttk.Button(input_frame, text="Generate Number", command=generate_random)
generate_random_button.pack(side=tk.LEFT, padx=10)

# Dropdown menu cho lựa chọn thuật toán sắp xếp
algo_dropdown_label = tk.Label(input_frame, text="Choose algorithm:")
algo_dropdown_label.pack(side=tk.LEFT, padx=10)

algo_options = ["Merge Sort", "Quick Sort", "Selection Sort", "Bubble Sort"]
algo_dropdown = ttk.Combobox(input_frame, values=algo_options)
algo_dropdown.set("Merge Sort")
algo_dropdown.pack(side=tk.LEFT)

# Nút Start Sorting
start_button = ttk.Button(input_frame, text="Start Sorting", command=start_sorting)
start_button.pack(side=tk.LEFT, padx=20)

# Điều khiển thanh trượt (slider)
slider_frame = tk.Frame(win)
slider_frame.pack()

slider_label = tk.Label(slider_frame, text="  Speed:")
slider_label.pack(side=tk.LEFT)
speed_control = ttk.Scale(slider_frame, from_=0, to=300)
speed_control.pack(side=tk.LEFT)
speed_control.set(50)

def update_slider_label(event):
    slider_label.config(text=f"Speed: {int(speed_control.get())}")

speed_control.bind("<Motion>", update_slider_label)

pause_button = ttk.Button(slider_frame, text="Pause", command=toggle_pause_resume)
pause_button.pack(side=tk.LEFT, padx=20)

stop_button = ttk.Button(slider_frame, text="Stop", command=stop_sorting)
stop_button.pack(side=tk.LEFT)

# Vùng biểu đồ cột
chart_area = tk.Canvas(win, bg="white")
chart_area.pack(fill=tk.BOTH, expand=True)

# Bắt đầu giao diện
win.mainloop()
