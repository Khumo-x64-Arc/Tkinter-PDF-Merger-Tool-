"""
Simple PDF Merger GUI using TKinter 

This python gui will allow for you to the following: 
-Select PDFs
- Reorder PDF's 
- Merge PDFs into a single file.

Note in prder to run this program the following is needed: 
  - pip install pydf (which is found in the requirements.txt)

  Once pydf is installed within your venv enter the following command: 
   - python pdf_merger_gui.py

"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pypdf import PdfReader, PdfWriter


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("620x420")
        self.files = []

        top = ttk.Frame(root, padding=10)
        top.pack(fill="x")
        ttk.Button(top, text="Add PDFs...", command=self.add_files).pack(side="left")
        ttk.Button(top, text="Remove", command=self.remove_selected).pack(side="left", padx=5)
        ttk.Button(top, text="Move Up", command=lambda: self.move(-1)).pack(side="left")
        ttk.Button(top, text="Move Down", command=lambda: self.move(1)).pack(side="left", padx=5)
        ttk.Button(top, text="Clear", command=self.clear).pack(side="left")

        mid = ttk.Frame(root, padding=(10, 0))
        mid.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(mid, selectmode="extended")
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(mid, orient="vertical", command=self.listbox.yview)
        scroll.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scroll.set)

        bottom = ttk.Frame(root, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Merge and Save As...", command=self.merge).pack(side="left")
        self.status = ttk.Label(bottom, text="No files selected")
        self.status.pack(side="left", padx=10)
        #end initialisation 

    #  file list handling 
    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF files", "*.pdf")]
        )
        for p in paths:
            if p not in self.files:
                self.files.append(p)
        self.refresh()

    def remove_selected(self):
        for i in reversed(self.listbox.curselection()):
            del self.files[i]
        self.refresh()
        #end remove selected

    def move(self, step):
        sel = self.listbox.curselection()
        if len(sel) != 1:
            return
        i = sel[0]
        j = i + step
        if 0 <= j < len(self.files):
            self.files[i], self.files[j] = self.files[j], self.files[i]
            self.refresh()
            self.listbox.selection_set(j)
            #end move 

    def clear(self):
        self.files = []
        self.refresh()
        #end clear 

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for i, f in enumerate(self.files, 1):
            self.listbox.insert(tk.END, f"{i}. {os.path.basename(f)}")
        self.status.config(text=f"{len(self.files)} file(s) selected")
    #end refresh 
     
    # PDF Merging 
    def merge(self):
        if len(self.files) < 2:
            messagebox.showwarning("Not enough files", "Select at least two PDFs to merge.")
            return

        out = filedialog.asksaveasfilename(
            title="Save merged PDF",
            defaultextension=".pdf",
            initialfile="merged.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not out:
            return

        writer = PdfWriter()
        try:
            for path in self.files:
                reader = PdfReader(path)
                if reader.is_encrypted:
                    reader.decrypt("")  # try empty password
                for page in reader.pages:
                    writer.add_page(page)
            with open(out, "wb") as fh:
                writer.write(fh)
        except Exception as exc:
            messagebox.showerror("Merge failed", str(exc))
            return

        self.status.config(text=f"Saved: {os.path.basename(out)}")
        messagebox.showinfo("Done", f"Merged {len(self.files)} files into:\n{out}") #MessageBox 
        # Merge function End 


if __name__ == "__main__":
    root = tk.Tk()
    PDFMergerApp(root)
    root.mainloop()
