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
sort_thread1 = None
sort_thread2 = None
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

# Hàm cho nhập thủ công và hiển thị các số trên cả hai biểu đồ
def manual_input():
    global data
    try:
        data = list(map(int, manual_entry.get().split(",")))
        draw_bars(data, chart_area1)
        draw_bars(data, chart_area2)
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

# Hàm cho chức năng vẽ bar chart, áp dụng cho mỗi biểu đồ riêng
def draw_bars(data, chart_area, color_array=None):
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

# Hàm hoán đổi vị trí của hai thanh với animation mượt mà trên mỗi biểu đồ riêng
def animate_swap(bar_positions, i, j, chart_area, duration=0.01):
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
def merge_sort(data, l, r, chart_area):
    if l < r:
        m = l + (r-l)//2
        merge_sort(data, l, m, chart_area)
        merge_sort(data, m+1, r, chart_area)
        merge(data, l, m, r, chart_area)
        
def merge(data, l, m, r, chart_area):
    global is_paused, is_stopped
    bar_positions = draw_bars(data, chart_area)
    n1 = m - l + 1
    n2 = r - m
    L = [0] * (n1)
    R = [0] * (n2)

    while is_paused:
        time.sleep(0.1)
    if is_stopped:
        return

    for i in range (0, n1):
        L[i] = data[l + i]
    
    for j in range (0, n2):
        R[j] = data[m + 1 + j]

    i = 0
    j = 0
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            data[k] = L[i]
            animate_swap(bar_positions, l + i, k, chart_area)
            i += 1
        else:
            data[k] = R[j]
            animate_swap( bar_positions, m + 1 + j, k, chart_area)
            j += 1
        k += 1
        bar_positions = draw_bars(data, chart_area)

    while i < n1:
        data[k] = L[i]
        animate_swap(bar_positions, l + i, k, chart_area)
        i += 1
        k += 1
        bar_positions = draw_bars(data, chart_area)

    while j < n2:
        data[k] = R[j]
        animate_swap( bar_positions, m + 1 + j, k, chart_area)
        j += 1
        k += 1
        bar_positions = draw_bars(data, chart_area)
    time.sleep(0.3 /speed_control.get())
    win.update_idletasks()

# Các thuật toán khác cũng sẽ được cập nhật tương tự để sử dụng chart_area thích hợp

# Thuật toán Quick Sort
def quick_sort(data, low, high, chart_area):
    if low < high:
        pi = partition(data, low, high, chart_area)
        quick_sort(data, low, pi - 1, chart_area)
        quick_sort(data, pi + 1, high, chart_area)

def partition(data, low, high, chart_area):
    global is_paused, is_stopped
    bar_positions = draw_bars(data, chart_area)
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
            animate_swap(bar_positions, i, j, chart_area)
            bar_positions = draw_bars(data, chart_area)
            #time.sleep(0.3 /speed_control.get())       
    data[i + 1], data[high] = data[high], data[i + 1]
    animate_swap(bar_positions, i+1, high, chart_area)
    bar_positions = draw_bars(data, chart_area)
    time.sleep(0.3 / speed_control.get())
    win.update_idletasks()
    return i + 1

# Thuật toán Selection Sort
def selection_sort(data, chart_area):
    global is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data, chart_area)
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
        animate_swap(bar_positions, i, min_index, chart_area)
        bar_positions = draw_bars(data, chart_area)
        time.sleep(0.3 /speed_control.get())
        win.update_idletasks()

# Thuật toán Bubble Sort
def bubble_sort(data, chart_area):
    global is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data, chart_area)
    for i in range(n):
        for j in range(0, n - i - 1):
            while is_paused:
                time.sleep(0.1)
            if is_stopped:
                return
            # So sánh hai phần tử liên tiếp
            if data[j] > data[j + 1]:
                # Hoán đổi các phần tử nếu phần tử bên trái lớn hơn phần tử bên phải
                data[j], data[j + 1] = data[j + 1], data[j]
                animate_swap(bar_positions, j, j + 1, chart_area)  # Hiệu ứng di chuyển mượt
                bar_positions = draw_bars(data, chart_area)
                time.sleep(0.3 /speed_control.get())
        # Vẽ lại tất cả thanh với màu xanh dương ngoại trừ những thanh đã sắp xếp xong (màu xanh lá)
        bar_positions = draw_bars(data, chart_area)
        win.update_idletasks()
    # Đảm bảo tất cả thanh trở về màu xanh dương khi sắp xếp xong
    bar_positions = draw_bars(data, chart_area)

def insert_sort(data, chart_area):
    global is_paused, is_stopped
    n = len(data)
    if n<=1:
        return
    bar_positions = draw_bars(data, chart_area)

    for i in range (1,n):
        key=data[i]
        j =i-1
        while j>=0 and key < data[j]:
            data[j+1]= data[j]
            j -= 1
        data[j+1] = key
        
        if j + 1 != i:
            animate_swap(bar_positions, j + 1, i, chart_area)

        bar_positions = draw_bars(data,chart_area)
        win.update_idletasks()
        time.sleep(0.3 /speed_control.get())
    win.update_idletasks()

