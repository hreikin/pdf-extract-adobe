from pathlib import Path
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
from tkinter.ttk import Notebook
import file_menu
import edit_menu
import format_menu
import help_menu
import grip

root = Tk()
# root.tk_setPalette("darkgrey")
root.title("Python Content Creator")
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")

# This gives a sidebar and a "main area" that is separated top and bottom.
pw = PanedWindow(orient="horizontal")
sidebar = Notebook(pw, width=300)
main = PanedWindow(pw, orient="vertical")
pw_top = Notebook(main, height=800)
pw_bottom = Notebook(main, height=100)
# Top half of main section, includes text area.
text_area = ScrolledText(pw_top, state="normal", wrap="word", pady=2, padx=3, undo=True, height=50)
text_area.focus_set()
text_area.pack(fill="both", expand=True)
# Bottom half of main section includes console and preview tabs.
console_area = ScrolledText(pw_bottom, state="normal", wrap="word", pady=2, padx=3)
# preview_area = Frame(pw_bottom)
pw_bottom.add(console_area, text="Console")
# pw_bottom.add(preview_area, text="Preview")
# Sidebar with extraction and conversion tabs.
extraction_tab = Frame(sidebar)
sidebar.add(extraction_tab, text="Extract")
conversion_tab = Frame(sidebar)
sidebar.add(conversion_tab, text="Convert")
database_tab = Frame(sidebar)
sidebar.add(database_tab, text="Import")

# add the paned window to the root
pw.pack(fill="both", expand=True)

# add the sidebar and main area to the main paned window
pw.add(sidebar)
pw.add(main)

# add the top and bottom to the sidebar
main.add(pw_top)
main.add(pw_bottom)

menubar = Menu(root)
file_menu.main(root, text_area, menubar)
edit_menu.main(root, text_area, menubar)
format_menu.main(root, text_area, menubar)
help_menu.main(root, text_area, menubar)
root.mainloop()