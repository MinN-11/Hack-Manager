#!/usr/bin/env python3
# GBA FE Hack Manager by MinN
#
# Simple tk interface

import sys
import os
import threading
import tkinter as tk
from tkinter import scrolledtext
import hack_manager


class RedirectText:
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(tk.END, string)

    def flush(self):
        pass


def call_hack_manager():
    threading.Thread(target=hack_manager.main).start()


def main():
    hack_manager.cd_current()
    if not os.path.isdir("patch"):
        os.mkdir("patch")
    if not os.path.isdir("rom"):
        os.mkdir("rom")
    window = tk.Tk()
    window.title("FEGBA Hack Manager")
    console = scrolledtext.ScrolledText(window)
    console.pack()
    sys.stdout = RedirectText(console)
    button = tk.Button(window, text="Apply Patches", command=call_hack_manager)
    button.pack()
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.mainloop()


if __name__ == '__main__':
    main()
