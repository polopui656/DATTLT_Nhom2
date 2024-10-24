import tkinter as tk
import random


def swap_two_pos(pos_0, pos_1):
    Bar1x1, _, Bar1x2, _ = canvas.coords(pos_0)
    Bar2x1, _, Bar2x2, _ = canvas.coords(pos_1)
    canvas.move(pos_0, Bar2x1-Bar1x1, 0)
    canvas.move(pos_1, Bar1x2-Bar2x2, 0)


def _insertion_sort():
    global barList
    global lengthList

    for i in range(len(lengthList)):
        cursor = lengthList[i]
        cursorBar = barList[i]
        pos = i

        while pos > 0 and lengthList[pos - 1] > cursor:
            lengthList[pos] = lengthList[pos - 1]
            barList[pos], barList[pos - 1] = barList[pos - 1], barList[pos]
            swap_two_pos(barList[pos],barList[pos-1])   # <-- updates the display
            yield                                       # <-- suspends the execution
            pos -= 1                                    # <-- execution resumes here when next is called

        lengthList[pos] = cursor
        barList[pos] = cursorBar
        swap_two_pos(barList[pos],cursorBar)


worker = None    # <-- Not a thread in spite of the name.

def insertion_sort():     # <-- commands the start of both the animation, and the sort
    global worker
    worker = _insertion_sort()
    animate()


def animate():      # <-- commands resuming the sort once the display has been updated
                    # controls the pace of the animation
    global worker
    if worker is not None:
        try:
            next(worker)
            window.after(10, animate)    # <-- repeats until the sort is complete,
        except StopIteration:            # when the generator is exhausted
            worker = None
        finally:
            window.after_cancel(animate) # <-- stop the callbacks


def shuffle():
    global barList
    global lengthList
    canvas.delete('all')
    xstart = 5
    xend = 15
    barList = []
    lengthList = []

    for x in range(1, 60):
        randomY = random.randint(1, 390)
        x = canvas.create_rectangle(xstart, randomY, xend, 395, fill='red')
        barList.append(x)
        xstart += 10
        xend += 10

    for bar in barList:
        x = canvas.coords(bar)
        length = x[3] - x[1]
        lengthList.append(length)

    for i in range(len(lengthList)-1):
        if lengthList[i] == min(lengthList):
            canvas.itemconfig(barList[i], fill='blue')
        elif lengthList[i] == max(lengthList):
            canvas.itemconfig(barList[i], fill='green')


window = tk.Tk()
window.title('Sorting')
window.geometry('600x435')
canvas = tk.Canvas(window, width='600', height='400')
canvas.grid(column=0,row=0, columnspan = 50)

insert = tk.Button(window, text='Insertion Sort', command=insertion_sort)
shuf = tk.Button(window, text='Shuffle', command=shuffle)
insert.grid(column=1,row=1)
shuf.grid(column=0, row=1)

shuffle()
window.mainloop()