# Chức năng thực hiện sorting theo lựa chọn từ dropdown cho từng biểu đồ
def run_sorting_algorithm(selected_algo, data, chart_area, time_label):
    start_time = time.time()
    sort_algorithms = {
        "Merge Sort": lambda: merge_sort(data, 0, len(data) - 1, chart_area),
        "Quick Sort": lambda: quick_sort(data, 0, len(data) - 1, chart_area),
        "Selection Sort": lambda: selection_sort(data, chart_area),
        "Bubble Sort": lambda: bubble_sort(data, chart_area),
        "Insertion Sort": lambda: insert_sort(data, chart_area),
    }
    sort_algorithms[selected_algo]()
    end_time = time.time()
    elapsed_time = end_time - start_time
    time_label.config(text=f"Sorting Time: {elapsed_time:.2f} seconds")

def start_sorting():
    global sort_thread1, sort_thread2, is_paused, is_stopped
    is_paused = False
    is_stopped = False
    selected_algo1 = algo_dropdown1.get()
    selected_algo2 = algo_dropdown2.get()

    sort_thread1 = threading.Thread(target=run_sorting_algorithm, args=(selected_algo1, data.copy(), chart_area1, time_label1))
    sort_thread2 = threading.Thread(target=run_sorting_algorithm, args=(selected_algo2, data.copy(), chart_area2, time_label2))

    sort_thread1.start()
    sort_thread2.start()

# Giao diện cho phần nhập và các nút chức năng
input_frame = tk.Frame(win)
input_frame.pack(anchor='w')

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
count_entry.pack(side=tk.LEFT, padx=10)
count_entry.insert(0, "10")

manual_label = tk.Label(input_frame, text="Manual Input:")
manual_label.pack(side=tk.LEFT)
manual_entry = tk.Entry(input_frame, width=30)
manual_entry.pack(side=tk.LEFT)
manual_entry.insert(0, "3, 5, 4, 9, 8, 7, 1, 2, 10, 6")

generate_random_button = ttk.Button(input_frame, text="Random Number", command=generate_random)
generate_random_button.pack(side=tk.LEFT)

manual_button = ttk.Button(input_frame, text="Input Numbers", command=manual_input)
manual_button.pack(side=tk.LEFT)

algo_dropdown1_label = tk.Label(input_frame, text="Choose algorithm for Bar Chart 1:")
algo_dropdown1_label.pack(side=tk.LEFT, padx=5)
algo_dropdown1 = ttk.Combobox(input_frame, values=["Merge Sort", "Quick Sort", "Selection Sort", "Bubble Sort", "Insertion Sort"])
algo_dropdown1.set("Merge Sort")
algo_dropdown1.pack(side=tk.LEFT)

algo_dropdown2_label = tk.Label(input_frame, text="Choose algorithm for Bar Chart 2:")
algo_dropdown2_label.pack(side=tk.LEFT, padx=5)
algo_dropdown2 = ttk.Combobox(input_frame, values=["Merge Sort", "Quick Sort", "Selection Sort", "Bubble Sort", "Insertion Sort"])
algo_dropdown2.set("Quick Sort")
algo_dropdown2.pack(side=tk.LEFT)

start_button = ttk.Button(input_frame, text="Start Sorting", command=start_sorting)
start_button.pack(side=tk.LEFT)

slider_frame = tk.Frame(win)
slider_frame.pack(anchor='w')

slider_label = tk.Label(slider_frame, text="Speed:")
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

frame1 = ttk.Frame(win, height=800, width=700, borderwidth=10, relief=tk.GROOVE)
frame1.pack_propagate(False)
frame1.pack(side=tk.LEFT, anchor="w")

f1_label = ttk.Label(frame1, text="Bar Chart 1")
f1_label.pack()

chart_area1 = tk.Canvas(frame1, bg="white")
chart_area1.pack(fill=tk.BOTH, expand=True)
time_label1 = ttk.Label(frame1, text="Sorting Time: 0.0 seconds")
time_label1.pack()

frame2 = ttk.Frame(win, height=800, width=700, borderwidth=10, relief=tk.GROOVE)
frame2.pack_propagate(False)
frame2.pack(side=tk.LEFT, anchor="e", padx=10)

f2_label = ttk.Label(frame2, text="Bar Chart 2")
f2_label.pack()

chart_area2 = tk.Canvas(frame2, bg="white")
chart_area2.pack(fill=tk.BOTH, expand=True)
time_label2 = ttk.Label(frame2, text="Sorting Time: 0.0 seconds")
time_label2.pack()

win.mainloop()
