import tkinter as tk
from tkinter import ttk
import random

# algorithm generators
# generators are used so we can go bar by bar and update the canvas after each step, instead of sorting all at once
# yeild is a feature not used often but this is one of the few cases where its very useful

def bubble_sort(data):
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            yield j, j + 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                yield j, j + 1

def selection_sort(data):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            yield min_idx, j
            if data[j] < data[min_idx]:
                min_idx = j
                yield i, min_idx
        data[i], data[min_idx] = data[min_idx], data[i]
        yield i, min_idx

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            yield j, j + 1
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
        yield j + 1, i

def merge_sort(data, start=0, end=None):
    if end is None:
        end = len(data)
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(data, start, mid) # sort left half
        yield from merge_sort(data, mid, end) # sort right half
        left = data[start:mid]
        right = data[mid:end]
        i = j = 0
        for k in range(start, end):
            if j >= len(right) or (i < len(left) and left[i] <= right[j]):
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1
            yield k, k

def quick_sort(data, low=0, high=None):
    if high is None:
        high = len(data) - 1
    if low < high:
        pivot = data[high]
        i = low
        for j in range(low, high):
            yield j, high
            if data[j] < pivot:
                data[i], data[j] = data[j], data[i]
                yield i, j
                i += 1
        data[i], data[high] = data[high], data[i]
        yield i, high
        yield from quick_sort(data, low, i - 1)
        yield from quick_sort(data, i + 1, high)

# Heap Sort is a bit more complex due to the need to maintain the heap property
# first time using this algorithm actually
def heap_sort(data):
    # heapify aka sift down to maintain max heap property
    def heapify(n, i):
        largest = i
        # left and right child indices
        l = 2 * i + 1
        r = 2 * i + 2
        # check if left child is larger than root data point
        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r
        # if largest is not root, swap and continue heapifying
        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            yield i, largest
            yield from heapify(n, largest)
    n = len(data)
    # build max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
    # one by one extract elements from heap
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        yield 0, i
        # call heapify on the reduced heap
        yield from heapify(i, 0)

# init gui
class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")

        self.data = []
        # current sorting algorithm generator
        self.generator = None

        self.setup_ui()
        self.generate_data()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.alg_var = tk.StringVar()
        self.alg_menu = ttk.Combobox(
            frame, textvariable=self.alg_var,
            values=["Bubble Sort", "Selection Sort",
                    "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]
        )
        self.alg_menu.current(0)
        self.alg_menu.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Generate", command=self.generate_data).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Start", command=self.start_sort).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Reset", command=self.generate_data).pack(side=tk.LEFT, padx=5)

        self.speed = tk.Scale(frame, from_=1, to=200,
                              orient=tk.HORIZONTAL, label="Speed (ms)")
        self.speed.set(50)
        self.speed.pack(side=tk.LEFT, padx=5)

        # canvas for drawing bars
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack()

    def generate_data(self):
        self.data = [random.randint(10, 350) for _ in range(50)]
        self.draw_data()

    def draw_data(self, color_positions={}):
        self.canvas.delete("all")
        width = 800 / len(self.data)
        # Draw bars
        for i, val in enumerate(self.data):
            x0 = i * width
            y0 = 400 - val
            x1 = (i + 1) * width
            y1 = 400
            color = color_positions.get(i, "blue")
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        self.root.update_idletasks()

    def start_sort(self):
        alg = self.alg_var.get()
        if alg == "Bubble Sort":
            self.generator = bubble_sort(self.data)
        elif alg == "Selection Sort":
            self.generator = selection_sort(self.data)
        elif alg == "Insertion Sort":
            self.generator = insertion_sort(self.data)
        elif alg == "Merge Sort":
            self.generator = merge_sort(self.data)
        elif alg == "Quick Sort":
            self.generator = quick_sort(self.data)
        elif alg == "Heap Sort":
            self.generator = heap_sort(self.data)

        self.animate()

    # animation loop. take next step from generator, update canvas, repeat until done
    def animate(self):
        try:
            i, j = next(self.generator)
            self.draw_data({i: "red", j: "green"})
            self.root.after(self.speed.get(), self.animate)
        except StopIteration:
            self.draw_data()

# App entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()