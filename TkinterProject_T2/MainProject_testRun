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
status_label = tk.Label(win, text="", font=("Helvetica", 12), fg="green")
status_label.pack()

data = []
sort_thread1 = None
sort_thread2 = None
pause_event = threading.Event()
stop_event = threading.Event()

# Hàm cho nút Generate ngẫu nhiên, điền vào Manual Input và nhập thủ công và hiển thị các số trên cả hai biểu đồ
def generate_random_multithreaded():
    global data

    def generate():
        global data
        try:
            # Lấy dữ liệu từ các trường nhập
            min_val = int(min_entry.get())
            max_val = int(max_entry.get())
            count = int(count_entry.get())

            # Kiểm tra giá trị hợp lệ
            if count <= 0:
                raise ValueError("Count must be greater than 0.")
            if min_val >= max_val:
                raise ValueError("Min value must be less than max value.")

            # Tạo dữ liệu nếu hợp lệ
            data = [random.randint(min_val, max_val) for _ in range(count)]
        except ValueError as e:
            # Hiển thị lỗi trên giao diện
            status_label.config(text=f"Error: {str(e)}", fg="red")
            data = []  # Reset dữ liệu nếu xảy ra lỗi


    def update_ui():
        if not data:
            # Không có dữ liệu: hiển thị lỗi
            chart_area_tab1.delete("all")
            chart_area_tab1.create_text(
                150, 300, text="No Data Available", fill="red", font=("Helvetica", 16)
            )
            status_label.config(text="Invalid input! Please check your values.", fg="red")
        else:
            # Có dữ liệu: cập nhật giao diện
            manual_entry.delete(0, tk.END)
            manual_entry.insert(0, ", ".join(map(str, data)))
            chart_areas = [
                chart_area_tab1,
                chart_area_tab2_1, chart_area_tab2_2,
                chart_area_tab3_1, chart_area_tab3_2, chart_area_tab3_3,
                chart_area_tab3_4, chart_area_tab3_5, chart_area_tab3_6,
            ]
            for canva in chart_areas:
                draw_bars(data, canva)
            status_label.config(text="Random data generated successfully!", fg="green")

    # Tạo và chạy luồng để tạo dữ liệu
    generate_thread = threading.Thread(target=generate)
    generate_thread.start()

    # Hàm kiểm tra luồng và cập nhật giao diện
    def wait_for_thread():
        if generate_thread.is_alive():
            win.after(100, wait_for_thread)
        else:
            update_ui()

    wait_for_thread()

# Hàm tạm dừng và tiếp tục sorting
def toggle_pause_resume():
    if pause_event.is_set():
        pause_event.clear()
        pause_button.config(text="Pause")
    else:
        pause_event.set()
        pause_button.config(text="Resume")

def stop_sorting():
    stop_event.set()
    pause_event.clear()  # Bỏ tạm dừng nếu đang dừng
    pause_button.config(text="Pause")

# Hàm cho chức năng vẽ bar chart, áp dụng cho mỗi biểu đồ riêng
def draw_bars(data, chart_area, color_array=None):
    chart_area.delete("all")  # Xóa canvas trước khi vẽ
    max_value = max(data)
    bar_width = int(bar_size_control.get())  # Lấy giá trị kích thước cột từ slider
    spacing = 10
    bar_positions = []

    if color_array is None:
        color_array = ["blue" for _ in range(len(data))]

    for i, value in enumerate(data):
        x0 = i * (bar_width + spacing)
        y0 = 250 - (value / max_value * 200)
        x1 = x0 + bar_width
        y1 = 250
        color = color_array[i]

        bar = chart_area.create_rectangle(x0, y0, x1, y1, fill=color)
        chart_area.create_text(
            x0 + bar_width / 2, y0 - 10, text=str(value), anchor=tk.S
        )
        bar_positions.append((bar, x0, y0, x1, y1))
    
    win.update_idletasks()
    return bar_positions
    
