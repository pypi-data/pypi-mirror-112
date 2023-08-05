import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
from PIL import Image, ImageTk
import threading, time, math
import numpy as np
import sys, os

from . import components as comp


class GUI(comp.backend.BackEnd_MixIn, tk.Tk):
    """
    The GUI is composed of:
        menu = menu bar containing all accessible functionality

        mainframe = frame containing all window contents
            imgframe = frame containing rendered image slices
                tracanvas = transaxial slice canvas
                corcanvas = coronal slice canvas
                sagcanvas = sagittal slice canvas

            infoframe = left portion containing all fields to manipulate tk variables
                imgselect = image selection menu
                imgposition = image voxel position entries and scales
                voi = VOI position, shape, and elsize entries
                options = flaggable checkboxes

        progressbar = bar below mainframe showing processing

        Variables:
            flag_crosshair (bool) = flag to show crosshairs
            flag_voi (bool) = flag to show VOI
            flag_zoom (bool) = flag to zoom into VOI
            imgs [NDArray,...] = list of NDArrays to reference
            samplerate (float) = screen pixel/ micron scale factor
            sampleshape [f,f,f] = total physical sampling space of image/voi
            selected_imgnames [i,i] = image filenames selected in dropdowns
            voi (dict)
                elsize [f,f,f] = physical size of elements
                pos [f,f,f] = image voxel coordinates
                shape [i,i,i] = total # of elements of voi

    """

    def front(self, verbosity=2):
        """Defines all the components positions and the GUI verbosity."""
        self.verbosity = verbosity
        self.menu = comp.menu.MainFrameMenu(self)
        self.config(menu=self.menu)

        self.mainframe = tk.Frame(self)
        self.mainframe.grid(row=0, column=0, sticky="nw")

        self.infoframe = comp.infoframe.InfoFrame(self.mainframe, self)
        self.infoframe.grid(row=0, column=0, sticky="nw")
        self.imgselect = comp.infoframe.ImgSelect(self.infoframe, self)
        self.imgpos = comp.infoframe.ImgPosition(self.infoframe, self)
        self.voiinfo = comp.infoframe.VOIInfo(self.infoframe, self)
        self.options = comp.infoframe.Options(self.infoframe, self)
        self.imgselect.pack(fill="x")
        self.imgpos.pack(fill="x")
        self.voiinfo.pack(fill="x")
        self.options.pack(fill="x")

        self.imgframe = comp.imgframe.ImgFrame(self.mainframe, self)
        self.imgframe.grid(row=0, column=1, sticky="nw")
        self.traframe = comp.imgframe.TraFrame(self.imgframe, self)
        self.corframe = comp.imgframe.CorFrame(self.imgframe, self)
        self.sagframe = comp.imgframe.SagFrame(self.imgframe, self)
        self.traframe.grid(row=1, column=0, sticky="nw")
        self.corframe.grid(row=0, column=0, sticky="nw")
        self.sagframe.grid(row=1, column=1, sticky="nw")

        self.progressbar = comp.progressbar.ProgressBar(self.mainframe, self)
        self.progressbar.grid(row=1, column=0, columnspan=2, sticky="nwe")


class Updater(tk.Toplevel):  # pragma: no cover
    def __init__(self, old_version, new_version):
        super().__init__()
        self.title("ctpros Updater")
        self.lift()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.label = tk.Label(
            self,
            text=f"Current Version: {old_version}   Latest Version:{new_version}",
        )
        self.ok = tk.Button(self, text="Update", command=self.okcommand)
        self.no = tk.Button(self, text="Don't Update", command=self.nocommand)
        self.label.pack(padx=15, pady=[10, 0])
        self.ok.pack()
        self.no.pack(pady=[0, 10])

    def okcommand(self, *args):
        python_path = f'"{os.path.join(sys.executable, "..")}"'
        sysand = "&&"
        pip_command = "pip install -U ctpros"
        os.system(f"cd {python_path} {sysand} activate {sysand} start {pip_command}")
        quit()

    def nocommand(self, *args):
        self.destroy()


class Notification(tk.Toplevel):
    def __init__(self, text):
        super().__init__()
        self.title("ctpros Notification")
        self.lift()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.label = tk.Label(self, text=text)
        self.ok = tk.Button(self, text="Ok", command=self.okcommand)
        self.label.pack(padx=15, pady=[10, 0])
        self.ok.pack(pady=[0, 10])

    def okcommand(self):
        self.destroy()
