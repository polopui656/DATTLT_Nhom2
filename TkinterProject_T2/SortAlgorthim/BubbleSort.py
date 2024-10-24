#Thuật toán Bubble Sort
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j] # Đổi chỗ hai phần tử
                draw_bars(data, ['green' if x == j or x == j+1 else 'blue' for x in range(len(data))]) # Vẽ lại biểu đồ với màu khác cho hai phần tử đang được hoán đổi
    time.sleep(speed_control.get() / 1000)               # Điều chỉnh tốc độ bằng thanh trượt
    draw_bars(data, ['blue' for _ in range(len(data))])  # Trả lại màu mặc định sau khi sắp xếp xong
