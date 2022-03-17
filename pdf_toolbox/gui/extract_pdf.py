from download.spiders import download_pdfs
from utils import constants
from gui import scroll_frame
from extraction import adobe_json

import fitz, logging, multiprocessing
# from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import font
# from tkinter.ttk import Progressbar
from functools import partial

class ExtractPDF(ttk.Frame):
    def __init__(self, master=None):
        """Create a subclass of Frame for our window element. Initialize and set 
        the variable defaults."""
        ttk.Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Ubuntu", size=16)
        self.zoom_on = False
        self.init_window()

    def init_window(self):
        """Construct the layout of the window element."""
        # Create PanedWindow for split layout.
        self.pw = ttk.PanedWindow(self.master, orient="horizontal")
        # Extraction options frame (left side) to hold all options.
        self.extract_options = ttk.Frame(self.pw)
        # Scrapy options. (Download/Scrape PDF Files)
        self.scrapy_download = ttk.Frame(self.extract_options)
        self.scrapy_download_top = ttk.Frame(self.scrapy_download)
        self.scrapy_download_top.pack(fill="both", expand=1)
        self.scrapy_download_middle = ttk.Frame(self.scrapy_download)
        self.scrapy_download_middle.pack(fill="both", expand=1)
        self.scrapy_download_left = ttk.Frame(self.scrapy_download_middle)
        self.scrapy_download_left.pack(side="left", fill="both")
        self.scrapy_download_right = ttk.Frame(self.scrapy_download_middle)
        self.scrapy_download_right.pack(side="right", fill="both")
        self.scrapy_download_bottom = ttk.Frame(self.scrapy_download)
        self.scrapy_download_bottom.pack(fill="both", expand=1)
        self.scrapy_download_lbl = ttk.Label(self.scrapy_download_top, text="Scrape PDF Files From Website.")
        self.scrapy_download_lbl.pack(side="left", fill="x")
        self.scrapy_download_url_ent_val = ttk.StringVar()
        self.scrapy_download_url_ent_lbl = ttk.Label(self.scrapy_download_left, text="Enter a URL, e.g. https://example.com/")
        self.scrapy_download_url_ent_lbl.pack(fill="x")
        self.scrapy_download_url_ent = ttk.Entry(self.scrapy_download_left, width=40, textvariable=self.scrapy_download_url_ent_val)
        self.scrapy_download_url_ent.pack(fill="x", expand=1)
        self.scrapy_download_domain_ent_val = ttk.StringVar()
        self.scrapy_download_domain_ent_lbl = ttk.Label(self.scrapy_download_right, text="Enter a domain, e.g. example.com/")
        self.scrapy_download_domain_ent_lbl.pack(fill="x")
        self.scrapy_download_domain_ent = ttk.Entry(self.scrapy_download_right, width=40, textvariable=self.scrapy_download_domain_ent_val)
        self.scrapy_download_domain_ent.pack(fill="x", expand=1)
        self.scrapy_download_progress_bar = ttk.Progressbar(self.scrapy_download_bottom, mode="indeterminate", bootstyle="success")
        self.scrapy_download_progress_bar.pack(fill="x", expand=1)
        self.scrapy_download_btn = ttk.Button(self.scrapy_download_bottom, text="Start Crawler", width=20, command=self.start_crawler) 
        self.scrapy_download_btn.pack(fill="x", expand=1)
        self.scrapy_download.pack(fill="both")
        # Adobe API options.
        self.adobe_api = ttk.Frame(self.extract_options)
        self.adobe_api_top = ttk.Frame(self.adobe_api)
        self.adobe_api_top.pack(fill="both", expand=1)
        self.adobe_api_middle = ttk.Frame(self.adobe_api)
        self.adobe_api_middle.pack(fill="both", expand=1)
        self.adobe_api_bottom = ttk.Frame(self.adobe_api)
        self.adobe_api_bottom.pack(fill="both", expand=1)
        self.adobe_api_left = ttk.Frame(self.adobe_api_middle)
        self.adobe_api_left.pack(side="left", fill="both")
        self.adobe_api_right = ttk.Frame(self.adobe_api_middle)
        self.adobe_api_right.pack(side="right", fill="both")
        self.adobe_api_lbl = ttk.Label(self.adobe_api_top, text="Adobe PDF Extract API")
        self.adobe_api_lbl.pack(side="left", fill="x")
        self.adobe_api_ent_multi_val = ttk.StringVar()
        self.adobe_api_ent_multi = ttk.Entry(self.adobe_api_left, width=60, textvariable=self.adobe_api_ent_multi_val)
        self.adobe_api_ent_multi.pack(fill="x", expand=1)
        self.adobe_api_btn_multi = ttk.Button(self.adobe_api_right, text="Select Folder",width=20, command=self.adobe_browse_folder)
        self.adobe_api_btn_multi.pack(fill="x")
        self.adobe_api_ent_single_val = ttk.StringVar()
        self.adobe_api_ent_single = ttk.Entry(self.adobe_api_left, width=60, textvariable=self.adobe_api_ent_single_val)
        self.adobe_api_ent_single.pack(fill="x", expand=1)
        self.adobe_api_btn_single = ttk.Button(self.adobe_api_right, text="Select File",width=20, command=self.adobe_browse_file)
        self.adobe_api_btn_single.pack(fill="x")
        self.adobe_api_progress_bar = ttk.Progressbar(self.adobe_api_bottom, mode="indeterminate", bootstyle="success")
        self.adobe_api_progress_bar.pack(fill="x", expand=1)
        self.adobe_api_btn_send = ttk.Button(self.adobe_api_bottom, text="Send Request(s)", command=self.generate_adobe_request)
        self.adobe_api_btn_send.pack(fill="x", expand=1)
        self.adobe_api.pack(fill="both")
        # PyMuPDF/OCR options. (Auto Extraction)
        self.auto_extract = ttk.Frame(self.extract_options)
        self.auto_some_text = ttk.Label(self.auto_extract, text="Auto Content Extraction.")
        self.auto_some_text.pack(fill="x", expand=1)
        self.auto_extract.pack(fill="both", expand=1)
        # PyMuPDF/OCR options. (Manual Extraction)
        self.manual_extract = ttk.Frame(self.extract_options)
        self.manual_some_text = ttk.Label(self.manual_extract, text="Manual Content Extraction.")
        self.manual_some_text.pack(fill="x", expand=1)
        self.manual_extract.pack(fill="both", expand=1)
        # PDF preview area (right side) with controls for navigation, zoom, etc 
        # at the top and the scrollable PDF preview below.
        self.preview_area = ttk.Frame(self.pw)
        # Controls for navigation, zoom, etc.
        self.top_bar = ttk.Frame(self.preview_area)
        self.open_btn = ttk.Button(self.top_bar, text="Open", command=self.open_extract)
        self.open_btn.pack(side="left", padx=0, pady=0)
        self.next_btn = ttk.Button(self.top_bar, text="Next", state="disabled", command=self.next_page)
        self.next_btn.pack(side="left", padx=0, pady=0)
        self.prev_btn = ttk.Button(self.top_bar, text="Prev", state="disabled", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=0, pady=0)
        self.zoom_btn = ttk.Button(self.top_bar, text="Zoom", state="disabled", command=self.toggle_zoom)
        self.zoom_btn.pack(side="left", padx=0, pady=0)
        self.top_bar.pack(side="top", fill="x")
        # Scrollable PDF preview area.
        self.pdf_preview = scroll_frame.ScrollFrame(self.preview_area)
        self.pdf_page_img = ttk.Label(self.pdf_preview.view_port, text="Open a PDF to view or manually extract content.", image=None)
        self.pdf_page_img.pack(side="left", fill="both", expand=1)
        self.pdf_preview.pack(side="bottom", fill="both", expand=1)
        # Add the Extraction and Preview areas to the PanedWindow.
        self.pw.add(self.extract_options)
        self.pw.add(self.preview_area)
        self.pw.pack(fill="both", expand=True)

