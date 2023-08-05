import tkinter as tk
import tkinter.ttk as ttk
import copy

from . import backend


class InfoFrame(ttk.LabelFrame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.master = master


class ImgSelect(ttk.LabelFrame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, text="Image Selection")
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):

        # LabelFrames
        self.labelframes = [
            ttk.LabelFrame(self, text=text) for text in ["Primary", "Secondary"]
        ]

        # Dropdowns
        values = self.get_options()
        self.dropdowns = [
            backend.OptionMenu(frame, variable)
            for frame, variable in zip(self.labelframes, self.master.selected_imgnames)
        ]
        self.update_values()
        self.mkcache()

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        [
            labelframe.grid(row=1, column=1 + i, sticky="ew")
            for i, labelframe in enumerate(self.labelframes)
        ]
        [dropdown.pack(ipadx=0, padx=0, ipady=0, pady=0) for dropdown in self.dropdowns]
        [dropdown.config(width=15) for dropdown in self.dropdowns]

    def get_options(self):
        return ["None", *[myimg.filename for myimg in self.master.imgs]]

    def new_selection(self, ind, new_string):
        cache = copy.deepcopy(self.cache)
        self.master.selected_imgnames[ind].set(new_string)
        self.validate_selection(ind)

        if cache != self.cache:
            self.master.refresh()

    def update_values(self):
        filenames = [myimg.filename for myimg in self.master.imgs]
        options = ["None", *filenames]
        callbacks = self.generate_callbacks(options)

        for index, (var, dropdown) in enumerate(
            zip(self.master.selected_imgnames, self.dropdowns)
        ):
            menu = dropdown["menu"]
            menu.delete(0, "end")
            for string in ["None", *filenames]:
                menu.add_command(label=string, command=callbacks[index][string])

    def generate_callbacks(self, newstrings):
        callbacks = {}
        for i in range(2):
            callbacks[i] = {}
            for newstring in newstrings:
                callbacks[i][
                    newstring
                ] = lambda *args, i=i, newstring=newstring: self.new_selection(
                    i, newstring
                )
        return callbacks

    def mkcache(self):
        self.cache = copy.deepcopy(self.master.get_selected_imgnames())

    def validate_selection(self, ind, *args, **kwargs):
        """
        Once an item is selected in the dropdown:

        Enforces the following rules:
        - If an img is selected and is already in another slot, swap the old slot with the cached value of the selected slot
        - If any img is selected, the primary img cannot be None

        """
        other_ind = int(not ind)
        selected_name, other_name = (
            self.master.selected_imgnames[ind].get(),
            self.master.selected_imgnames[other_ind].get(),
        )
        selected_dropdown, other_dropdown = (
            self.dropdowns[ind],
            self.dropdowns[other_ind],
        )
        old_selected_value = self.cache[ind]

        refresh_flag = False

        if selected_name != "None" and selected_name == other_name:
            other_dropdown._variable.set(old_selected_value)

        primary_name = self.master.selected_imgnames[0].get()
        second_name = self.master.selected_imgnames[1].get()
        if primary_name == "None" and second_name != "None":
            self.master.selected_imgnames[1].set("None")
            self.master.selected_imgnames[0].set(second_name)
        self.mkcache()

    def refresh(self):
        """
        Updates structure of radio buttons.
        Applies validation rules.
        """
        self.update_values()


class ImgPosition(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="Image Position", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        # Labels
        self.labels = [ttk.Label(self, text=label) for label in "XYZ"]

        # Entries
        self.entries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(self.master.pos, [0, 0, 0], [0, 0, 0])
        ]

        # Scales
        self.scales = [
            backend.IntScale(
                self,
                orient=tk.VERTICAL,
                variable=var,
                entry=entry,
            )
            for _, (var, entry) in enumerate(zip(self.master.pos, self.entries))
        ]

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        [label.grid(row=1, column=i + 1) for i, label in enumerate(self.labels)]
        [
            entry.grid(row=2, column=i + 1, padx=5, pady=(0, 5))
            for i, entry in enumerate(self.entries)
        ]
        [
            scale.grid(row=3, column=i + 1, pady=(0, 10))
            for i, scale in enumerate(self.scales)
        ]
        self.grid_columnconfigure(4, weight=1)


class VOIInfo(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="VOI Info", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        # Bound Labels
        self.dimlabels = [ttk.Label(self, text=label) for label in "XYZ"]
        self.poslabel = ttk.Label(self, text="Position")
        self.shapelabel = ttk.Label(self, text="Size")
        self.elsizelabel = ttk.Label(self, text="Element Size (\u03bcm)")

        # Position Entries
        self.posentries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(self.master.voi["pos"], [0, 0, 0], [0, 0, 0])
        ]

        # Shape Entries
        self.shapeentries = [
            backend.IntRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(
                self.master.voi["shape"], [1, 1, 1], [1, 1, 1]
            )
        ]

        # Elsize entries
        self.elsizeentries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(
                self.master.voi["elsize"], [1, 1, 1], [1, 1, 1]
            )
        ]

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        [label.grid(row=0, column=i + 2) for i, label in enumerate(self.dimlabels)]
        self.poslabel.grid(row=1, column=1, sticky="e")
        [
            posentry.grid(row=1, column=i + 2, padx=5, pady=5)
            for i, posentry in enumerate(self.posentries)
        ]
        self.shapelabel.grid(row=2, column=1, sticky="e")
        [
            shapeentry.grid(row=2, column=i + 2, pady=5)
            for i, shapeentry in enumerate(self.shapeentries)
        ]
        self.elsizelabel.grid(row=3, column=1, sticky="e")
        [
            elsizeentry.grid(row=3, column=i + 2, pady=5)
            for i, elsizeentry in enumerate(self.elsizeentries)
        ]
        self.grid_columnconfigure(4, weight=1)


class Options(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="Options", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        self.crosshaircheck = ttk.Checkbutton(
            self, text="View Crosshairs", variable=self.master.flag_crosshair
        )
        self.voicheck = ttk.Checkbutton(
            self, text="View VOI", variable=self.master.flag_voi
        )
        self.zoomcheck = ttk.Checkbutton(
            self, text="Zoom to VOI", variable=self.master.flag_zoom
        )

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        self.crosshaircheck.grid(row=0, column=1, sticky="w")
        self.voicheck.grid(row=1, column=1, sticky="w")
        self.zoomcheck.grid(row=2, column=1, sticky="w")
        self.grid_columnconfigure(2, weight=1)
