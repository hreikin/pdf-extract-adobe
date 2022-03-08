from utils import constants

from markdown import Markdown
from pathlib import Path
from tkinter import *
from tkinter import font
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
        self.myfont = font.Font(family="Ubuntu", size=14)
        self.init_window()

    def init_window(self):
        """Construct the layout of the window."""
        # Create PanedWindow for split layout.
        self.main_pw = PanedWindow(self.master, sashrelief="raised", sashwidth=10, orient="vertical")

        self.editor_pw = PanedWindow(self.main_pw, sashrelief="raised", sashwidth=10, orient="horizontal")
        self.editor_frame = Frame(self.editor_pw, relief="groove", borderwidth=5)
        self.top_bar = Frame(self.editor_frame, relief="groove", borderwidth=5)
        self.open_btn = Button(self.top_bar, text="Open")
        self.open_btn.pack(side="left", padx=0, pady=0)
        self.save_as_btn = Button(self.top_bar, text="Save As")
        self.save_as_btn.pack(side="left", padx=0, pady=0)
        self.save_btn = Button(self.top_bar, text="Save")
        self.save_btn.pack(side="left", padx=0, pady=0)
        self.top_bar.pack(side="top", fill="x")
        # Top half of main section, includes text area.
        self.text_area = ScrolledText(self.editor_frame, state="normal", wrap="word", pady=2, padx=3, undo=True, width=80, height=25, font=self.myfont)
        self.text_area.pack(fill="both", expand=1)
        self.text_area.focus_set()
        default_file = Path(f"welcome.md").resolve()
        # constants.cur_file = default_file
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