# ------------------------------------------------------------------------------
# Open the PDF file to view/edit/extract from.
# ------------------------------------------------------------------------------
    def open_extract(self):
        """Open a file dialog and ask for an input file for the previewer to load 
        and display."""
        self.fname = filedialog.askopenfile(
            title="PDF Toolbox Document Browser", 
            initialdir=constants.pdf_dir, 
            filetypes=(
                ("PDF Files", "*.pdf"), 
                ("XPS Files", "*.*xps"), 
                ("Epub Files", "*.epub"), 
                ("Fiction Books", "*.fb2"), 
                ("Comic Books", "*.cbz"), 
                ("HTML", "*.htm*")
                )
            )
        if not self.fname:
            messagebox.showerror(title="Cancelling.", message="No file chosen.")
            return
        self.doc = fitz.open(self.fname)
        self.page_count = len(self.doc)
        # Allocate storage for page display lists.
        self.dlist_tab = [None] * self.page_count
        self.max_width = self.pdf_preview.winfo_screenwidth() - 20
        self.max_height = self.pdf_preview.winfo_screenheight() - 150
        self.max_size = (self.max_width, self.max_height)
        self.cur_page = 0
        # If zoom is on, display twice as large.
        if self.zoom_on == False:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.max_size
                )
        elif self.zoom_on == True:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.zoom_max_size
                )
        self.pdf_page_data = ttk.PhotoImage(data=self.data)
        self.pdf_page_img.configure(image=self.pdf_page_data, text=None)
        # Set button states to normal after file has been loaded.
        self.next_btn.configure(state="normal")
        self.prev_btn.configure(state="normal")
        self.zoom_btn.configure(state="normal")

