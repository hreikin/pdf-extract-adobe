from utils import constants
from gui import editor

from markdown import Markdown
from pathlib import Path
from tkinter import *
from tkinter import font
from tkinterweb import HtmlFrame
from pygments import lex
from pygments.lexers.markup import MarkdownLexer
from pygments.token import Generic
from pygments.lexer import bygroups
from pygments.styles import get_style_by_name

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
        # Frame for editor and toolbar.
        self.editor_frame = Frame(self.editor_pw, relief="groove", borderwidth=5)
        # Toolbar.
        self.top_bar = Frame(self.editor_frame, relief="groove", borderwidth=5)
        self.open_btn = Button(self.top_bar, text="Open")
        self.open_btn.pack(side="left", padx=0, pady=0)
        self.save_as_btn = Button(self.top_bar, text="Save As")
        self.save_as_btn.pack(side="left", padx=0, pady=0)
        self.save_btn = Button(self.top_bar, text="Save")
        self.save_btn.pack(side="left", padx=0, pady=0)
        self.top_bar.pack(side="top", fill="x")
        # Editor with line numbers.
        self.editor = editor.Editor(self.editor_frame, font=self.myfont)
        self.editor.pack(side="right", fill="both", expand=1)
        self.editor.text_area.focus_set()
        # Set Pygments syntax highlighting style.
        self.lexer = Lexer()
        self.syntax_highlighting_tags = self.load_style("monokai")
        # Open default file. This needs changing to only show the default on the 
        # first run or update, normally it should load the file that was open 
        # last time the program was running.
        default_file = Path(f"welcome.md").resolve()
        with open(default_file, "r") as stream:
            default_text = stream.read()
        self.editor.text_area.insert(0.0, default_text)
        # Applies markdown formatting to default file.
        self.check_markdown(start="1.0", end=END)
        self.editor.text_area.bind("<<Modified>>", self.on_input_change)
        # Bind each key Release to the markdown checker function
        self.editor.text_area.bind("<KeyRelease>", lambda event: self.check_markdown())
        self.editor_frame.pack(fill="both", expand=1)

        # A tkinterweb HtmlFrame for the preview window.
        self.preview_frame = HtmlFrame(self.editor_pw, relief="groove", borderwidth=5)

        # Add the editor and preview frames to the paned window.
        self.editor_pw.add(self.editor_frame)
        self.editor_pw.add(self.preview_frame)
        self.editor_pw.pack(fill="both", expand=1)

        # Options area for create/convert related functions.
        self.create_options = Frame(self.main_pw, relief="groove", borderwidth=5)
        self.some_other_text = Label(self.create_options, text="The create/convert options go here.")
        self.some_other_text.pack(fill="both", expand=1)
        self.create_options.pack(fill="both", expand=1)

        # Add the editor paned window first and then the create frame to achieve 
        # the split layout.
        self.main_pw.add(self.editor_pw)
        self.main_pw.add(self.create_options)
        self.main_pw.pack(fill="both", expand=1)


    def on_input_change(self, event):
        """When the user types update the preview and editors line numbers."""
        self.editor.text_area.edit_modified(0)
        md2html = Markdown()
        markdownText = self.editor.text_area.get("1.0", END)
        html = md2html.convert(markdownText)
        self.preview_frame.load_html(html)
        self.editor.line_nums.on_key_press()

    def load_style(self, stylename):
        self.style = get_style_by_name(stylename)
        self.syntax_highlighting_tags = []
        for token, opts in self.style.list_styles():
            kwargs = {}
            fg = opts['color']
            bg = opts['bgcolor']
            if fg:
                kwargs['foreground'] = '#' + fg
            if bg:
                kwargs['background'] = '#' + bg
            font = ('Monospace', 10) + tuple(key for key in ('bold', 'italic') if opts[key])
            kwargs['font'] = font
            kwargs['underline'] = opts['underline']
            self.editor.text_area.tag_configure(str(token), **kwargs)
            self.syntax_highlighting_tags.append(str(token))
        self.editor.text_area.configure(bg=self.style.background_color,
                        fg=self.editor.text_area.tag_cget("Token.Text", "foreground"),
                        selectbackground=self.style.highlight_color)
        self.editor.text_area.tag_configure(str(Generic.StrongEmph), font=('Monospace', 10, 'bold', 'italic'))
        self.syntax_highlighting_tags.append(str(Generic.StrongEmph))
        return self.syntax_highlighting_tags    

    def check_markdown(self, start='insert linestart', end='insert lineend'):
        self.data = self.editor.text_area.get(start, end)
        while self.data and self.data[0] == '\n':
            start = self.editor.text_area.index('%s+1c' % start)
            self.data = self.data[1:]
        self.editor.text_area.mark_set('range_start', start)
        # clear tags
        for t in self.syntax_highlighting_tags:
            self.editor.text_area.tag_remove(t, start, "range_start +%ic" % len(self.data))
        # parse text
        for token, content in lex(self.data, self.lexer):
            self.editor.text_area.mark_set("range_end", "range_start + %ic" % len(content))
            for t in token.split():
                self.editor.text_area.tag_add(str(t), "range_start", "range_end")
            self.editor.text_area.mark_set("range_start", "range_end")


# Extend MarkdownLexer to add markup for bold-italic
class Lexer(MarkdownLexer):
    tokens = {key: val.copy() for key, val in MarkdownLexer.tokens.items()}
    # # bold-italic fenced by '***'
    tokens['inline'].insert(2, (r'(\*\*\*[^* \n][^*\n]*\*\*\*)',
                                bygroups(Generic.StrongEmph)))
    # # bold-italic fenced by '___'
    tokens['inline'].insert(2, (r'(\_\_\_[^_ \n][^_\n]*\_\_\_)',
                                bygroups(Generic.StrongEmph)))