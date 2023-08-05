import tkinter as tk
import tkinter.ttk as ttk
import os, sys
import subprocess


def stylename_elements_options(widgetclass, *args, **kwargs):
    """Function to expose the options of every element associated to a widget stylename.

    Requires instantiation, so pass *args and **kwargs for a proper call of the widget class.
    Ex:
        stylename_elements_options(ttk.OptionMenu,master="None",variable="None")
    """

    def iter_layout(layout, tab_amnt=0, elements=[]):
        """Recursively prints the layout children."""
        el_tabs = "  " * tab_amnt
        val_tabs = "  " * (tab_amnt + 1)

        for element, child in layout:
            elements.append(element)
            print(el_tabs + "'{}': {}".format(element, "{"))
            for key, value in child.items():
                if type(value) == str:
                    print(val_tabs + "'{}' : '{}',".format(key, value))
                else:
                    print(val_tabs + "'{}' : [(".format(key))
                    iter_layout(value, tab_amnt=tab_amnt + 3)
                    print(val_tabs + ")]")

            print(el_tabs + "{}{}".format("} // ", element))

        return elements

    widget = widgetclass(*args, **kwargs)
    stylename = widget.winfo_class()
    try:
        # Get widget elements
        style = ttk.Style()
        layout = style.layout(stylename)
        config = widget.configure()

        print("{:*^50}\n".format(f"Style = {stylename}"))

        print("{:*^50}".format("Config"))
        for key, value in config.items():
            print("{:<15}{:^10}{}".format(key, "=>", value))

        print("\n{:*^50}".format("Layout"))
        elements = iter_layout(layout)

        # Get options of widget elements
        print("\n{:*^50}".format("element options"))
        for element in elements:
            print("{0:30} options: {1}".format(element, style.element_options(element)))

    except tk.TclError:
        print(
            '_tkinter.TclError: "{0}" in function'
            "widget_elements_options({0}) is not a regonised stylename.".format(
                stylename
            )
        )


def multisplit(string, *splitters):
    results = [string]
    for splitter in splitters:
        for i, result in enumerate(results):
            splitstring = result.split(splitter)
            results.pop(i)
            for j, substring in enumerate(splitstring):
                results.insert(i + j, substring)

            pass
    return results


def check_updates():  # pragma: no cover
    python_path = f'"{os.path.join(sys.executable, "..")}"'
    sysand = "&&"
    pip_command = "pip list --outdated"
    stream = os.popen(f"cd {python_path} {sysand} activate {sysand} {pip_command}")
    output = stream.read()
    split = multisplit(output, " ", "\n")
    filtered = [val for val in split if val]

    if "ctpros" in output:
        index = filtered.index("ctpros")
        old_version = filtered[index + 1]
        new_version = filtered[index + 2]
        return old_version, new_version
    else:
        return None


def update():
    python_path = f'"{os.path.join(sys.executable, "..")}"'
    sysand = "&&"
    pip_command = "pip install -U ctpros"
    stream = os.popen(f"cd {python_path} {sysand} activate {sysand} {pip_command}")
    output = stream.read()
    updated = not output[0:30] == "Requirement already up-to-date"
    return updated
