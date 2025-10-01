#Importing the AI model and setting it up in the GUI
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import font
from diffusers import StableDiffusionPipeline
from transformers import CLIPTextModel
from torch import Generator
import requests
from PIL import Image, ImageTk
from transformers import BlipProcessor, BlipForConditionalGeneration
import threading

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

file_path = "No file selected."
aimodel = "texttoimg"
textoutput=''

btn_switch = 1

#Creates the window the GUI is located in
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

#This section handles the integration of the AI into the pre-existing window
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

        def image_to_text(file_path): #This function grabs an image, summons the AI to analyse the image and then outputs a description
            self.preview_area.configure(state=tk.NORMAL)
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.configure(state=tk.DISABLED)
            acc_txt.pack_forget()
            global textoutput

            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            urlcheck = 'http'
            if urlcheck in file_path:
                print("verify")
                raw_image = Image.open(requests.get(file_path, stream=True).raw).convert('RGB')
            else:
                raw_image = Image.open(file_path).convert('RGB')
            text = "An image of"
            inputs = processor(raw_image, text, return_tensors="pt")
            out = model.generate(**inputs)
            textoutput=(processor.decode(out[0], skip_special_tokens=True))

            self.preview_area.configure(state=tk.NORMAL)
            self.preview_area.insert(tk.END, textoutput)
            self.preview_area.configure(state=tk.DISABLED)

            loading_txt.pack_forget()
            
        def text_to_image(prompt): #This function grabs the text, summons the AI to generate and image and then outputs the image
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)  
            self.output_text.configure(state=tk.DISABLED)
            device = 'cuda'

            generator = Generator(device=device)
            generator.manual_seed(42)
            
            clip_backbone = "openai/clip-vit-large-patch14"
            sd_model_id = "CompVis/stable-diffusion-v1-4"

            safeclip_text_model = CLIPTextModel.from_pretrained("aimagelab/safeclip_vit-l_14")
            safe_pipeline = StableDiffusionPipeline.from_pretrained(sd_model_id, safety_checker=None)

            safe_pipeline.text_encoder = safeclip_text_model
            safe_pipeline = safe_pipeline.to(device)

            gen_image = safe_pipeline(prompt=prompt, generator=generator).images[0]

            # Convert to Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(gen_image)

            # Show in preview_area
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.image_create(tk.END, image=tk_image)
            self.output_text.configure(state=tk.DISABLED)

            # Keep a reference so it’s not garbage collected
            self.output_text.image = tk_image

            loading_txt.pack_forget()

        def run_model():
            # Show loading label immediately
            loading_txt.pack(expand=True)
            self.update_idletasks()

            def task():
                if self.input_type_var.get() == 'texttoimg':
                    textprompt = self.text_entry.get('1.0', tk.END)
                    text_to_image(textprompt)
                # elif self.input_type_var.get() == 'imgtotext' and file_path != "":
                #     image_to_text(file_path)
                elif self.input_type_var.get() == 'imgtotext' and file_path != "":
                    image_to_text(file_path)

                # Hide the loading label on the main thread
                self.after(0, loading_txt.pack_forget)

            # Start the thread so GUI doesn’t freeze
            threading.Thread(target=task, daemon=True).start()

        def clear_outputs():
            #This is for when the user wants to clear the AI
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)  
            self.output_text.configure(state=tk.DISABLED)

            self.preview_area.configure(state=tk.NORMAL)
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.configure(state=tk.DISABLED)


        #This handles the buttons inside the GUI
        controls = ttk.Frame(left, padding=(0, 12)) # Model control buttons
        controls.pack(fill=tk.X)
        tk.Button(controls, text="Run Model", command=run_model, bg="#75ff75").pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(controls, text="Clear Outputs", bg="#ff6767", command=clear_outputs).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(6, 0))

        self.input_frame = ttk.Frame(left) # Input field
        self.input_frame.pack(fill=tk.X, pady=(12, 0))
        ttk.Label(self.input_frame, text="Text Input:").pack(anchor="w", pady=(0, 4))
        self.text_entry = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
        self.text_entry.pack(fill=tk.X)

        ttk.Label(left, text="Input Type:").pack(anchor="w", pady=(12, 4)) # Input selection
        self.input_type_var = tk.StringVar(value="text")
        ttk.Radiobutton(left, text="Text-to-Image", variable=self.input_type_var, value="texttoimg", command=self.on_input_type_change).pack(anchor="w")
        ttk.Radiobutton(left, text="Image-to-Text", variable=self.input_type_var, value="imgtotext", command=self.on_input_type_change).pack(anchor="w")
        # Turns "texttoimg" button on once
        global btn_switch
        while btn_switch == 1:
            self.input_type_var.set("texttoimg")
            btn_switch = 0

        loading_txt = ttk.Label(left, text="Loading output, this may take some time...")

        right = tk.Frame(self.tab_main, pady=8, padx=8) # Output field
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(right, text="Visual Output:").pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(right, height=25, wrap=tk.WORD)
        self.output_text.pack(fill=tk.X)
        self.output_text.insert(tk.END, textoutput)
        self.output_text.configure(state=tk.DISABLED)

        ttk.Label(right, text="Text Output:").pack(anchor="w", pady=(8, 0))
        self.preview_area = scrolledtext.ScrolledText(right, height=500, wrap=tk.WORD)
        self.preview_area.pack(fill="both")
        self.preview_area.insert(tk.END, textoutput)
        self.preview_area.configure(state=tk.DISABLED)


    #This is for the model information tab
    def build_info_tab(self):
        ttk.Label(self.tab_info, text="Model Information", font=(None, 12, "bold")).pack(anchor="w", padx=12, pady=12)
        self.model_info_text = scrolledtext.ScrolledText(self.tab_info, wrap=tk.WORD, height=20)
        self.model_info_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.model_info_text.insert(tk.END, "The artificial intelligence model which was selected to be utilised in the code is referred to as Safe-CLIP. This is a multimodal model which is able to create AI generated images, as well as being able to analyse and describe images. This has several applications in multimodal circumstances, where it is beneficial to generate text from a pre-existing image, or generating an image from pre-existing text. This model also has NSFW (Not Safe For Work) filters, which improve the applicability of this model. Since it is able to effectively prevent the generation of content which is considered offensive or inappropriate, this AI model is able to be implemented in professional circumstances.")
        self.model_info_text.configure(state=tk.DISABLED)

    #This is for the OOP concepts used tab
    def build_oop_tab(self):
        ttk.Label(self.tab_oop, text="OOP Concepts Used", font=(None, 12, "bold")).pack(anchor="w", padx=12, pady=12)
        self.oop_text = scrolledtext.ScrolledText(self.tab_oop, wrap=tk.WORD, height=20)
        self.oop_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        explanation = ("Object oriented programming was significantly utilised in the code. For example, encapsulation was used to optimise the code, which involves the process of combining data within classes together. For the purpose of avoiding conflicting data in the GUI, some data was made to be private, meaning it was able to be contained within certain sections of the code. This reduced the need for redundant code, making the code easier to work with and reducing the resources required to run the code. Moreover, method overriding was utilised throughout the code. This involves some of the parameters of a parent class being redefined for a subclass. As a result, some of the properties of a parent class can be utilised in the subclass, meaning the subclass does not need to be defined from scratch. In this code, it was utilised to for different types of windows throughout the GUI, and it reduced redundancy in the code. Therefore, less resources were required to run the code, and the code was easier to manipulate.")
        self.oop_text.insert(tk.END, explanation)
        self.oop_text.configure(state=tk.DISABLED)

    def on_input_type_change(self):
        def select_file():
            global file_path

            temp_file_path = filedialog.askopenfilename(
                title="Select a file",
                initialdir="/",  # Optional: starting directory
                filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")) 
            )
            print(file_path)
            if ".png" in temp_file_path or ".jpg" in temp_file_path:
                acc_txt.pack(anchor="n", pady=(4, 4))
                file_path = temp_file_path
                print(file_path)
            else:
                file_path = ''
            return
        
        for w in self.input_frame.winfo_children():
            w.destroy()
        if self.input_type_var.get() == "texttoimg":
            ttk.Label(self.input_frame, text="Text Input:").pack(anchor="w", pady=(0, 4))
            self.text_entry = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
            self.text_entry.pack(fill=tk.BOTH, expand=True)
        else:
            tk.Button(self.input_frame, text="[File selection]", command=select_file, width=93, height=9, bg="#e6e6e6").pack(fill=tk.BOTH, expand=True)
            italic_font = font.Font(family="Calibri", size=12, slant="italic")
            global acc_txt
            acc_txt = tk.Label(self.input_frame, text="File Accepted, Run the Model", font=italic_font)
            
            

def main():
    app = AIIntegratorWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
