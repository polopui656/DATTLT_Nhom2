from heapq import merge
import tkinter as tk
import random
from tkinter import font
import matplotlib.pyplot as plt

# Tạo số ngẫu nhiên
def generate_random_numbers():
    try:
        count = int(entry.get())
        random_numbers = [random.randint(0, 999) for _ in range(count)]
        result_label.config(text=", ".join(map(str, random_numbers)))
        plot_bar_chart(random_numbers)
    except ValueError:
        result_label.config(text="Please enter a valid number")

# Bảng bar chart
def plot_bar_chart(numbers):
    plt.figure(figsize=(10, 6))
    
    # Sử dụng chỉ số làm trục x và giá trị làm độ cao của cột
    indices = range(len(numbers))
    plt.bar(indices, numbers, color='blue')

    # Giá trị số ngẫu nhiên phía dưới mỗi cột
    plt.xticks(indices, numbers, rotation=90)
    
    plt.xlabel("Index (Order of Generation)")
    plt.ylabel("Random Number")
    plt.title("Bar Chart of Random Numbers")
    plt.tight_layout()  
    plt.show()

# Thuật toán Selection Sort
def selection_sort(numbers):
    n = len(numbers)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if numbers[j] < numbers[min_index]:
                min_index = j
        # Hoán đổi vị trí
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
    return numbers

# Thuật toán Merge Sort
def merge_sort(numbers):
    n = len(numbers)
    if n <= 1:
        return n
    
    mid = n // 2
    left = numbers[:mid]
    right = numbers[mid:]

    sortLeft = merge_sort(left)
    sortRight = merge_sort(right)

    return merge(sortLeft, sortRight)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right [j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[:j])

    return result

def sort_numbers():
    if generate_random_numbers:
        sorted_numbers = selection_sort(generate_random_numbers.copy())  
        result_label.config(text=", ".join(map(str, sorted_numbers)))
        plot_bar_chart(sorted_numbers, title="Random Numbers (Sorted by Selection Sort)")


# Main code
root = tk.Tk()
root.geometry('900x500')
root.title("Random Number Generator")

prompt_label = tk.Label(root, text="Enter the number of random numbers to generate:")
prompt_label.config(font=("Courier", 14))
prompt_label.pack()

entry = tk.Entry(root)
entry.pack()

generate_button = tk.Button(root, text="Generate", command=generate_random_numbers)
generate_button.config(font=("Courier", 14))
generate_button.pack()




result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
