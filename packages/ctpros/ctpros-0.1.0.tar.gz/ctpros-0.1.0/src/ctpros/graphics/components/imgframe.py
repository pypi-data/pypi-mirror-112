import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from PIL import Image, ImageTk
import copy

from . import backend


class ImgFrame(ttk.Frame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.master = master

    def refresh(self):
        self.master.traframe.resample()
        self.master.traframe.redraw()
        self.master.corframe.resample()
        self.master.corframe.redraw()
        self.master.sagframe.resample()
        self.master.sagframe.redraw()


class SliceFrame(ttk.LabelFrame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.arrays = []
        self.image = None
        self.canvas = None
        self.parent = parent
        self.master = master

    def resample(self, label=None):
        myimgs = self.master.get_selected_imgs()
        self.arrays = []
        if myimgs and self.master.flag_render.get():
            voi = self.master.generate_voi()
            for myimg in myimgs:
                offset = -(myimg.affine.scale() / 2)
                voi.pos.ravel()[:] += offset
                self.arrays.append(getattr(myimg.generic, label)(voi=voi).view())
                voi.pos.ravel()[:] -= offset
        self.generate_img()

    def normalize_array(self, array):
        if array.dtype in [
            np.uint16,
            np.int16,
            np.int8,
            np.uint8,
            np.single,
            np.double,
        ]:
            array = copy.deepcopy(array)
            array[array < 0] = 0
            array_max = array.max()
            if array_max == 0:
                pass
            elif array_max <= 255:
                array *= int(np.floor(255 / array_max))
            else:
                array //= int(np.ceil(array_max / 255))
            array = array.astype(np.uint8)
        elif array.dtype == np.bool:
            array = array.astype(np.uint8) * 255
        elif array.dtype == np.complex64:
            array = np.absolute(array)
            array /= array.max() / 255
        else:
            raise Exception(f"Unknown scaling for dtype {array.dtype} of array.")
        return array

    def generate_img(self):
        if not self.arrays:
            self.image = None
        else:
            normalized_arrays = [self.normalize_array(array) for array in self.arrays]
            if len(normalized_arrays) == 1:
                final_array = normalized_arrays[0]

            elif len(normalized_arrays) == 2:
                primary, secondary = normalized_arrays
                final_array = np.empty((*primary.shape, 3), np.uint8)
                final_array[:, :, 0] = secondary
                final_array[:, :, 1] = np.minimum(primary, secondary)
                final_array[:, :, 2] = primary

            self.image = ImageTk.PhotoImage(
                master=self.canvas, image=Image.fromarray(final_array)
            )

    def redraw(self):
        self.canvas.draw_image()
        self.canvas.draw_voi()
        self.canvas.draw_crosshairs()

    def refresh(self):
        self.resample()
        self.redraw()


class TraFrame(SliceFrame):
    def __init__(self, *args, text="Transaxial", **kwargs):
        super().__init__(*args, text=text, **kwargs)
        self.canvas = TraCanvas(self, self.master)
        self.canvas.pack(pady=(0, 1))

    def resample(self):
        super().resample("tra")


class CorFrame(SliceFrame):
    def __init__(self, *args, text="Coronal", **kwargs):
        super().__init__(*args, text=text, **kwargs)
        self.canvas = CorCanvas(self, self.master)
        self.canvas.pack(pady=(0, 1))

    def resample(self):
        super().resample("cor")


class SagFrame(SliceFrame):
    def __init__(self, *args, text="Sagittal", **kwargs):
        super().__init__(*args, text=text, **kwargs)
        self.canvas = SagCanvas(self, self.master)
        self.canvas.pack(pady=(0, 1))

    def resample(self):
        super().resample("sag")


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, master, *args, bd=-2, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(width=250, height=250)
        self.master = master
        self.parent = parent
        self.crosshairs = [
            self.create_line(0, 0, 0, 0, fill="cyan"),
            self.create_line(0, 0, 0, 0, fill="cyan"),
        ]
        [self.tag_raise(ch) for ch in self.crosshairs]
        self.voi = self.create_rectangle(0, 0, 0, 0, outline="yellow")
        self.image = None
        self.master.update_idletasks()
        self.bind("<Button-1>", self.cb_lclick)
        self.bind("<B1-Motion>", self.cb_lmotion)
        self.bind("<Double-Button-1>", self.cb_lclick2)
        self.bind("<Button-3>", self.cb_rclick)
        self.bind("<B3-Motion>", self.cb_rmotion)
        self.bind("<Double-Button-3>", self.cb_rclick2)
        self.bind("<Alt-1>", self.cb_altlclick)
        self.bind("<Alt-3>", self.cb_altrclick)
        self.bind("<Shift-3>", self.cb_shiftrclick)

    def draw_image(self):
        image = self.parent.image
        if image is None:
            self.config(width=250, height=250)
        else:
            self.image = self.create_image(0, 0, anchor=tk.NW, image=image)
            self.tag_lower(self.image)
            if self.winfo_height() != image.height():
                self.config(height=image.height())
            if self.winfo_width() != image.width():
                self.config(width=image.width())
            self.master.update_idletasks()

    def draw_crosshairs(self):
        if self.master.flag_crosshair.get() and self.parent.image:
            if self.calc_ch_horz_pos() != tuple(self.coords(self.crosshairs[0])):
                self.coords(self.crosshairs[0], *self.calc_ch_horz_pos())  # horizontal
            if self.calc_ch_vert_pos() != tuple(self.coords(self.crosshairs[1])):
                self.coords(self.crosshairs[1], *self.calc_ch_vert_pos())  # vertical
        else:
            self.coords(self.crosshairs[0], -1, -1, 0, 0)  # horizontal
            self.coords(self.crosshairs[1], -1, -1, 0, 0)  # vertical

    def draw_voi(self):
        if (
            self.master.flag_voi.get()
            and self.parent.image
            and self.check_voi_in_view()
            and not self.master.flag_zoom.get()
        ):

            self.coords(self.voi, *self.calc_voi_params())
        else:
            self.coords(self.voi, -2, -2, 0, 0)

    def calc_ch_horz_pos(self):
        "Returns the pixel position for the horizontal crosshair."
        raise Exception(
            "Expected overwrite of method calc_ch_horz_pos in CustomCanvas subclass."
        )

    def calc_ch_vert_pos(self):
        "Returns the pixel position for the vertical crosshair."
        raise Exception(
            "Expected overwrite of method calc_ch_vert_pos in CustomCanvas subclass."
        )

    def calc_voi_params(self):
        "Returns the tkinter rectangle parameters to draw the VOI onto the canvas."
        raise Exception(
            "Expected overwrite of method calc_voi_params in CustomCanvas subclass."
        )

    def check_voi_in_view(self):
        return Exception(
            "Expected overwrite of method check_voi_in_view in CustomCanvas subclass."
        )

    @backend.cache_event()
    def cb_lclick(self, event):
        raise Exception()

    @backend.cache_event()
    def cb_lclick2(self, event):
        entries = self.master.imgpos.entries
        entries[0].set(np.floor(entries[0].maxval / 2))
        entries[1].set(np.floor(entries[1].maxval / 2))
        entries[2].set(np.floor(entries[2].maxval / 2))
        self.parent.parent.refresh()

    @backend.cache_event()
    def cb_rclick(self, event):
        self.cache["pos"] = self.master.get_selected_imgs()[0].affine.translate()

    def cb_rclick2(self, event):
        myimg = self.master.get_selected_imgs()[0]
        myimg.reset_affine()
        self.parent.parent.refresh()

    @backend.cache_event()
    def cb_rmotion(self, event):
        raise Exception()

    @backend.cache_event(mod="alt")
    def cb_altlclick(self, event):
        raise Exception()

    def cb_altrclick(self, event):
        raise Exception()

    def cb_release(self, event):
        self.cache = {"event": None, "mod": None}

    def cb_lmotion(self, event):
        if self.cache["mod"] == "alt":
            self.cb_altlclick(event)
        else:
            self.cb_lclick(event)

    def cb_shiftrclick(self, event):
        raise Exception()

    def cb_shiftrmotion(self, event):
        raise Exception()


class TraCanvas(CustomCanvas):
    def calc_ch_horz_pos(self):
        pos = (
            (
                self.master.get_pos(2)
                - self.master.get_voi().pos.ravel()[2] * self.master.flag_zoom.get()
                + 0.5
            )
            * self.master.get_selected_imgs()[0].affine.scale()[2]
            * self.master.samplerate.get()
        )
        return pos, 0, pos, self.winfo_height()

    def calc_ch_vert_pos(self):
        pos = (
            (
                self.master.pos[1].get()
                - self.master.get_voi().pos.ravel()[1] * self.master.flag_zoom.get()
                + 0.5
            )
            * self.master.get_selected_imgs()[0].affine.scale()[1]
            * self.master.samplerate.get()
        )
        return 0, pos, self.winfo_width(), pos

    def calc_voi_params(self):
        voi = self.master.get_voi()
        primaryimg = self.master.get_selected_imgs()[0]
        screenshape = (voi.shape) * voi.elsize * self.master.samplerate.get() - 1
        position = (
            voi.pos.ravel() * primaryimg.affine.scale() * self.master.samplerate.get()
        )
        return (
            screenshape[2] + position[2],
            screenshape[1] + position[1],
            position[2],
            position[1],
        )

    def check_voi_in_view(self):
        voi = self.master.get_voi()
        guipos = self.master.pos[0].get() + 0.5
        return (
            guipos >= voi.pos[0]
            and guipos
            < voi.pos[0]
            + voi.shape[0]
            * voi.elsize[0]
            / self.master.get_selected_imgs()[0].affine.scale()[0]
        )

    def calc_img_pixel_pos(self, event):
        x_pixel = (
            event.x
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[1]
            )
            - 0.5
            + self.master.get_voi().pos.ravel()[2] * self.master.flag_zoom.get()
        )
        y_pixel = (
            event.y
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[2]
            )
            - 0.5
            + self.master.get_voi().pos.ravel()[1] * self.master.flag_zoom.get()
        )
        if x_pixel <= 0:
            x_pixel = 0
        if y_pixel <= 0:
            y_pixel = 0
        return x_pixel, y_pixel

    @backend.cache_event()
    def cb_lclick(self, event):
        """Sets the position of the GUI and selected images."""
        x, y = self.calc_img_pixel_pos(event)
        self.master.imgpos.entries[2].set(round(x, 1))
        self.master.imgpos.entries[1].set(round(y, 1))
        self.draw_crosshairs()

    @backend.cache_event(mod="shift")
    def cb_shiftrclick(self, event):
        self.cache["affine"] = self.master.get_selected_imgs()[0].affine.copy()
        self.cb_shiftrmotion(event)

    def cb_shiftrmotion(self, event):
        xcache, ycache = self.calc_img_pixel_pos(self.cache["event"])
        x, y = self.calc_img_pixel_pos(event)
        pos = ((self.master.get_pos().T + 0.5)).ravel()  # array coords
        angle_1 = np.arctan2(ycache - pos[1], xcache - pos[2])
        angle_2 = np.arctan2(y - pos[1], x - pos[2])
        delta = angle_1 - angle_2
        rotation = np.array([0, 0, delta])
        imgpos = self.master.get_selected_imgs()[0].position
        self.master.get_selected_imgs()[0].affine = (
            self.cache["affine"]
            .copy()
            .translate(-imgpos)
            .rotate(*rotation)
            .translate(imgpos)
        )
        self.parent.parent.refresh()

    def cb_rmotion(self, event):
        """Displaces the image itself while maintaining the relative position of the image."""
        if self.cache["mod"] is None:
            x, y = (event.x - self.cache["event"].x, event.y - self.cache["event"].y)
            x, y = [val / self.master.samplerate.get() for val in [x, y]]
            myimg = self.master.get_selected_imgs()[0]
            affine = myimg.affine
            translation = self.cache["pos"] - affine.translate() + [0, y, x]
            translation = np.round(translation / affine.scale(), 1) * affine.scale()
            affine.translate(translation)
            rounded = np.round(affine.translate() / affine.scale(), 1) * affine.scale()
            affine.translate(-affine.translate() + rounded)
            self.parent.parent.refresh()
        elif self.cache["mod"] == "alt":
            self.cb_altrclick(event)
        elif self.cache["mod"] == "shift":
            self.cb_shiftrmotion(event)

    @backend.cache_event(mod="alt")
    def cb_altlclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        self.master.voiinfo.posentries[2].set(round(x, 1))
        self.master.voiinfo.posentries[1].set(round(y, 1))

    @backend.cache_event(mod="alt")
    def cb_altrclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        pos = [float(posentry.get()) for posentry in self.master.voiinfo.posentries]
        elsize = [
            float(elsizeentry.get())
            for elsizeentry in self.master.voiinfo.elsizeentries
        ]
        scale = self.master.get_selected_imgs()[0].affine.scale()
        self.master.voiinfo.shapeentries[2].set(
            int(round((x + 1 - pos[2]) * scale[2] / elsize[2]))
        )
        self.master.voiinfo.shapeentries[1].set(
            int(round((y + 1 - pos[1]) * scale[1] / elsize[1]))
        )