def draw_bars_multithreaded(data, chart_area, color_array=None):
    def draw():
        draw_bars(data, chart_area, color_array)
    win.after(0, draw)

    # Xóa nội dung cũ trên canvas
    chart_area.delete("all")

    # Lấy giá trị lớn nhất để chuẩn hóa chiều cao
    max_value = max(data)
    bar_width = max(
        10, min(50, 600 // len(data))
    )  # Điều chỉnh độ rộng cột theo số lượng phần tử
    spacing = 10  # Khoảng cách giữa các cột
    canvas_height = 600  # Chiều cao canvas
    canvas_width = chart_area.winfo_width()  # Chiều rộng canvas hiện tại
    max_bar_width = canvas_width // len(data) - spacing  # Đảm bảo không tràn canvas

    if bar_width > max_bar_width:
        bar_width = max_bar_width

    # Đặt màu mặc định nếu không có mảng màu
    if color_array is None:
        color_array = ["blue" for _ in range(len(data))]

    bar_positions = []  # Danh sách lưu vị trí các thanh

    # Vẽ các thanh biểu đồ
    for i, value in enumerate(data):
        # Tính toán vị trí và kích thước từng thanh
        x0 = i * (bar_width + spacing)
        y0 = canvas_height - (
            value / max_value * (canvas_height - 50)
        )  # Dưới cùng có padding 50
        x1 = x0 + bar_width
        y1 = canvas_height
        color = color_array[i]

        # Tạo thanh và gán văn bản giá trị
        bar = chart_area.create_rectangle(x0, y0, x1, y1, fill=color)
        chart_area.create_text(
            x0 + bar_width / 2,
            y0 - 10,
            text=str(value),
            anchor=tk.S,
            font=("Helvetica", 10),
        )
        bar_positions.append((bar, x0, y0, x1, y1))

    # Cập nhật giao diện ngay lập tức
    win.update_idletasks()
    return bar_positions

# Hàm hoán đổi vị trí của hai thanh với animation mượt mà trên mỗi biểu đồ riêng
def animate_swap(bar_positions, i, j, chart_area, duration=0.01):
    # Đặt màu xanh lá cho các thanh đang chọn
    chart_area.itemconfig(bar_positions[i][0], fill="green")
    chart_area.itemconfig(bar_positions[j][0], fill="green")
    win.update_idletasks()

    x0_i, x1_i = bar_positions[i][1], bar_positions[i][3]
    x0_j, x1_j = bar_positions[j][1], bar_positions[j][3]

    # Chia nhỏ các bước di chuyển để tạo hiệu ứng mượt mà
    steps = 400
    delta_x_i = (x0_j - x0_i) / steps
    delta_x_j = (x0_i - x0_j) / steps

    for step in range(steps):
        while pause_event.is_set():  # Dừng nếu trạng thái Pause được bật
            time.sleep(0.1)
        if stop_event.is_set():  # Thoát nếu trạng thái Stop được bật
            return
        chart_area.move(bar_positions[i][0], delta_x_i, 0)
        chart_area.move(bar_positions[j][0], delta_x_j, 0)
        win.update_idletasks()
        time.sleep(duration / steps)

    # Hoán đổi vị trí trong danh sách
    bar_positions[i], bar_positions[j] = bar_positions[j], bar_positions[i]
    win.update_idletasks()

def animate_swap_multithreaded(bar_positions, i, j, chart_area, duration=0.01):
    def swap():
        animate_swap(bar_positions, i, j, chart_area, duration)
    thread = threading.Thread(target=swap)
    thread.start()

# Thuật toán Merge Sort
def merge_sort(data, l, r, chart_area):
    global pause_event, stop_event
    if stop_event.is_set():
        return
    if l < r:
        m = l + (r - l) // 2
        merge_sort(data, l, m, chart_area)
        merge_sort(data, m + 1, r, chart_area)
        merge(data, l, m, r, chart_area)
        draw_bars(data, chart_area)

def merge(data, l, m, r, chart_area):
    global pause_event, stop_event

    n1 = m - l + 1
    n2 = r - m
    L = data[l : m + 1]
    R = data[m + 1 : r + 1]

    i = j = 0
    k = l
    bar_positions = draw_bars(data, chart_area)

    while i < n1 and j < n2:
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        if L[i] <= R[j]:
            data[k] = L[i]
            animate_swap(bar_positions, l + i, k, chart_area)
            i += 1
        else:
            data[k] = R[j]
            animate_swap(bar_positions, m + 1 + j, k, chart_area)
            j += 1
        bar_positions = draw_bars(data, chart_area)
        time.sleep(0.3 / speed_control.get())
        k += 1

    while i < n1:
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        data[k] = L[i]
        animate_swap(bar_positions, l + i, k, chart_area)
        bar_positions = draw_bars(data, chart_area)
        i += 1
        k += 1

    while j < n2:
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        data[k] = R[j]
        animate_swap(bar_positions, m + 1 + j, k, chart_area)
        bar_positions = draw_bars(data, chart_area)
        j += 1
        k += 1

# Thuật toán Quick Sort
def quick_sort(data, low, high, chart_area):
    global pause_event, stop_event
    if stop_event.is_set():
        return
    if low < high:
        pi = partition(data, low, high, chart_area)
        if pi == -1:
            return
        quick_sort(data, low, pi - 1, chart_area)
        quick_sort(data, pi + 1, high, chart_area)

def partition(data, low, high, chart_area):
    global pause_event, stop_event
    pivot = data[high]
    i = low - 1
    bar_positions = draw_bars(data, chart_area)

    for j in range(low, high):
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return -1
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            animate_swap(bar_positions, i, j, chart_area)
            bar_positions = draw_bars(data, chart_area)

    data[i + 1], data[high] = data[high], data[i + 1]
    animate_swap(bar_positions, i + 1, high, chart_area)
    bar_positions = draw_bars(data, chart_area)
    time.sleep(0.3 / speed_control.get())
    return i + 1

# Thuật toán Selection Sort
def selection_sort(data, chart_area):
    global pause_event, stop_event
    n = len(data)
    bar_positions = draw_bars(data, chart_area)

    for i in range(n):
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        min_index = i
        for j in range(i + 1, n):
            while pause_event.is_set():
                time.sleep(0.1)
            if stop_event.is_set():
                return
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        animate_swap(bar_positions, i, min_index, chart_area)
        bar_positions = draw_bars(data, chart_area)
        time.sleep(0.3 / speed_control.get())

# Thuật toán Bubble Sort
def bubble_sort(data, chart_area):
    global pause_event, stop_event
    n = len(data)
    bar_positions = draw_bars(data, chart_area)

    for i in range(n):
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        for j in range(0, n - i - 1):
            while pause_event.is_set():
                time.sleep(0.1)
            if stop_event.is_set():
                return
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                animate_swap(bar_positions, j, j + 1, chart_area)
                bar_positions = draw_bars(data, chart_area)
                time.sleep(0.3 / speed_control.get())

# Thuật toán Insertion Sort
def insert_sort(data, chart_area):
    global pause_event, stop_event
    n = len(data)
    bar_positions = draw_bars(data, chart_area)

    for i in range(1, n):
        while pause_event.is_set():
            time.sleep(0.1)
        if stop_event.is_set():
            return
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            while pause_event.is_set():
                time.sleep(0.1)
            if stop_event.is_set():
                return
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
        animate_swap(bar_positions, j + 1, i, chart_area)
        bar_positions = draw_bars(data, chart_area)
        time.sleep(0.3 / speed_control.get())

#Thuật toán Counting Sort
def counting_sort(data, chart_area):
    global pause_event, stop_event
    if not data:
        return
    
    max_val = max(data)
    min_val = min(data)
    range_of_elements = max_val - min_val + 1
    count = [0 for _ in range(range_of_elements)]
    output = [0 for _ in range(len(data))]
    
    for i in range(0, len(data)):
        count[data[i] - min_val] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i-1]
    
    i = len(data)-1
    while i >= 0:
        output[count[data[i] - min_val] - 1] = data[i]
        count[data[i] - min_val] -= 1
        i -= 1
    
    for i in range(0, len(data)):
        data[i] = output[i]
        bar_positions = draw_bars(data, chart_area)
        animate_swap(bar_positions, i, i, chart_area)
        time.sleep(0.3 / speed_control.get())
        
   
