from gui import extract_pdf
from utilities import constants

from functools import partial
from pathlib import Path
from tkinter import *
from tkinter import font, filedialog
from tkinter import messagebox as mbox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook

import multiprocessing
import logging
import grip

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

class PDFToolbox(Frame):
    """Create a subclass of Frame for our window."""
    def __init__(self, master=None):
        """Initialize and set the font."""
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Ubuntu", size=16)
        self.init_window()

    def init_window(self):
        """Construct the layout"""
        self.tabs = Notebook(self.master)

        self.extract_tab = Frame(self.tabs)
        self.create_tab = Frame(self.tabs)
        self.tabs.add(self.extract_tab, text="Extract")
        self.tabs.add(self.create_tab, text="Create")
        self.tabs.pack(fill="both", expand=1)

        self.extract_area = extract_pdf.ExtractPDF(self.extract_tab)

        self.main_menu = Menu(self)
        self.file_menu = Menu(self.main_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save as", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.main_menu)

    def on_input_change(self, event):
        """This is currently unfinished."""
        self.text_area.edit_modified(0)
        pass

    def open_file(self):
        """Open a file and clear/insert the text into the text_area."""
        open_filename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*")), initialdir=constants.src_dir)
        if open_filename:
            try:
                with open(open_filename, "r") as stream:
                    open_filename_contents = stream.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, open_filename_contents)
                constants.cur_file = Path(open_filename)
                self.pw_top.tab(self.text_area, text=constants.cur_file.name)
                self.master.title(f"Python Content Creator - {constants.cur_file.name}")
            except:
                mbox.showerror(title="Error", message=f"Error Opening Selected File\n\nThe file you selected: {open_filename} can not be opened!")
    
    def save_file(self):
        """Saves the file with the given filename."""
        file_data = self.text_area.get("1.0" , END)
        save_filename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"), ("Text File", "*.txt")) , title="Save Markdown File")
        if save_filename:
            try:
                with open(save_filename, "w") as stream:
                    stream.write(file_data)
            except:
                mbox.showerror(title="Error", message=f"Error Saving File\n\nThe file: {save_filename} can not be saved!")

    def start_preview(self):
        """Starts the Grip server using multiprocessing library."""
        self.serve_grip = partial(grip.serve, path=constants.cur_file.resolve(), browser=True)
        self.preview_thread = multiprocessing.Process(target=self.serve_grip)
        self.preview_thread.start()

    def stop_preview(self):
        """Stops the Grip server."""
        self.preview_thread.terminate()
        # pass

    def adobe_browse_folder(self):
        """Browse for a folder and set the Entry field to the chosen folder."""
        pdf_dir = filedialog.askdirectory(initialdir=constants.src_dir)
        self.adobe_request_ent_val.set(pdf_dir)

# class PDFToolbox(Frame):
#     """Create a subclass of Frame for our window."""
#     def __init__(self, master=None):
#         """Initialize and set the font."""
#         Frame.__init__(self, master)
#         self.master = master
#         self.myfont = font.Font(family="Ubuntu", size=16)
#         self.init_window()

#     def init_window(self):
#         """Construct the layout"""
#         # This gives a left and right sidebar with a "main area" that is separated top and bottom.
#         self.pw = PanedWindow(orient="horizontal")
#         self.left_sidebar = Notebook(self.pw, width=300)
#         self.main = PanedWindow(self.pw, orient="vertical")
#         self.pw_top = Notebook(self.main)
#         self.pw_bottom = Notebook(self.main, height=100)
#         self.right_sidebar = Notebook(self.pw, width=300)

#         # Top half of main section, includes text area.
#         self.text_area = ScrolledText(self.pw_top, state="normal", wrap="word", pady=2, padx=3, undo=True, width=90, height=27, font=self.myfont)
#         self.text_area.focus_set()
#         default_file = Path("welcome.md").resolve()
#         constants.cur_file = default_file
#         with open(default_file, "r") as stream:
#             default_text = stream.read()
#         self.text_area.insert(0.0, default_text)
#         self.master.title(f"Python Content Creator - {constants.cur_file.name}")

#         # Bottom half of main section includes console.
#         self.console_area = ScrolledText(self.pw_bottom, state="normal", wrap="word", pady=2, padx=3, height=13)

#         # Right sidebar with extraction, conversion, import and preview tabs.
#         # Extraction tab construction.
#         self.extraction_tab = Frame(self.right_sidebar, width=100)
#         self.adobe_request = Frame(self.extraction_tab, relief="groove", borderwidth=3)
#         self.adobe_request.pack(fill="x", expand=1)
#         self.adobe_request_lbl = Label(self.adobe_request, text="Adobe PDF Extract API")
#         self.adobe_request_lbl.pack(fill="x", expand=1)
#         self.adobe_request_ent_val = StringVar()
#         self.adobe_request_ent = Entry(self.adobe_request, textvariable=self.adobe_request_ent_val)
#         self.adobe_request_ent.pack(fill="x", expand=1, side="left")
#         self.adobe_request_btn = Button(self.adobe_request, text="Browse", command=self.adobe_browse_folder)
#         self.adobe_request_btn.pack(fill="x", expand=1, side="right")
#         self.pdf_preview_area = Frame(self.extraction_tab)
#         self.pdf_preview = pdf_viewer.PDFPreview(self.pdf_preview_area)
#         self.pdf_preview.pack(fill="x", expand=1)
#         self.pdf_preview_area.pack(fill="x", expand=1)

