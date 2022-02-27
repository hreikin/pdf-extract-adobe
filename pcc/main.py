from utilities import constants
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import grip
from pathlib import Path
from functools import partial

def serve_preview():
    try:
        grip.serve(path=constants.cur_file, browser=True)
    except grip.AlreadyRunningError:
        grip.render_page(path=constants.cur_file)

root = tk.Tk()
root.title("Python Content Creator")
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")

# This gives a left and right sidebar with a "main area" that is separated top and bottom.
pw = tk.PanedWindow(orient="horizontal")
left_sidebar = ttk.Notebook(pw, width=300)
main = tk.PanedWindow(pw, orient="vertical")
pw_top = ttk.Notebook(main)
pw_bottom = ttk.Notebook(main, height=100)
right_sidebar = ttk.Notebook(pw, width=300)

# Top half of main section, includes text area.
text_area = scrolledtext.ScrolledText(pw_top, state="normal", wrap="word", pady=2, padx=3, undo=True, width=175, height=50)
text_area.focus_set()
default_file = Path("welcome.md").resolve()
constants.cur_file = default_file
with open(default_file, "r") as stream:
    default_text = stream.read()
text_area.insert(0.0, default_text)

# Bottom half of main section includes console.
console_area = scrolledtext.ScrolledText(pw_bottom, state="normal", wrap="word", pady=2, padx=3)

# Right sidebar with extraction, conversion, import and preview tabs.
extraction_tab = tk.Frame(right_sidebar)
conversion_tab = tk.Frame(right_sidebar)
database_tab = tk.Frame(right_sidebar)
preview_area = tk.Frame(right_sidebar)
grip_serve = partial(serve_preview)
btn_preview = tk.Button(preview_area, text="Preview", command=grip_serve)
btn_preview.pack()
right_sidebar.add(extraction_tab, text="Extract")
right_sidebar.add(conversion_tab, text="Convert")
right_sidebar.add(database_tab, text="Import")
right_sidebar.add(preview_area, text="Preview")

# Left sidebar with directory/tree view tab.
tree_view_tab = tk.Frame(left_sidebar)
left_sidebar.add(tree_view_tab, text="Tree View")

# add the paned window to the root
pw.pack(fill="both", expand=True)

# add the sidebars and main area to the root paned window, note the order
pw.add(left_sidebar)
pw.add(main)
pw.add(right_sidebar)

# add the top and bottom to the main window
main.add(pw_top)
main.add(pw_bottom)

# add top and bottom sections of main window area
pw_top.add(text_area, text=constants.cur_file.name)
pw_bottom.add(console_area, text="Console")

# start the mainloop
root.mainloop()