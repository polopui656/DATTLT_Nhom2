import tkinter as tk
import random
import matplotlib.pyplot as plt

def generate_random_numbers():
    try:
        count = int(entry.get())
        random_numbers = [random.randint(0, 999) for _ in range(count)]
        result_label.config(text=", ".join(map(str, random_numbers)))
        plot_bar_chart(random_numbers)
    except ValueError:
        result_label.config(text="Please enter a valid number")

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


root = tk.Tk()
root.title("Random Number Generator")


prompt_label = tk.Label(root, text="Enter the number of random numbers to generate:")
prompt_label.pack()

entry = tk.Entry(root)
entry.pack()

generate_button = tk.Button(root, text="Generate", command=generate_random_numbers)
generate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