# Chức năng thực hiện sorting theo lựa chọn từ dropdown cho từng biểu đồ
def run_sorting_algorithm(selected_algo, data, chart_area, time_label, thread_id):
    global pause_event, stop_event

    # Tập hợp các thuật toán sorting
    sort_algorithms = {
        "Merge Sort": lambda: merge_sort(data, 0, len(data) - 1, chart_area),
        "Quick Sort": lambda: quick_sort(data, 0, len(data) - 1, chart_area),
        "Selection Sort": lambda: selection_sort(data, chart_area),
        "Bubble Sort": lambda: bubble_sort(data, chart_area),
        "Insertion Sort": lambda: insert_sort(data, chart_area),
        "Counting Sort": lambda: counting_sort(data, chart_area),
    }

    try:
        sort_algorithms[selected_algo]()
        if time_label:
            time_label.config(text="Sorting Completed!")
    except Exception as e:
        print(f"Error in sorting algorithm: {e}")


def start_all_tabs_sorting():
    pause_event.clear()
    stop_event.clear()

    if not data:
        status_label.config(text="No Data to Sort!", fg="red")
        return

    # Danh sách các thuật toán và chart areas
    algorithms = [
        (algo_dropdown1.get(), data.copy(), chart_area_tab1),
        (algo_dropdown2_1.get(), data.copy(), chart_area_tab2_1),
        (algo_dropdown2_2.get(), data.copy(), chart_area_tab2_2),
        (algo_dropdown3_1.get(), data.copy(), chart_area_tab3_1),
        (algo_dropdown3_2.get(), data.copy(), chart_area_tab3_2),
        (algo_dropdown3_3.get(), data.copy(), chart_area_tab3_3),
        (algo_dropdown3_4.get(), data.copy(), chart_area_tab3_4),
        (algo_dropdown3_5.get(), data.copy(), chart_area_tab3_5),
        (algo_dropdown3_6.get(), data.copy(), chart_area_tab3_6),
    ]

    # Khởi động sorting trên từng tab
    for algo, data_copy, chart_area in algorithms:
        if algo in ["Merge Sort", "Quick Sort", "Selection Sort", "Bubble Sort", "Insertion Sort","Counting Sort"]:
            threading.Thread(
                target=run_sorting_algorithm,
                args=(algo, data_copy, chart_area, None, 1),
            ).start()
    
