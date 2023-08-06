import logging
import tkinter as tk
from tkinter.filedialog import askopenfilename

import numpy as np
from PIL import ImageGrab

from map_analyser import maplib as ml


class Viewer:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("{}x{}".format(ZoomCanvas.SIZE[0], ZoomCanvas.SIZE[1]))
        self.window.title("Map analyser")

        self.window.rowconfigure(1, weight=4)
        self.window.columnconfigure(0, weight=4)

        self.label = tk.Label(self.window, text=" ")
        self.label.grid(row=0, column=0)

        canvas_frame = tk.Frame(self.window)
        canvas_frame.grid(row=1, column=0, sticky="nsew")

        self.canvas = ZoomCanvas(canvas_frame)
        self.process_main_callback = True

    def entry(self, main_callback):
        self.callback(main_callback(self))
        self.window.mainloop()

    def callback(self, generator):
        try:
            if self.process_main_callback:
                string = next(generator)
                logging.info(string)
                self.label['text'] = string
            self.window.after(100, lambda: self.callback(generator))
        except StopIteration:
            pass

    def add_areas(self, areas):
        for a in areas:
            self.add_polygon(a)

    def add_map(self, map):
        """
        Displays map image and centers it.
        """
        self.canvas.add_map(map)
        pass

    def add_graph(self, graph):
        lines = []
        for a in graph.areas:
            tmp = a.copy()
            tmp.speed = 100
            self.add_polygon(tmp)
            for area in a.neighbours:
                x1 = np.round(np.average(a.coords.x))
                y1 = np.round(np.average(a.coords.y))
                x2 = np.round(np.average(area.coords.x))
                y2 = np.round(np.average(area.coords.y))
                lines.append([ml.Coord(x1, y1), ml.Coord(x2, y2)])
        for l in lines:
            self.add_path(l, color='#0000FF')

    def get_start_and_end(self):
        start, end = self._start_and_end[:2]
        start, end = ml.Coord(*start), ml.Coord(*end)
        return start, end

    @staticmethod
    def get_file():
        return askopenfilename()

    def click_control_callback(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        print(x, y),
        p = self.canvas.translate_back(ml.Coord(x, y))
        self.add_control(p),
        self._start_and_end.append(p)

    def prompt_start_end(self, bind=True):
        if bind:
            self._start_and_end = []
            self._prompt_start_end_binding = self.window.bind('<ButtonPress-1>', self.click_control_callback)
            self.process_main_callback = False
            # self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
            #                 text="Select start")
        if len(self._start_and_end) >= 2:
            self.window.unbind("<Button 1>", self._prompt_start_end_binding)
            self.process_main_callback = True
        else:
            self.window.after(100, lambda: self.prompt_start_end(bind=False))

    def add_control(self, control, color="#FF0000"):
        p = self.canvas.translate(control)
        i = self.canvas.my_scale * 1000
        self.canvas.create_oval(p[0] - i, p[1] - i, p[0] + i, p[1] + i, fill="", outline=color, width=2)

    def add_path(self, path, color="#FF0000"):
        cs = [self.canvas.translate(p) for p in path]
        self.canvas.create_line(*cs, fill=color)

    def add_polygon(self, polygon):
        cs = list(zip(*self.canvas.translate(polygon.coords)))

        color = "#%02x%02x%02x" % (polygon.r, polygon.g, polygon.b)
        self.canvas.create_polygon(*cs, fill=color, outline='#000000')

    def save_snapshot(self, name):
        x = self.window.winfo_rootx() + self.canvas.winfo_x()
        y = self.window.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(name + '.jpg')


class DebugViewer:
    @staticmethod
    def show(list_of_areas):
        vw = Viewer()
        for a in list_of_areas:
            vw.add_polygon(a)
        # blocking call:
        vw.window.mainloop()

    @staticmethod
    def show_holes(polygon):
        vw = Viewer()
        for hole in polygon.holes:
            fake_polygon = lambda: None
            fake_polygon.coords = ml.CoordsLists(np.asarray([h[0] for h in hole]), np.asarray([h[1] for h in hole]))
            fake_polygon.r = polygon.r
            fake_polygon.g = polygon.g
            fake_polygon.b = polygon.b
            fake_polygon.speed = polygon.speed

            vw.add_polygon(fake_polygon)
        # blocking call:
        vw.window.mainloop()


class TestViewer(Viewer):
    def entry(self, main_callback):
        def cb(_):
            yield 'Started running'

        def main_cb(viewer):
            for s in main_callback(viewer):
                logging.debug(s)

        from threading import Thread
        thread = Thread(target=main_cb, args=(self,))
        thread.start()
        super().entry(cb)

    def add_graph(self, graph):
        self.start, self.end = graph.areas[0].get_center(), graph.areas[-1].get_center()
        self.start, self.end = ml.Coord(3113, 6470), ml.Coord(706, -8650)
        print(self.start, self.end)
        super().add_graph(graph)

    def get_start_and_end(self):
        self.add_control(self.start)
        self.add_control(self.end)
        return self.start, self.end

    def prompt_start_end(self, bind=True):
        pass

    def add_polygon(self, polygon):
        super().add_polygon(polygon)


class ZoomCanvas(tk.Canvas):
    DELTA = 0.75
    GMAPS = True  # False not implemented
    SIZE = (800, 600)

    def __init__(self, master):
        super().__init__(master, highlightthickness=0)

        self.grid(row=0, column=0, sticky='nswe')
        self.master.rowconfigure(0, weight=4)
        self.master.columnconfigure(0, weight=4)

        self.coords_label = tk.Label(master, text=" ")
        self.coords_label.grid(row=2)

        self.my_scale = 1 / 1000
        self.my_w, self.my_h = ZoomCanvas.SIZE

        # Bindings:
        self.bind('<ButtonPress-2>', self._on_move_begin)
        self.bind('<B2-Motion>', self._on_move)
        self.bind('<ButtonPress-3>', self._on_move_begin)  # without mouse
        self.bind('<B3-Motion>', self._on_move)  # without mouse
        self.bind('<MouseWheel>', self._on_zoom)  # windows
        self.bind('<Button-5>', self._on_zoom)  # linux
        self.bind('<Button-4>', self._on_zoom)  # linux
        self.bind("<Configure>", self._on_resize)

        def moved(event):
            x, y = self.canvasx(event.x), self.canvasy(event.y)
            self.coords_label['text'] = f"canvas: {x} {y} map: {self.translate_back(ml.Coord(x, y))}"

        self.bind("<Motion>", moved)

        self.map = None
        # anchors
        self.map_center = self.create_text(0, 0, text='')
        self.canvas00 = self.create_text(0, 0, text='')

    def add_map(self, map):
        self.map = map
        self.map_imageID = None
        self.map_image = None

        # get center
        bb = self.map.get_bounding_box()
        center = ml.Coord(round(self.my_scale * (bb[0].x + bb[1].x) / 2),
                          round(self.my_scale * (bb[0].y + bb[1].y) / 2))

        # set new anchor
        self.map_center = self.create_text(center.x, center.y, text='')

        self._draw_map()

        # move to center
        self.scan_mark(center.x, center.y)
        self.scan_dragto(self.my_w // 2, self.my_h // 2, gain=1)

    def translate(self, coords):
        x, y = self.coords(self.canvas00)
        c = self.my_scale
        return c * (coords[0] + x / c), c * (coords[1] + y / c)

    def translate_back(self, coords):
        x, y = self.coords(self.canvas00)
        c = self.my_scale
        return np.rint(coords.x / c - x / c), np.rint(coords.y / c - y / c)

    def _on_resize(self, event):
        self.scan_mark(self.my_w // 2, self.my_h // 2)
        self.scan_dragto(event.width // 2, event.height // 2, gain=1)  # move to center
        self._draw_map()
        self.my_w, self.my_h = event.width, event.height  # store new size

    def _on_move_begin(self, event):
        # print(str(event.x)+' '+str(event.y))
        self.scan_mark(event.x, event.y)  # remembers previous coords

    def _on_move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)  # gain must be 1 to reflect mouse movement

    def _on_zoom(self, event):
        scale = 1.0
        if event.num == 5 or event.delta == -120:
            scale *= ZoomCanvas.DELTA
            self.my_scale *= ZoomCanvas.DELTA
        if event.num == 4 or event.delta == 120:
            scale /= ZoomCanvas.DELTA
            self.my_scale /= ZoomCanvas.DELTA

        x = self.canvasx(event.x)
        y = self.canvasy(event.y)

        self._rescale(scale, x, y)

    def _draw_map(self):
        if self.map is None:
            return  # no map given

        if self.map_imageID is not None:
            self.delete(self.map_imageID)

        tmp = self.map.get_photo_image(scale=self.my_scale)
        coords = self.coords(self.map_center) if ZoomCanvas.GMAPS else self.canvas00
        self.map_imageID = self.create_image(coords, anchor='center', image=tmp)

        self.lower(self.map_imageID)
        self.map_image = tmp  # stop GC
        # self.canvas['scrollregion'] = self.canvas.bbox('all') #disables running out of screen

    def _rescale(self, scale, x, y):
        # scale all objects:
        self.scale('all', x, y, scale, scale)
        # scale map:
        self._draw_map()