class CorCanvas(CustomCanvas):
    def calc_ch_horz_pos(self):
        pos = (
            (
                self.master.pos[2].get()
                - self.master.get_voi().pos.ravel()[2] * self.master.flag_zoom.get()
            )
            * self.master.samplerate.get()
            * self.master.get_selected_imgs()[0].affine.scale()[2]
        )
        return pos, 0, pos, self.winfo_height()

    def calc_ch_vert_pos(self):
        pos = (
            self.winfo_height()
            - (
                self.master.pos[0].get()
                - self.master.get_voi().pos.ravel()[0] * self.master.flag_zoom.get()
                + 0.5
            )
            * self.master.get_selected_imgs()[0].affine.scale()[0]
            * self.master.samplerate.get()
        )
        return 0, pos, self.winfo_width(), pos

    def calc_voi_params(self):
        voi = self.master.get_voi()
        primaryimg = self.master.get_selected_imgs()[0]
        screenshape = (voi.shape) * voi.elsize * self.master.samplerate.get() - 1
        position = (
            voi.pos.ravel() * primaryimg.affine.scale() * self.master.samplerate.get()
        )
        return (
            screenshape[2] + position[2],
            self.winfo_height() - position[0] - primaryimg.affine.scale()[0],
            position[2],
            self.winfo_height()
            - screenshape[0]
            - primaryimg.affine.scale()[0]
            - position[0],
        )

    def check_voi_in_view(self):
        voi = self.master.get_voi()
        guipos = self.master.pos[1].get() + 0.5
        return (
            guipos >= voi.pos[1]
            and guipos
            < voi.pos[1]
            + voi.shape[1]
            * voi.elsize[1]
            / self.master.get_selected_imgs()[0].affine.scale()[1]
        )

    def calc_img_pixel_pos(self, event):
        x_pixel = (
            event.x
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[0]
            )
            - 0.5
            + self.master.get_voi().pos.ravel()[2] * self.master.flag_zoom.get()
        )
        y_pixel = (
            (self.winfo_height() - event.y)
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[2]
            )
            + (self.master.get_voi().pos.ravel()[0]) * self.master.flag_zoom.get()
            - 0.5
        )
        if x_pixel <= 0:
            x_pixel = 0
        if y_pixel <= 0:
            y_pixel = 0
        return x_pixel, y_pixel

    @backend.cache_event()
    def cb_lclick(self, event):
        """Sets the position of the GUI and selected images."""
        x, y = self.calc_img_pixel_pos(event)
        self.master.imgpos.entries[2].set(round(x, 1))
        self.master.imgpos.entries[0].set(round(y, 1))
        self.draw_crosshairs()

    @backend.cache_event(mod="alt")
    def cb_altlclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        self.master.voiinfo.posentries[2].set(round(x, 1))
        self.master.voiinfo.posentries[0].set(round(y, 1))

    @backend.cache_event(mod="alt")
    def cb_altrclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        pos = [float(posentry.get()) for posentry in self.master.voiinfo.posentries]
        elsize = [
            float(elsizeentry.get())
            for elsizeentry in self.master.voiinfo.elsizeentries
        ]
        scale = self.master.get_selected_imgs()[0].affine.scale()
        self.master.voiinfo.shapeentries[2].set(
            int(round((x + 1 - pos[2]) * scale[2] / elsize[2]))
        )
        self.master.voiinfo.shapeentries[0].set(
            int(round((y + 1 - pos[0]) * scale[0] / elsize[0]))
        )

    def cb_rmotion(self, event):
        """Displaces the image itself while maintaining the relative position of the image."""
        if self.cache["mod"] is None:
            x, y = (event.x - self.cache["event"].x, event.y - self.cache["event"].y)
            x, y = [val / self.master.samplerate.get() for val in [x, y]]
            myimg = self.master.get_selected_imgs()[0]
            affine = myimg.affine
            translation = -affine.translate() + self.cache["pos"] + [-y, 0, x]
            translation = np.round(translation / affine.scale(), 1) * affine.scale()
            affine.translate(translation)
            rounded = np.round(affine.translate() / affine.scale(), 1) * affine.scale()
            affine.translate(-affine.translate() + rounded)
            self.parent.parent.refresh()
        elif self.cache["mod"] is "alt":
            self.cb_altrclick(event)
        elif self.cache["mod"] == "shift":
            self.cb_shiftrmotion(event)

    @backend.cache_event(mod="shift")
    def cb_shiftrclick(self, event):
        self.cache["affine"] = self.master.get_selected_imgs()[0].affine.copy()
        self.cb_shiftrmotion(event)

    def cb_shiftrmotion(self, event):
        xcache, ycache = self.calc_img_pixel_pos(self.cache["event"])
        x, y = self.calc_img_pixel_pos(event)
        pos = ((self.master.get_pos().T + 0.5)).ravel()  # array coords
        angle_1 = np.arctan2(ycache - pos[0], xcache - pos[2])
        angle_2 = np.arctan2(y - pos[0], x - pos[2])
        # pos[0] = self.winfo_height() - pos[0]
        delta = angle_1 - angle_2
        rotation = np.array([0, delta, 0])
        imgpos = self.master.get_selected_imgs()[0].position
        self.master.get_selected_imgs()[0].affine = (
            self.cache["affine"]
            .copy()
            .translate(-imgpos)
            .rotate(*rotation)
            .translate(imgpos)
        )
        self.parent.parent.refresh()


