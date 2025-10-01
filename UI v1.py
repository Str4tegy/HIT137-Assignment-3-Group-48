import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class BaseWindow(tk.Tk):
    """Base window class settings""" # Docstring
    def __init__(self):
        super().__init__()
        self.title("HF AI Tkinter GUI")
        self.geometry("1900x1080")
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self) # Create notebook for navigating pages
        self.tab_main = ttk.Frame(self.notebook) # Notebook tabs
        self.tab_info = ttk.Frame(self.notebook) 
        self.tab_oop = ttk.Frame(self.notebook) 

    def layout_widgets(self):
        self.notebook.add(self.tab_main, text="Main")
        self.notebook.add(self.tab_info, text="Model Info")
        self.notebook.add(self.tab_oop, text="OOP Explanation")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

class AIIntegratorWindow(BaseWindow):
    """Window with UI elements""" # Docstring
    def __init__(self):
        super().__init__()
        self.build_main_tab()
        self.build_info_tab()
        self.build_oop_tab()

    def build_main_tab(self):
        left = ttk.Frame(self.tab_main, padding=8) # Left panel
        left.pack(side=tk.LEFT, fill=tk.Y)

        controls = ttk.Frame(left, padding=(0, 12)) # Model control buttons
        controls.pack(fill=tk.X)
        ttk.Button(controls, text="Run Model").pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(controls, text="Clear Output").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(6, 0))

        self.input_frame = ttk.Frame(left) # Input field
        self.input_frame.pack(fill=tk.X, pady=(12, 0))
        ttk.Label(self.input_frame, text="Text Input:").pack(anchor="w", pady=(0, 4))
        self.text_entry = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
        self.text_entry.pack(fill=tk.X)

        ttk.Label(left, text="Select Model:").pack(anchor="w", pady=(12, 4)) # AI selection
        self.model_var = tk.StringVar(value="texttoimg")
        ttk.Radiobutton(left, text="Text-to-Image", variable=self.model_var, value="texttoimg").pack(anchor="w")
        ttk.Radiobutton(left, text="Image-to-Text", variable=self.model_var, value="imgtotext").pack(anchor="w")

        ttk.Label(left, text="Input Type:").pack(anchor="w", pady=(12, 4)) # Input selection
        self.input_type_var = tk.StringVar(value="text")
        ttk.Radiobutton(left, text="Text", variable=self.input_type_var, value="text", command=self.on_input_type_change).pack(anchor="w")
        ttk.Radiobutton(left, text="Image File", variable=self.input_type_var, value="image", command=self.on_input_type_change).pack(anchor="w")

        right = ttk.Frame(self.tab_main, padding=8) # Output field
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(right, text="Model Output:").pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(right, height=25, wrap=tk.WORD)
        self.output_text.pack(fill=tk.X)
        ttk.Label(right, text="Visual Output:").pack(anchor="w", pady=(8, 0))
        self.preview_canvas = tk.Canvas(right, height=500, bg="#ffffff")
        self.preview_canvas.pack(fill=tk.X)

    def build_info_tab(self):
        ttk.Label(self.tab_info, text="Model Information", font=(None, 12, "bold")).pack(anchor="w", padx=12, pady=12)
        self.model_info_text = scrolledtext.ScrolledText(self.tab_info, wrap=tk.WORD, height=20)
        self.model_info_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.model_info_text.insert(tk.END, "Whats your favourite song, Steven? steven here! hello steven...")
        self.model_info_text.configure(state=tk.DISABLED)

    def build_oop_tab(self):
        ttk.Label(self.tab_oop, text="OOP Concepts Used", font=(None, 12, "bold")).pack(anchor="w", padx=12, pady=12)
        self.oop_text = scrolledtext.ScrolledText(self.tab_oop, wrap=tk.WORD, height=20)
        self.oop_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        explanation = ("The OOP concepts demonstrated in this GUI:")
        self.oop_text.insert(tk.END, explanation)
        self.oop_text.configure(state=tk.DISABLED)

    def on_input_type_change(self):
        for w in self.input_frame.winfo_children():
            w.destroy()
        if self.input_type_var.get() == "text":
            ttk.Label(self.input_frame, text="Text Input:").pack(anchor="w", pady=(0, 4))
            self.text_entry = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
            self.text_entry.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(self.input_frame, text="[File selection]").pack(anchor="w")

def main():
    app = AIIntegratorWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
