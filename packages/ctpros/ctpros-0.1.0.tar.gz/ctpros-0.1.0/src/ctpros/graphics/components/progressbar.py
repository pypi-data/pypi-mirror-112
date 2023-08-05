import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
import collections
import copy

import numpy as np


class ProgressBar(ttk.Progressbar):
    def __init__(self, parent, master, *args, **kwargs):
        orient = kwargs.pop("orient", tk.HORIZONTAL)
        self.progress = kwargs.pop("variable", tk.DoubleVar())
        self.parent = parent
        self.master = master
        super().__init__(parent, *args, variable=self.progress, orient=orient, **kwargs)

    def run(self, func, *args, **kwargs):
        self.config(mode="indeterminate")
        mythread = threading.Thread(target=func, args=args, kwargs=kwargs)
        mythread.start()
        while mythread.isAlive():
            self.step()
            self.master.update_idletasks()
            time.sleep(0.0075)
        super().stop()
        self.config(mode="determinate")
        self.progress.set(0)


class LinkedIterator(collections.Iterator):
    def __init__(self, iterable, progressbar, w=None):
        if w is None:
            self.w = iter(np.ones(len(iterable)) / len(iterable) * 100)
        else:
            self.w = iter(w / sum(w) * 100)
        self.progressbar = progressbar
        self.progressbar.progress.set(0)
        if not hasattr(iterable, "__next__"):
            self.iter = iter(iterable)
        else:
            self.iter = iterable

    def __next__(self):
        try:
            self.progressbar.step(self.w.__next__())
            self.progressbar.master.update_idletasks()
            return self.iter.__next__()
        except:
            self.progressbar.progress.set(0)
            raise StopIteration
