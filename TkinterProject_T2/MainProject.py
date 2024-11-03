import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# Tạo cửa sổ chính
win = tk.Tk()
win.title("SortingAlgorthim")
width = win.winfo_screenwidth()
height = win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))

data = []
sort_thread = None
is_paused = False
is_stopped = False


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
        data = [
            random.randint(min_val, max_val) for _ in range(count)
        ]  # Tạo số ngẫu nhiên
        draw_bars(data)
    except ValueError:
        pass


# Hàm cho nhập thủ công
def manual_input():
    global data
    chart_area.delete("all")
    try:
        data = list(
            map(int, manual_entry.get().split(","))
        )  # Nhập các số và tách bằng dấu phẩy
        draw_bars(data)
    except ValueError:
        pass


# Hàm tạm dừng và tiếp tục sorting
def toggle_pause_resume():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")


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
        chart_area.create_text(
            x0 + bar_width / 2, y0 - 10, text=str(value), anchor=tk.S
        )
        bar_positions.append((bar, x0, y0, x1, y1))
    win.update_idletasks()
    return bar_positions


# Hàm hoán đổi vị trí của hai thanh với animation mượt mà
def animate_swap(bar_positions, i, j, duration=0.01):
    # Hiện thị màu cho bar khi bị biến đổi
    chart_area.itemconfig(bar_positions[i][0], fill="green")
    chart_area.itemconfig(bar_positions[j][0], fill="green")
    win.update_idletasks()

    # Vị trí của bar_positions
    x0_i, x1_i = bar_positions[i][1], bar_positions[i][3]
    x0_j, x1_j = bar_positions[j][1], bar_positions[j][3]

    # Thực hiện dịch chuyển mượt mà
    steps = 500
    delta_x_i = (x0_j - x0_i) / steps
    delta_x_j = (x0_i - x0_j) / steps

    for step in range(steps):
        chart_area.move(bar_positions[i][0], delta_x_i, 0)
        chart_area.move(bar_positions[j][0], delta_x_j, 0)
        win.update()
        time.sleep(duration / steps)

    bar_positions[i], bar_positions[j] = bar_positions[j], bar_positions[i]
    win.update_idletasks()


# Thuật toán Merge Sort
def merge_sort(data, left, right):
    bar_positions = draw_bars(data)  # Hình dung mảng ban đầu
    if left < right:
        m = (left + right) // 2
        merge_sort(data, left, m)
        merge_sort(data, m + 1, right)

        # Tối ưu hóa: Bỏ qua việc hợp nhất nếu đã được sắp xếp
        if data[m] <= data[m + 1]:
            return

        # Hợp nhất hai nửa
        merge(data, bar_positions, left, m, right)
        draw_bars(data)  # Final draw after merge


def merge(data, bar_positions, left, m, right):
    global is_paused, is_stopped
    j = m + 1
    while left <= m and j <= right:
        while is_paused:
            time.sleep(0.1)
        if is_stopped:
            return data
        win.update_idletasks()
        animate_swap(bar_positions, left, j)  # So sánh
        draw_bars(data)
        time.sleep(speed_control.get() / 300)
        if data[left] <= data[j]:
            left += 1
        else:
            temp = data[j]
            i = j
            while i != left:
                data[i] = data[i - 1]  # Các yếu tố chuyển dịch
                i -= 1
                animate_swap(bar_positions, i, j)  # Chuyển dịch
                draw_bars(data)
                time.sleep(speed_control.get() / 300)
            data[left] = temp  # Đặt phần tử nhỏ hơn vào đúng vị trí
            left += 1
            m += 1
            j += 1
        draw_bars(data)
        time.sleep(speed_control.get() / 300)
        win.update_idletasks()


# Thuật toán Quick Sort
def quick_sort(data, low, high):
    if low < high:
        pi = partition(data, low, high)
        draw_bars(data, ["green" if x == pi else "blue" for x in range(len(data))])
        time.sleep(speed_control.get() / 100)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)


