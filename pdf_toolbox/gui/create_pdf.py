from utils import constants

from markdown import Markdown
from pathlib import Path
from tkinter import *
from tkinter import font
from tkinterweb import HtmlFrame
from tkinter.scrolledtext import ScrolledText
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
        # bind each key Release to the markdown checker function
        self.text_area.bind("<KeyRelease>", lambda event: self.check_markdown())
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

        self.lexer = Lexer()
        self.syntax_highlighting_tags = self.load_style("monokai")

    def on_input_change(self, event):
        """This is currently unfinished."""
        self.text_area.edit_modified(0)
        md2html = Markdown()
        markdownText = self.text_area.get("1.0", END)
        html = md2html.convert(markdownText)
        self.preview_frame.load_html(html)
        self.check_markdown()

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
            self.text_area.tag_configure(str(token), **kwargs)
            self.syntax_highlighting_tags.append(str(token))
        self.text_area.configure(bg=self.style.background_color,
                        fg=self.text_area.tag_cget("Token.Text", "foreground"),
                        selectbackground=self.style.highlight_color)
        self.text_area.tag_configure(str(Generic.StrongEmph), font=('Monospace', 10, 'bold', 'italic'))
        self.syntax_highlighting_tags.append(str(Generic.StrongEmph))
        return self.syntax_highlighting_tags    

    def check_markdown(self, start='insert linestart', end='insert lineend'):
        self.data = self.text_area.get(start, end)
        while self.data and self.data[0] == '\n':
            start = self.text_area.index('%s+1c' % start)
            self.data = self.data[1:]
        self.text_area.mark_set('range_start', start)
        # clear tags
        for t in self.syntax_highlighting_tags:
            self.text_area.tag_remove(t, start, "range_start +%ic" % len(self.data))
        # parse text
        for token, content in lex(self.data, self.lexer):
            self.text_area.mark_set("range_end", "range_start + %ic" % len(content))
            for t in token.split():
                self.text_area.tag_add(str(t), "range_start", "range_end")
            self.text_area.mark_set("range_start", "range_end")


# Extend MarkdownLexer to add markup for bold-italic
class Lexer(MarkdownLexer):
    tokens = {key: val.copy() for key, val in MarkdownLexer.tokens.items()}
    # # bold-italic fenced by '***'
    tokens['inline'].insert(2, (r'(\*\*\*[^* \n][^*\n]*\*\*\*)',
                                bygroups(Generic.StrongEmph)))
    # # bold-italic fenced by '___'
    tokens['inline'].insert(2, (r'(\_\_\_[^_ \n][^_\n]*\_\_\_)',
                                bygroups(Generic.StrongEmph)))