class SagCanvas(CustomCanvas):
    def calc_ch_horz_pos(self):
        pos = (
            (
                self.master.pos[0].get()
                - self.master.get_voi().pos.ravel()[0] * self.master.flag_zoom.get()
                + 0.5
            )
            * self.master.samplerate.get()
            * self.master.get_selected_imgs()[0].affine.scale()[0]
        )
        return pos, 0, pos, self.winfo_height()

    def calc_ch_vert_pos(self):
        pos = (
            (
                self.master.pos[1].get()
                - self.master.get_voi().pos.ravel()[1] * self.master.flag_zoom.get()
                + 0.5
            )
            * self.master.samplerate.get()
            * self.master.get_selected_imgs()[0].affine.scale()[1]
        )
        return 0, pos, self.winfo_width(), pos

    def calc_voi_params(self):
        voi = self.master.get_voi()
        primaryimg = self.master.get_selected_imgs()[0]
        screenshape = (voi.shape) * voi.elsize * self.master.samplerate.get() - 1
        position = (
            voi.pos.ravel() * primaryimg.affine.scale() * self.master.samplerate.get()
        )
        return (
            screenshape[0] + position[0],
            screenshape[1] + position[1],
            position[0],
            position[1],
        )

    def check_voi_in_view(self):
        voi = self.master.get_voi()
        guipos = self.master.pos[2].get() + 0.5
        return (
            guipos >= voi.pos[2]
            and guipos
            < voi.pos[2]
            + voi.shape[2]
            * voi.elsize[2]
            / self.master.get_selected_imgs()[0].affine.scale()[2]
        )

    def calc_img_pixel_pos(self, event):
        x_pixel = (
            event.x
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[0]
            )
            - 0.5
            + self.master.get_voi().pos.ravel()[0] * self.master.flag_zoom.get()
        )
        y_pixel = (
            event.y
            / (
                self.master.samplerate.get()
                * self.master.get_selected_imgs()[0].affine.scale()[1]
            )
            - 0.5
            + self.master.get_voi().pos.ravel()[1] * self.master.flag_zoom.get()
        )
        if x_pixel <= 0:
            x_pixel = 0
        if y_pixel <= 0:
            y_pixel = 0
        return x_pixel, y_pixel

    @backend.cache_event()
    def cb_lclick(self, event):
        """Sets the position of the GUI and selected images."""
        x, y = self.calc_img_pixel_pos(event)
        self.master.imgpos.entries[0].set(round(x, 1))
        self.master.imgpos.entries[1].set(round(y, 1))
        self.draw_crosshairs()

    @backend.cache_event(mod="alt")
    def cb_altlclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        self.master.voiinfo.posentries[0].set(round(x, 1))
        self.master.voiinfo.posentries[1].set(round(y, 1))

    @backend.cache_event(mod="alt")
    def cb_altrclick(self, event):
        if self.master.flag_zoom.get():
            return
        x, y = self.calc_img_pixel_pos(event)
        pos = [float(posentry.get()) for posentry in self.master.voiinfo.posentries]
        elsize = [
            float(elsizeentry.get())
            for elsizeentry in self.master.voiinfo.elsizeentries
        ]
        scale = self.master.get_selected_imgs()[0].affine.scale()
        self.master.voiinfo.shapeentries[0].set(
            int(round((x + 1 - pos[0]) * scale[0] / elsize[0]))
        )
        self.master.voiinfo.shapeentries[1].set(
            int(round((y + 1 - pos[1]) * scale[1] / elsize[1]))
        )

    def cb_rmotion(self, event):
        """Displaces the image itself while maintaining the relative position of the image."""
        if self.cache["mod"] is None:
            x, y = (event.x - self.cache["event"].x, event.y - self.cache["event"].y)
            x, y = [val / self.master.samplerate.get() for val in [x, y]]
            myimg = self.master.get_selected_imgs()[0]
            affine = myimg.affine
            translation = self.cache["pos"] - affine.translate() + [x, y, 0]
            translation = np.round(translation / affine.scale(), 1) * affine.scale()
            affine.translate(translation)
            rounded = np.round(affine.translate() / affine.scale(), 1) * affine.scale()
            affine.translate(-affine.translate() + rounded)
            self.parent.parent.refresh()
        elif self.cache["mod"] is "alt":
            self.cb_altrclick(event)
        elif self.cache["mod"] == "shift":
            self.cb_shiftrmotion(event)

    @backend.cache_event(mod="shift")
    def cb_shiftrclick(self, event):
        self.cache["affine"] = self.master.get_selected_imgs()[0].affine.copy()
        self.cb_shiftrmotion(event)

    def cb_shiftrmotion(self, event):
        xcache, ycache = self.calc_img_pixel_pos(self.cache["event"])
        x, y = self.calc_img_pixel_pos(event)
        pos = ((self.master.get_pos().T + 0.5)).ravel()  # array coords
        angle_1 = np.arctan2(ycache - pos[1], xcache - pos[0])
        angle_2 = np.arctan2(y - pos[1], x - pos[0])
        delta = angle_2 - angle_1
        rotation = np.array([delta, 0, 0])
        imgpos = self.master.get_selected_imgs()[0].position
        self.master.get_selected_imgs()[0].affine = (
            self.cache["affine"]
            .copy()
            .translate(-imgpos)
            .rotate(*rotation)
            .translate(imgpos)
        )
        self.parent.parent.refresh()