# ------------------------------------------------------------------------------
# Read the page data.
# ------------------------------------------------------------------------------
    def get_page(self, pno, max_size=None):
        """Return a tkinter.PhotoImage or a PNG image for a document page number.
        
        :arg int pno: 0-based page number
        :arg max_size: (width, height) of available image area"""
        # Get display list of page number.
        self.dlist = self.dlist_tab[pno]
        # Create if not yet there.
        if not self.dlist:
            self.dlist_tab[pno] = self.doc[pno].get_displaylist()
            self.dlist = self.dlist_tab[pno]
        # The page rectangle.
        self.r = self.dlist.rect
        self.clip = self.r
        # Ensure image fits screen: exploit, but do not exceed width or height.
        self.zoom_0 = 1
        if max_size:
            self.zoom_0 = min(1, max_size[0] / self.r.width, max_size[1] / self.r.height)
            if self.zoom_0 == 1:
                self.zoom_0 = min(max_size[0] / self.r.width, max_size[1] / self.r.height)
        self.mat_0 = fitz.Matrix(self.zoom_0, self.zoom_0)
        self.pix = self.dlist.get_pixmap(matrix=self.mat_0, alpha=False)
        # Make PPM image from pixmap for tkinter.
        self.img = self.pix.tobytes("ppm")
        # Return image and clip position.
        return self.img, self.clip.tl

    def next_page(self):
        """When called, load the next PDF page."""
        self.cur_page += 1
        # Sanitize page number and wrap around.
        while self.cur_page >= self.page_count:
            self.cur_page -= self.page_count
        # Pages < 0 are valid but look bad.
        while self.cur_page < 0:
            self.cur_page += self.page_count
        if self.zoom_on == False:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.max_size
                )
        elif self.zoom_on == True:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.zoom_max_size
                )
        self.pdf_page_data = ttk.PhotoImage(data=self.data)
        self.pdf_page_img.configure(image=self.pdf_page_data, text=None)

    def prev_page(self):
        """When called, load the previous PDF page."""
        self.cur_page -= 1
        # Sanitize page number and wrap around.
        while self.cur_page >= self.page_count:
            self.cur_page -= self.page_count
        # Pages < 0 are valid but look bad.
        while self.cur_page < 0:
            self.cur_page += self.page_count
        if self.zoom_on == False:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.max_size
                )
        elif self.zoom_on == True:
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.zoom_max_size
                )
        self.pdf_page_data = ttk.PhotoImage(data=self.data)
        self.pdf_page_img.configure(image=self.pdf_page_data, text=None)

    def toggle_zoom(self):
        """Toggle zoom on or off. When zoomed pages a displayed at twice their 
        normal size."""
        if self.zoom_on == False:
            self.zoom_on = True
            self.zoom_width = self.max_width * 2
            self.zoom_height = self.max_height * 2
            self.zoom_max_size = (self.zoom_width, self.zoom_height)
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.zoom_max_size
                )
        elif self.zoom_on == True:
            self.zoom_on = False
            self.data, self.clip_pos = self.get_page(
                self.cur_page,
                max_size=self.max_size
                )
        self.pdf_page_data = ttk.PhotoImage(data=self.data)
        self.pdf_page_img.configure(image=self.pdf_page_data, text=None)

    def adobe_browse_folder(self):
        """Browse for a folder and set the Entry field to the chosen folder."""
        pdf_dir = filedialog.askdirectory(title="PDF Toolbox Document Browser", initialdir=constants.src_dir)
        self.adobe_api_ent_multi_val.set(pdf_dir)
        self.adobe_api_ent_single_val.set("")

    def adobe_browse_file(self):
        """Browse for a file and set the Entry field to the chosen file."""
        pdf_file = filedialog.askopenfilename(
            title="PDF Toolbox Document Browser", 
            initialdir=constants.src_dir, 
            filetypes=(
                ("PDF Files", "*.pdf"), 
                ("XPS Files", "*.*xps"), 
                ("Epub Files", "*.epub"), 
                ("Fiction Books", "*.fb2"), 
                ("Comic Books", "*.cbz"), 
                ("HTML", "*.htm*")
                )
            )
        self.adobe_api_ent_single_val.set(pdf_file)
        self.adobe_api_ent_multi_val.set("")

    def generate_adobe_request(self):
        """Use multiprocessing to create Adobe API request."""
        if self.adobe_api_ent_multi_val.get() == "" and self.adobe_api_ent_single_val.get() == "":
            return
        if self.adobe_api_ent_multi_val.get() == "":
            self.send_adobe_request = partial(adobe_json.extract_pdf_adobe, source_path=self.adobe_api_ent_single_val.get())
            self.adobe_process = multiprocessing.Process(target=self.send_adobe_request)
            self.adobe_process.start()
            self.adobe_api_progress_bar.start()
            self.after(80, self.check_process, self.adobe_process, self.adobe_api_progress_bar)
            # adobe_process.join()
        elif self.adobe_api_ent_single_val.get() == "":
            self.send_adobe_request = partial(adobe_json.extract_pdf_adobe, source_path=self.adobe_api_ent_multi_val.get())
            self.adobe_process = multiprocessing.Process(target=self.send_adobe_request)
            self.adobe_process.start()
            self.after(80, self.check_process, self.adobe_process, self.adobe_api_progress_bar)

    def start_crawler(self):
        """Use multiprocessing to start the crawler."""
        if self.scrapy_download_domain_ent_val.get == "" or self.scrapy_download_url_ent_val.get() == "":
            return
        self.crawler_partial = partial(download_pdfs.run_spider, start_url=self.scrapy_download_url_ent_val.get(), allowed_domain=self.scrapy_download_domain_ent_val.get())
        self.crawler_process = multiprocessing.Process(target=self.crawler_partial)
        self.crawler_process.start()
        self.scrapy_download_progress_bar.start()
        self.after(80, self.check_process, self.crawler_process, self.scrapy_download_progress_bar)

    def check_process(self, process, progress_bar):
        """Checks if process has finished, if it has then it joins the process 
        and stops the progress bar."""
        if (process.is_alive()):
            self.after(80, self.check_process, process, progress_bar)
            return
        else:
            try:
                process.join()
                progress_bar.stop()
                logging.info("Process complete, exiting.")
            except:
                logging.exception("ERROR: Unable to stop process.")

# ------------------------------------------------------------------------------
# Run standalone.
# ------------------------------------------------------------------------------

# mainwindow = Tk()
# preview = ExtractPDF(mainwindow)
# preview.mainloop()
