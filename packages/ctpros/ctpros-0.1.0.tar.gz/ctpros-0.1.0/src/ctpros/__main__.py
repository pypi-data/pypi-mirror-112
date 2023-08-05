# pragma: no cover
import tkinter as tk
import tkinter.ttk as ttk

import sys
from ctpros.graphics import GUI


def main(argv):
    gui = GUI(*argv)
    gui.mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])