#         self.conversion_tab = Frame(self.right_sidebar, width=100)
#         self.database_tab = Frame(self.right_sidebar, width=100)
#         # Preview tab construction.
#         self.preview_tab = Frame(self.right_sidebar, width=100)
#         self.preview_area = Frame(self.preview_tab, relief="groove", borderwidth=3)
#         self.preview_area.pack(fill="x", expand=1)
#         self.lbl_preview = Label(self.preview_area, text="Browser Preview")
#         self.lbl_preview.pack(fill="none", expand=1)
#         self.btn_preview_start = Button(self.preview_area, text="Start Preview", state="active", command=self.start_preview)
#         self.btn_preview_start.pack(fill="x", expand=1, padx=(10,5), pady=(10,10), side="left")
#         self.btn_preview_stop = Button(self.preview_area, text="Stop Preview", state="normal", command=self.stop_preview)
#         self.btn_preview_stop.pack(fill="x", expand=1, padx=(5,10), pady=(10,10), side="right")
#         # Add the tabs to the right sidebar.
#         self.right_sidebar.add(self.extraction_tab, text="Extract", sticky="nsew")
#         self.right_sidebar.add(self.conversion_tab, text="Convert", sticky="nsew")
#         self.right_sidebar.add(self.database_tab, text="Import", sticky="nsew")
#         self.right_sidebar.add(self.preview_tab, text="Preview", sticky="nsew")

#         # Left sidebar with directory/tree view tab.
#         self.tree_view_tab = Frame(self.left_sidebar)
#         self.left_sidebar.add(self.tree_view_tab, text="Tree View")

#         # add the paned window to the root
#         self.pw.pack(fill="both", expand=True)

#         # add the sidebars and main area to the root paned window, note the order
#         self.pw.add(self.left_sidebar)
#         self.pw.add(self.main)
#         self.pw.add(self.right_sidebar)

#         # add the top and bottom to the main window
#         self.main.add(self.pw_top)
#         self.main.add(self.pw_bottom)

#         # add top and bottom sections of main window area
#         self.pw_top.add(self.text_area, text=constants.cur_file.name)
#         self.pw_bottom.add(self.console_area, text="Console")


#         self.text_area.bind("<<Modified>>", self.on_input_change)
#         self.main_menu = Menu(self)
#         self.file_menu = Menu(self.main_menu)
#         self.file_menu.add_command(label="Open", command=self.open_file)
#         self.file_menu.add_command(label="Save as", command=self.save_file)
#         self.file_menu.add_separator()
#         self.file_menu.add_command(label="Exit", command=self.quit)
#         self.main_menu.add_cascade(label="File", menu=self.file_menu)
#         self.master.config(menu=self.main_menu)

#     def on_input_change(self, event):
#         """This is currently unfinished."""
#         self.text_area.edit_modified(0)
#         pass

#     def open_file(self):
#         """Open a file and clear/insert the text into the text_area."""
#         open_filename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*")), initialdir=constants.src_dir)
#         if open_filename:
#             try:
#                 with open(open_filename, "r") as stream:
#                     open_filename_contents = stream.read()
#                 self.text_area.delete(1.0, END)
#                 self.text_area.insert(END, open_filename_contents)
#                 constants.cur_file = Path(open_filename)
#                 self.pw_top.tab(self.text_area, text=constants.cur_file.name)
#                 self.master.title(f"Python Content Creator - {constants.cur_file.name}")
#             except:
#                 mbox.showerror(f"Error Opening Selected File\n\nThe file you selected: {open_filename} can not be opened!")
    
#     def save_file(self):
#         """Saves the file with the given filename."""
#         file_data = self.text_area.get("1.0" , END)
#         save_filename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"), ("Text File", "*.txt")) , title="Save Markdown File")
#         if save_filename:
#             try:
#                 with open(save_filename, "w") as stream:
#                     stream.write(file_data)
#             except:
#                 mbox.showerror(f"Error Saving File\n\nThe file: {save_filename} can not be saved!")

#     def start_preview(self):
#         """Starts the Grip server using multiprocessing library."""
#         self.serve_grip = partial(grip.serve, path=constants.cur_file.resolve(), browser=True)
#         self.preview_thread = multiprocessing.Process(target=self.serve_grip)
#         self.preview_thread.start()

#     def stop_preview(self):
#         """Stops the Grip server."""
#         self.preview_thread.terminate()
#         # pass

#     def adobe_browse_folder(self):
#         """Browse for a folder and set the Entry field to the chosen folder."""
#         pdf_dir = filedialog.askdirectory(initialdir=constants.src_dir)
#         self.adobe_request_ent_val.set(pdf_dir)
            
# Instantiate the root window, set the screen size and instantiate the PCC window
# before running the main loop.
root = Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x{screen_height}")
app = PDFToolbox(root)
app.mainloop()
