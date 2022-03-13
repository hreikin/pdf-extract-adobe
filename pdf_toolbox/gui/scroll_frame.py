from tkinter import *
import platform

# ------------------------------------------------------------------------------
# Scrollable Frame Class
# ------------------------------------------------------------------------------
class ScrollFrame(Frame):
    # Create a frame (self)
    def __init__(self, parent, **kw):
        """Scrollable frame for an image, used to display the PDF files."""
        super().__init__(parent, **kw)
        # Place canvas on self
        self.canvas = Canvas(self, borderwidth=0)
        # Place a frame on the canvas, this frame will hold the child widgets
        self.view_port = Frame(self.canvas)
        # Place a vertical scrollbar on self
        self.vert_scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # Attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vert_scrollbar.set)
        # Pack scrollbar to right of self
        self.vert_scrollbar.pack(side="right", fill="y")
        # Horizontal scrollbar, doesn't work as expected currently.
        self.hori_scrollbar = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hori_scrollbar.set)
        self.hori_scrollbar.pack(side="bottom", fill="x")
        # Pack canvas to left of self and expand to fill.
        self.canvas.pack(side="left", fill="both", expand=True)
        # Add view port frame to canvas.
        self.canvas_window = self.canvas.create_window(
            (4,4), 
            window=self.view_port, 
            anchor="nw", 
            tags="self.view_port"
            )
        # Bind an event whenever the size of the view_port frame changes.
        self.view_port.bind("<Configure>", self.on_frame_configure)
        # Bind an event whenever the size of the canvas frame changes.
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        # Bind wheel events when the cursor enters the control.
        self.view_port.bind('<Enter>', self.on_enter)
        # Unbind wheel events when the cursorl leaves the control.
        self.view_port.bind('<Leave>', self.on_leave)
        # Perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize.
        self.on_frame_configure(None)

    def on_frame_configure(self, event):                                              
        """Reset the scroll region to encompass the inner frame"""
        # Whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        # Whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)

    def on_mouse_wheel(self, event):
        """Cross platform scroll wheel event."""
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def on_enter(self, event):
        """Bind wheel events when the cursor enters the control."""
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_leave(self, event):
        """Unbind wheel events when the cursorl leaves the control."""
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
