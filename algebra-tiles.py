import tkinter as tk

TILE_SIZE = 40

class Tile:
    def __init__(self, tile_type, sign, x, y, canvas):
        self.tile_type = tile_type
        self.sign = sign
        self.x = x
        self.y = y
        self.canvas = canvas
        self.item = None
        self.text = None
        self.draw()
        
    def draw(self):
        color = "skyblue" if self.sign > 0 else "salmon"  # absolute salmon

        if self.tile_type == "x2":
            size = TILE_SIZE * 2
            self.item = self.canvas.create_rectangle(self.x, self.y,self.x + size, self.y + size,fill=color, tags="tile")
            self.text = self.canvas.create_text(self.x + size/2, self.y + size/2, text="x²", tags="tile")
            self.width = size
            self.height = size
        elif self.tile_type == "x":
            width = TILE_SIZE * 2
            height = TILE_SIZE
            self.item = self.canvas.create_rectangle(self.x, self.y,self.x + width, self.y + height,fill=color, tags="tile")
            self.text = self.canvas.create_text(self.x + width/2, self.y + height/2, text="x", tags="tile")
            self.width = width
            self.height = height
        elif self.tile_type == "1":
            size = TILE_SIZE
            self.item = self.canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill=color, tags="tile")
            self.text = self.canvas.create_text(self.x + size/2, self.y + size/2, text="1", tags="tile")
            self.width = size
            self.height = size

    def move(self, dx, dy):
        self.canvas.move(self.item, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self.x += dx
        self.y += dy


class AlgebraTilesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algebra Tiles Simulator")

        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.tiles = []
        self.drag_data = {"tile": None, "x": 0, "y": 0}

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="+ x²", command=lambda: self.add_tile("x2", 1)).grid(row=0, column=0)
        tk.Button(control_frame, text="- x²", command=lambda: self.add_tile("x2", -1)).grid(row=0, column=1)
        tk.Button(control_frame, text="+ x", command=lambda: self.add_tile("x", 1)).grid(row=0, column=2)
        tk.Button(control_frame, text="- x", command=lambda: self.add_tile("x", -1)).grid(row=0, column=3)
        tk.Button(control_frame, text="+ 1", command=lambda: self.add_tile("1", 1)).grid(row=0, column=4)
        tk.Button(control_frame, text="- 1", command=lambda: self.add_tile("1", -1)).grid(row=0, column=5)
        tk.Button(control_frame, text="Clear", command=self.clear).grid(row=0, column=6)

        # Bind dragging events
        self.canvas.tag_bind("tile", "<ButtonPress-1>", self.on_tile_press)
        self.canvas.tag_bind("tile", "<B1-Motion>", self.on_tile_move)
        self.canvas.tag_bind("tile", "<ButtonRelease-1>", self.on_tile_release)

    def add_tile(self, tile_type, sign):
        x_offset, y_offset = 20, 20
        if self.tiles:
            last = self.tiles[-1]
            x_offset = last.x + last.width + 10
            y_offset = last.y
            if x_offset > 750:
                x_offset = 20
                y_offset += 120

        tile = Tile(tile_type, sign, x_offset, y_offset, self.canvas)
        self.tiles.append(tile)

    def clear(self):
        for tile in self.tiles:
            self.canvas.delete(tile.item)
            self.canvas.delete(tile.text)
        self.tiles = []

    # Dragging handlers
    def on_tile_press(self, event):
        # Find which tile was clicked
        items = self.canvas.find_withtag("current")
        for tile in self.tiles:
            if tile.item in items or tile.text in items:
                self.drag_data["tile"] = tile
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                break

    def on_tile_move(self, event):
        tile = self.drag_data["tile"]
        if tile:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            tile.move(dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_tile_release(self, event):
        self.drag_data["tile"] = None


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgebraTilesApp(root)
    root.mainloop()