# Phân vùng cho Quick Sort
def partition(data, low, high):
    bar_positions = draw_bars(data)
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        draw_bars(data, ["red" if x == j else "blue" for x in range(len(data))])
        win.update_idletasks()
        time.sleep(speed_control.get() / 300)
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            animate_swap(bar_positions, i, j)
            bar_positions = draw_bars(data)
            time.sleep(speed_control.get() / 100)
    data[i + 1], data[high] = data[high], data[i + 1]
    draw_bars(
        data, ["green" if x == i + 1 or x == high else "blue" for x in range(len(data))]
    )
    win.update_idletasks()
    time.sleep(speed_control.get() / 300)
    return i + 1


# Thuật toán Selection Sort
def selection_sort(data):
    is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            while is_paused:
                time.sleep(0.1)
            if is_stopped:
                return
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        animate_swap(bar_positions, i, min_index)  # Thực hiện hoán đổi animation
        bar_positions = draw_bars(
            data
        )  # Cập nhật lại vị trí của các cột sau khi hoán đổi
        time.sleep(speed_control.get() / 300)
        win.update_idletasks()


# Thuật toán Bubble Sort
def bubble_sort(data):
    is_paused, is_stopped
    n = len(data)
    bar_positions = draw_bars(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            while is_paused:
                time.sleep(0.1)
            if is_stopped:
                return
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]  # Đổi chỗ hai phần tử
                animate_swap(bar_positions, i, j)
                bar_positions = draw_bars(data)
                time.sleep(
                    speed_control.get() / 300
                )  # Điều chỉnh tốc độ bằng thanh trượt


# Chức năng thực hiện sorting theo lựa chọn từ dropdown
def start_sorting():
    global sort_thread, is_paused, is_stopped
    is_paused = False
    is_stopped = False
    selected_algo = algo_dropdown.get()
    match selected_algo:
        case "Merge Sort":
            sort_thread = threading.Thread(
                target=lambda: merge_sort(data, 0, len(data) - 1)
            )
        case "Quick Sort":
            sort_thread = threading.Thread(
                target=lambda: quick_sort(data, 0, len(data) - 1)
            )
        case "Selection Sort":
            sort_thread = threading.Thread(target=lambda: selection_sort(data))
        case "Bubble Sort":
            sort_thread = threading.Thread(target=lambda: bubble_sort(data))
    sort_thread.start()


# Giao diện cho phần nhập
input_frame = tk.Frame(win)
input_frame.pack()

# Dropdown menu cho lựa chọn giữa ngẫu nhiên và nhập thủ công
dropdown_label = tk.Label(input_frame, text="Choose method:")
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
min_entry.insert(0, "1")

max_label = tk.Label(random_frame, text="Max:")
max_label.pack(side=tk.LEFT)
max_entry = tk.Entry(random_frame, width=5)
max_entry.pack(side=tk.LEFT)
max_entry.insert(0, "20")

count_label = tk.Label(random_frame, text="Count:")
count_label.pack(side=tk.LEFT)
count_entry = tk.Entry(random_frame, width=5)
count_entry.pack(side=tk.LEFT)
count_entry.insert(0, "20")

generate_random_button = ttk.Button(
    random_frame, text="Generate Number", command=generate_random
)
generate_random_button.pack(side=tk.LEFT, padx=10)

# Giao diện cho Manual Input
manual_frame = tk.Frame(input_frame)
manual_label = tk.Label(manual_frame, text="Manual Input:")
manual_label.pack(side=tk.LEFT)
manual_entry = tk.Entry(manual_frame, width=30)
manual_entry.pack(side=tk.LEFT)
manual_entry.insert(0, "3, 5, 4, 9, 8, 7, 1, 2, 10, 6")  # Placeholder để gợi ý

manual_button = ttk.Button(manual_frame, text="Input Numbers", command=manual_input)
manual_button.pack(side=tk.LEFT, padx=10)

# Hiển thị giao diện Random ban đầu
random_frame.pack(side=tk.LEFT, padx=10)

# Dropdown menu cho lựa chọn thuật toán sắp xếp
algo_dropdown_label = tk.Label(input_frame, text="Choose sorting algorithm:")
algo_dropdown_label.pack(side=tk.LEFT, padx=10)

algo_options = ["Merge Sort", "Quick Sort", "Selection Sort", "Bubble Sort"]
algo_dropdown = ttk.Combobox(input_frame, values=algo_options)
algo_dropdown.set("Merge Sort")  # Giá trị mặc định
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