def check_threads_complete():
    global threads
    if any(thread.is_alive() for thread in threads):
        win.after(100, check_threads_complete)
    else:
        print("All sorting threads have completed.")
        status_label.config(text="All sorting threads completed!", fg="blue")

# Chức năng sắp xếp thuật toán
def start_sorting():
    global data

    # Lấy dữ liệu từ Manual Input
    try:
        manual_data = list(map(int, manual_entry.get().split(",")))
        if manual_data:
            data = manual_data
    except ValueError:
        status_label.config(
            text="Invalid Manual Input! Please enter comma-separated integers.",
            fg="red",
        )
        return

    if not data:
        status_label.config(text="No Data to Sort! Please generate or input data.", fg="red")
        return

    status_label.config(text="Sorting started...", fg="green")

    # Bắt đầu sorting trên tất cả các tab
    start_all_tabs_sorting()

# Giao diện cho phần nhập và các nút chức năng
input_frame = tk.Frame(win)
input_frame.pack(anchor="w")

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

manual_label = tk.Label(input_frame, text="DATA:")
manual_label.pack(side=tk.LEFT, padx=20)
manual_entry = tk.Entry(input_frame, width=30)
manual_entry.pack(side=tk.LEFT)
manual_entry.insert(0, "3, 5, 4, 9, 8, 7, 1, 2, 10, 6")

