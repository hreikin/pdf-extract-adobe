from gui import extract_pdf, create_pdf
from utils import constants

from pathlib import Path
# from tkinter import *
import tkinter as tk
from tkinter import font, filedialog, simpledialog
from tkinter import messagebox as mbox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from ttkbootstrap import Notebook

import logging

##################################### LOGS #####################################
# Initialize the logger and specify the level of logging. This will log "DEBUG" 
# and higher messages to file and log "INFO" and higher messages to the console.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    filename='debug.log',
                    filemode='w')

# Define a "handler" which writes "INFO" messages or higher to the "sys.stderr".
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set a format which is simpler for console messages.
formatter = logging.Formatter('[%(asctime)s]: %(message)s', datefmt='%H:%M:%S')

# Tell the console "handler" to use this format.
console.setFormatter(formatter)

# Add the "handler" to the "root logger".
logging.getLogger('').addHandler(console)

################################################################################

# Appends extra headings to constants.headings
new_headings = ["Title"]
for item in constants.headings:
    new_headings.append(item)
    for i in range(0, 101):
        new_headings.append(f"{item}[{i}]")
constants.headings = new_headings

class PDFToolbox(ttk.Frame):
    def __init__(self, master=None):
        """Create a subclass of Frame for our window and then initialize and set 
        the variables."""
        ttk.Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Ubuntu", size=16)
        self.init_window()

    def init_window(self):
        """Construct the layout."""
        self.tabs = ttk.Notebook(self.master)

        # Create two tabs and add them to the notebook.
        self.extract_tab = ttk.Frame(self.tabs)
        self.create_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.create_tab, text="Create")
        self.tabs.add(self.extract_tab, text="Extract")
        self.tabs.pack(fill="both", expand=1)

        # Instantiate the create class for the create tab and configure its 
        # buttons.
        self.create_area = create_pdf.CreatePDF(self.create_tab)
        self.create_area.open_btn.configure(command=self.open_md_file)
        self.create_area.save_as_btn.configure(command=self.save_as_md_file)
        self.create_area.save_btn.configure(command=self.save_md_file)

        # Instantiate the extract class.
        self.extract_area = extract_pdf.ExtractPDF(self.extract_tab)

        # Create main menu layout.
        self.main_menu = ttk.Menu(self)
        self.file_menu = ttk.Menu(self.main_menu)
        self.file_menu.add_command(label="Open Markdown File", command=self.open_md_file)
        self.file_menu.add_command(label="Save as", command=self.save_as_md_file)
        self.file_menu.add_command(label="Save", command=self.save_md_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)

        # Create edit menu layout.
        self.edit_menu = ttk.Menu(self.main_menu)
        self.edit_menu.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=lambda: self.focus_get().event_generate("<<Undo>>"), accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=lambda: self.focus_get().event_generate("<<Redo>>"), accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)

        # Create right click menu layout for the editor.
        self.right_click = ttk.Menu(self.create_area.editor.text_area)
        self.right_click.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.right_click.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.right_click.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.right_click.add_separator()
        self.right_click.add_command(label="Undo", command=lambda: self.focus_get().event_generate("<<Undo>>"), accelerator="Ctrl+Z")
        self.right_click.add_command(label="Redo", command=lambda: self.focus_get().event_generate("<<Redo>>"), accelerator="Ctrl+Y")
        self.right_click.add_separator()
        self.right_click.add_command(label="Find", command=self.find, accelerator="Ctrl+F")
        self.right_click.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")

        # Bind mouse/key events to functions.
        self.create_area.editor.text_area.bind_all("<Control-f>", self.find)
        self.create_area.editor.text_area.bind_all("<Control-a>", self.select_all)
        self.create_area.editor.text_area.bind("<Button-3>", self.popup)
        self.create_area.editor.text_area.bind_all("<<MouseWheel>>", self.scroll_line_numbers)

        # Configure the menus.
        self.master.config(menu=self.main_menu)

    def popup(self, event):
        """Right-click popup at mouse location."""
        self.right_click.post(event.x_root, event.y_root)

    def select_all(self, *args):
        """Select all text within the editor window."""
        self.create_area.editor.text_area.tag_add(SEL, "1.0", END)
        self.create_area.editor.text_area.mark_set(0.0, END)
        self.create_area.editor.text_area.see(INSERT)

    def find(self, *args):
        """Search for a string within the editor window."""
        self.create_area.editor.text_area.tag_remove('found', '1.0', END)
        target = simpledialog.askstring('Find', 'Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.create_area.editor.text_area.search(target, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(target))
                self.create_area.editor.text_area.tag_add('found', idx, lastidx)
                idx = lastidx
            self.create_area.editor.text_area.tag_config('found', foreground='white', background='blue')

    def open_md_file(self):
        """Open a file and clear/insert the text into the text_area."""
        open_filename_md = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*")), initialdir=constants.src_dir)
        if open_filename_md:
            try:
                with open(open_filename_md, "r") as stream:
                    open_filename_contents = stream.read()
                self.create_area.editor.text_area.delete(1.0, END)
                self.create_area.editor.text_area.insert(END, open_filename_contents)
                self.create_area.check_markdown(start="1.0", end=END)
                constants.cur_file = Path(open_filename_md)
            except:
                mbox.showerror(title="Error", message=f"Error Opening Selected File\n\nThe file you selected: {open_filename_md} can not be opened!")
    
    def save_as_md_file(self):
        """Saves the file with the given filename."""
        self.file_data = self.create_area.editor.text_area.get("1.0" , END)
        self.save_filename_md = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"), ("Text File", "*.txt")) , title="Save Markdown File")
        if self.save_filename_md:
            try:
                with open(self.save_filename_md, "w") as stream:
                    stream.write(self.file_data)
            except:
                mbox.showerror(title="Error", message=f"Error Saving File\n\nThe file: {self.save_filename_md} can not be saved!")

    def save_md_file(self):
        """Quick saves the file with its current name, if it fails because no 
        name exists it calls the "save_as_md_file" function."""
        self.file_data = self.create_area.editor.text_area.get("1.0" , END)
        try:
            with open(constants.cur_file, "w") as stream:
                stream.write(self.file_data)
        except:
            self.save_as_md_file()

    def scroll_line_numbers(self):
        """Scroll line numbers at the same time as the text area within the 
        editor."""
        self.create_area.line_nums.yview_scroll(number=1)
            
# Instantiate the root window, set the screen size and instantiate the PDF 
# Toolbox window before running the main loop.
if __name__ == "__main__":
    # root = ttk.Tk()
    # style = ttk.Style("darkly")
    # root = ttk.Window()
    root = ttk.Window(themename="darkly")
    root.title("PDF Toolbox")
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"{screen_width}x{screen_height}")
    app = PDFToolbox(root)
    app.mainloop()
