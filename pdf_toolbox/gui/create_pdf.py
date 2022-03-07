from utils import constants

from markdown import Markdown
from pathlib import Path
from tkinter import *
from tkinter import font, filedialog, messagebox
from tkinterweb import HtmlFrame
from tkinter.scrolledtext import ScrolledText

class CreatePDF(Frame):
    def __init__(self, master=None):
        """
        Create a subclass of Frame for our window element. Initialize and set 
        the font and variable defaults.
        """
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Ubuntu", size=16)
        self.init_window()

    def init_window(self):
        """Construct the layout of the window."""
        # Create PanedWindow for split layout.
        self.main_pw = PanedWindow(self.master, sashrelief="raised", sashwidth=10, orient="vertical")

        self.editor_pw = PanedWindow(self.main_pw, sashrelief="raised", sashwidth=10, orient="horizontal")
        self.editor_frame = Frame(self.editor_pw, relief="groove", borderwidth=5)
        self.top_bar = Frame(self.editor_frame, relief="groove", borderwidth=5)
        self.open_btn = Button(self.top_bar, text="Open", command=self.open_md_file)
        self.open_btn.pack(side="left", padx=0, pady=0)
        self.save_as_btn = Button(self.top_bar, text="Save As", command=self.save_as_md_file)
        self.save_as_btn.pack(side="left", padx=0, pady=0)
        self.top_bar.pack(side="top", fill="x")
        # Top half of main section, includes text area.
        self.text_area = ScrolledText(self.editor_frame, state="normal", wrap="word", pady=2, padx=3, undo=True, width=80, height=25, font=self.myfont)
        self.text_area.pack(fill="both", expand=1)
        self.text_area.focus_set()
        default_file = Path(f"welcome.md").resolve()
        constants.cur_file = default_file
        with open(default_file, "r") as stream:
            default_text = stream.read()
        self.text_area.insert(0.0, default_text)
        self.text_area.bind("<<Modified>>", self.on_input_change)
        self.editor_frame.pack(fill="both", expand=1)

        self.preview_frame = HtmlFrame(self.editor_pw, relief="groove", borderwidth=5)
        self.editor_pw.add(self.editor_frame)
        self.editor_pw.add(self.preview_frame)
        self.editor_pw.pack(fill="both", expand=1)

        self.create_options = Frame(self.main_pw, relief="groove", borderwidth=5)
        self.some_other_text = Label(self.create_options, text="The create/convert options go here.")
        self.some_other_text.pack(fill="both", expand=1)
        self.create_options.pack(fill="both", expand=1)

        self.main_pw.add(self.editor_pw)
        self.main_pw.add(self.create_options)
        self.main_pw.pack(fill="both", expand=1)


    def on_input_change(self, event):
        """This is currently unfinished."""
        self.text_area.edit_modified(0)
        md2html = Markdown()
        markdownText = self.text_area.get("1.0", END)
        html = md2html.convert(markdownText)
        self.preview_frame.load_html(html)

    def open_md_file(self):
        """Open a file and clear/insert the text into the text_area."""
        open_filename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*")), initialdir=constants.src_dir)
        if open_filename:
            try:
                with open(open_filename, "r") as stream:
                    open_filename_contents = stream.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, open_filename_contents)
                constants.cur_file = Path(open_filename)
            except:
                messagebox.showerror(title="Error", message=f"Error Opening Selected File\n\nThe file you selected: {open_filename} can not be opened!")
    
    def save_as_md_file(self):
        """Saves the file with the given filename."""
        file_data = self.text_area.get("1.0" , END)
        save_filename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"), ("Text File", "*.txt")) , title="Save Markdown File")
        if save_filename:
            try:
                with open(save_filename, "w") as stream:
                    stream.write(file_data)
            except:
                messagebox.showerror(title="Error", message=f"Error Saving File\n\nThe file: {save_filename} can not be saved!")