# Nút Random & Input
generate_random_button = ttk.Button(
    input_frame, text="Random Number", command=generate_random_multithreaded
)
generate_random_button.pack(side=tk.LEFT)

# Điều khiển tốc độ
slider_frame = tk.Frame(win)
slider_frame.pack(anchor="w")

slider_label = tk.Label(slider_frame, text="Speed:")
slider_label.pack(side=tk.LEFT)
speed_control = ttk.Scale(slider_frame, from_=0, to=300)
speed_control.pack(side=tk.LEFT)
speed_control.set(50)


def update_slider_label(event):
    slider_label.config(text=f"Speed: {int(speed_control.get())}")


speed_control.bind("<Motion>", update_slider_label)

# Nút Pause & Stop
start_sorting_button = ttk.Button(
    slider_frame, text="Start", command=start_sorting
)
start_sorting_button.pack(side=tk.LEFT, padx=10)

pause_button = ttk.Button(slider_frame, text="Pause", command=toggle_pause_resume)
pause_button.pack(side=tk.LEFT, padx=20)

stop_button = ttk.Button(slider_frame, text="Stop", command=stop_sorting)
stop_button.pack(side=tk.LEFT)

# Slider điều chỉnh kích thước cột
size_label = tk.Label(slider_frame, text="Bar Size:")
size_label.pack(side=tk.LEFT, padx=(20, 5))

bar_size_control = ttk.Scale(slider_frame, from_=10, to=100, orient=tk.HORIZONTAL)
bar_size_control.pack(side=tk.LEFT)
bar_size_control.set(35 )  # Giá trị mặc định

def update_bar_size(event):
    chart_areas = [
                    chart_area_tab1,
                    chart_area_tab2_1, chart_area_tab2_1,
                    chart_area_tab3_1, chart_area_tab3_2, chart_area_tab3_3,
                    chart_area_tab3_4, chart_area_tab3_5, chart_area_tab3_6,
                ]
    for canva in chart_areas:
        draw_bars(data, canva)

# Bind the slider to the update function
bar_size_control.bind("<Motion>", update_bar_size)

# Bảng Thứ 1
# Tạo TabControl và các Tab
TabControl = ttk.Notebook(win)

# Tab 1
ftab1 = ttk.Frame(TabControl)
# Dropdown Thuật Toán của Tab 1
algo_dropdown1 = ttk.Combobox(
    ftab1,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",  # Dropdown chỉ đọc
)
algo_dropdown1.set("Merge Sort")
algo_dropdown1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
chart_area_tab1 = tk.Canvas(ftab1, bg="white")
chart_area_tab1.pack(fill=tk.BOTH, expand=True)

TabControl.add(ftab1, text="One Algorithm")

# Tab 2
ftab2 = ttk.Frame(TabControl)

# Cấu hình lưới cho Tab 2
ftab2.grid_rowconfigure(0, weight=1)  # Hàng 0 co giãn theo chiều dọc
ftab2.grid_columnconfigure(0, weight=1)  # Cột 0 co giãn theo chiều ngang
ftab2.grid_columnconfigure(1, weight=1)  # Cột 1 co giãn theo chiều ngang

