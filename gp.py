#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
import os

SCALE = 16


class GpEditor:
    def __init__(self, root, fn):
        self.root = root
        self.fn = fn
        self.width = 8
        self.height = 8
        self.F = np.zeros((self.height, self.width))
        self.dragging = False
        self.drag_val = 0

        if os.path.exists(fn):
            try:
                self.F = np.loadtxt(fn)
                self.height, self.width = self.F.shape
            except Exception:
                messagebox.showerror("Error", "File format wrong.")
                self.F = np.zeros((self.height, self.width))

        self._build_ui()
        self._redraw()

    def _build_ui(self):
        self.root.title(f"gp {self.width}x{self.height}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root,
                                width=self.width * SCALE,
                                height=self.height * SCALE,
                                cursor='crosshair')
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind('<ButtonPress-1>',   self._on_press)
        self.canvas.bind('<B1-Motion>',        self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)

        btn_frame = tk.Frame(self.root, padx=4, pady=4)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(btn_frame, text="Save",   width=8, command=self._save).pack(side=tk.LEFT,  padx=2)
        tk.Button(btn_frame, text="Clear",  width=8, command=self._clear).pack(side=tk.LEFT,  padx=2)
        tk.Button(btn_frame, text="Resize", width=8, command=self._resize).pack(side=tk.LEFT,  padx=2)
        tk.Button(btn_frame, text="Quit",   width=8, command=self._quit).pack(side=tk.RIGHT, padx=2)

        self.status = tk.StringVar(value=f"{self.width}x{self.height}")
        tk.Label(btn_frame, textvariable=self.status, anchor='w').pack(side=tk.LEFT, padx=8)

        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    def _redraw(self):
        self.canvas.delete('all')
        for i in range(self.height):
            for j in range(self.width):
                x0, y0 = j * SCALE, i * SCALE
                fill = '#ffffff' if self.F[i][j] else '#000000'
                self.canvas.create_rectangle(x0, y0, x0 + SCALE, y0 + SCALE,
                                             fill=fill, outline='#00ff00')

    def _cell(self, event):
        cx = event.x // SCALE
        cy = event.y // SCALE
        if 0 <= cx < self.width and 0 <= cy < self.height:
            return cx, cy
        return None, None

    def _on_press(self, event):
        cx, cy = self._cell(event)
        if cx is None:
            return
        self.drag_val = int(self.F[cy][cx]) ^ 1
        self.F[cy][cx] = self.drag_val
        self.dragging = True
        self._redraw()

    def _on_drag(self, event):
        if not self.dragging:
            return
        cx, cy = self._cell(event)
        if cx is None:
            return
        if self.F[cy][cx] != self.drag_val:
            self.F[cy][cx] = self.drag_val
            self._redraw()

    def _on_release(self, event):
        self.dragging = False

    def _save(self):
        np.savetxt(self.fn, self.F, '%d')
        messagebox.showinfo("Saved", f"Written: {self.fn}")

    def _clear(self):
        self.F = np.zeros((self.height, self.width))
        self._redraw()

    def _resize(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Resize")
        dlg.resizable(False, False)
        dlg.grab_set()

        tk.Label(dlg, text="Width:").grid(row=0, column=0, padx=8, pady=6, sticky='e')
        w_var = tk.StringVar(value=str(self.width))
        tk.Entry(dlg, textvariable=w_var, width=6).grid(row=0, column=1, padx=8)

        tk.Label(dlg, text="Height:").grid(row=1, column=0, padx=8, pady=6, sticky='e')
        h_var = tk.StringVar(value=str(self.height))
        tk.Entry(dlg, textvariable=h_var, width=6).grid(row=1, column=1, padx=8)

        def apply():
            try:
                nw = int(w_var.get())
                nh = int(h_var.get())
                if nw < 1 or nh < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Enter positive integers.", parent=dlg)
                return
            self.width, self.height = nw, nh
            self.F = np.zeros((self.height, self.width))
            self.canvas.config(width=self.width * SCALE, height=self.height * SCALE)
            self.root.title(f"gp {self.width}x{self.height}")
            self.status.set(f"{self.width}x{self.height}")
            self._redraw()
            dlg.destroy()

        tk.Button(dlg, text="OK",     width=8, command=apply).grid(row=2, column=0, padx=8, pady=8)
        tk.Button(dlg, text="Cancel", width=8, command=dlg.destroy).grid(row=2, column=1, padx=8, pady=8)

        dlg.bind('<Return>', lambda e: apply())
        dlg.bind('<Escape>', lambda e: dlg.destroy())

    def _quit(self):
        self.root.destroy()


def main():
    if len(sys.argv) < 2:
        print("Usage: gp.py <filename>")
        sys.exit(1)
    root = tk.Tk()
    GpEditor(root, sys.argv[1])
    root.mainloop()


if __name__ == '__main__':
    main()
