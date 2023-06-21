import tkinter as tk
from tkinter import filedialog
import os

# From https://github.com/streamlit/streamlit/issues/1019#issuecomment-803550033


def folder_select():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    dirname = os.path.abspath(filedialog.askdirectory(master=root))
    return dirname