# Frame Biểu Đồ 1
frame_tab2_1 = ttk.Frame(ftab2, borderwidth=10, relief=tk.GROOVE)
frame_tab2_1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 2 - Biểu đồ 1
algo_dropdown2_1 = ttk.Combobox(
    frame_tab2_1,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown2_1.set("Merge Sort")
algo_dropdown2_1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab2_1 = tk.Canvas(frame_tab2_1, bg="white")
chart_area_tab2_1.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 2
frame_tab2_2 = ttk.Frame(ftab2, borderwidth=10, relief=tk.GROOVE)
frame_tab2_2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 2 - Biểu đồ 2
algo_dropdown2_2 = ttk.Combobox(
    frame_tab2_2,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown2_2.set("Quick Sort")
algo_dropdown2_2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab2_2 = tk.Canvas(frame_tab2_2, bg="white")
chart_area_tab2_2.pack(fill=tk.BOTH, expand=True)

TabControl.add(ftab2, text="Two Algorithm")

# Tab 3
ftab3 = ttk.Frame(TabControl)

# Cấu hình lưới cho Tab 3
ftab3.grid_rowconfigure(0, weight=1)  # Hàng 0 co giãn theo chiều dọc
ftab3.grid_columnconfigure(0, weight=1)  # Cột 0 co giãn theo chiều ngang
ftab3.grid_columnconfigure(1, weight=1)  # Cột 1 co giãn theo chiều ngang
ftab3.grid_columnconfigure(2, weight=1)  # Cột 2 co giãn theo chiều ngang

# Frame Biểu Đồ 1
frame_tab3_1 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 1
algo_dropdown3_1 = ttk.Combobox(
    frame_tab3_1,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_1.set("Merge Sort")
algo_dropdown3_1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_1 = tk.Canvas(frame_tab3_1, bg="white",)
chart_area_tab3_1.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 2
frame_tab3_2 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 2
algo_dropdown3_2 = ttk.Combobox(
    frame_tab3_2,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_2.set("Quick Sort")
algo_dropdown3_2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_2 = tk.Canvas(frame_tab3_2, bg="white")
chart_area_tab3_2.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 3
frame_tab3_3 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 3
algo_dropdown3_3 = ttk.Combobox(
    frame_tab3_3,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_3.set("Selection Sort")
algo_dropdown3_3.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_3 = tk.Canvas(frame_tab3_3, bg="white")
chart_area_tab3_3.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 4
frame_tab3_4 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 4
algo_dropdown3_4 = ttk.Combobox(
    frame_tab3_4,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_4.set("Bubble Sort")
algo_dropdown3_4.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_4 = tk.Canvas(frame_tab3_4, bg="white")
chart_area_tab3_4.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 5
frame_tab3_5 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_5.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 5
algo_dropdown3_5 = ttk.Combobox(
    frame_tab3_5,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_5.set("Insertion Sort")
algo_dropdown3_5.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_5 = tk.Canvas(frame_tab3_5, bg="white")
chart_area_tab3_5.pack(fill=tk.BOTH, expand=True)

# Frame Biểu Đồ 6
frame_tab3_6 = ttk.Frame(ftab3, borderwidth=10, relief=tk.GROOVE)
frame_tab3_6.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

# Dropdown Thuật Toán của Tab 3 - Biểu đồ 6
algo_dropdown3_6 = ttk.Combobox(
    frame_tab3_6,
    values=[
        "Merge Sort",
        "Quick Sort",
        "Selection Sort",
        "Bubble Sort",
        "Insertion Sort",
        "Counting Sort"
    ],
    state="readonly",
)
algo_dropdown3_6.set("Counting Sort")
algo_dropdown3_6.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

chart_area_tab3_6 = tk.Canvas(frame_tab3_6, bg="white")
chart_area_tab3_6.pack(fill=tk.BOTH, expand=True)

TabControl.add(ftab3, text="ALL Algorithm")

TabControl.pack(expand=1, fill="both")

# Bắt đầu Giao diện
win.mainloop()
