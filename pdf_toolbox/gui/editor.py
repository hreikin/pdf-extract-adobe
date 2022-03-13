from tkinter import *

class Editor(Frame):
    def __init__(self, master, **kwargs):
        """Two Text widgets and a Scrollbar in a Frame."""
        Frame.__init__(self, master) # no need for super

        # Creating the widgets
        self.text_area = Text(self, state="normal", wrap="none", pady=2, padx=3, undo=True, width=100, height=25)
        self.line_nums = LineNumbers(self, self.text_area, width=1)
        self.line_nums.pack(side="left", fill="y")
        self.text_area.pack(side="left", fill="both", expand=1)
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side="right", fill="y")


        # Changing the settings to make the scrolling work
        self.scrollbar['command'] = self.on_scrollbar
        self.line_nums['yscrollcommand'] = self.on_textscroll
        self.text_area['yscrollcommand'] = self.on_textscroll

    def on_scrollbar(self, *args):
        '''Scrolls both text widgets when the scrollbar is moved'''
        self.line_nums.yview(*args)
        self.text_area.yview(*args)

    def on_textscroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel
        is moved on a text widget'''
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])


class LineNumbers(Text):
    def __init__(self, master, text_widget, **kwargs):
        """A class to handle automatically updating the editors line numbers."""
        super().__init__(master, **kwargs)

        self.text_widget = text_widget

        self.insert(1.0, '1')
        self.configure(state='disabled')

    def on_key_press(self, event=None):
        """Checks each key press to update the line numbers if on a new line."""
        final_index = str(self.text_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(no + 1) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')
