import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
from gauss_iterated_crypto import GaussCircleCrypto
import time

class appGaussCircleIterated:
    
    def __init__(self):
        self.root = tk.Tk()
        self.state = tk.StringVar()
        
        # Set the size of the window
        window_width = 1000
        window_height = 750

        # Center the window on the screen
        self.center_window(self.root, window_width, window_height)
        self.root.title("Gauss Iterated Map - Group 01")

        label = tk.Label(self.root, text="Gauss-Circle Iterated Map, developed by Group-01.", font=('Arial', 18))
        label.pack(padx=20, pady=20)

        # Create a frame to contain the Input and Output
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        encrypt_button = tk.Radiobutton(frame, text="Encrypt", variable=self.state, value="encrypt", font=('Arial', 12))
        encrypt_button.pack(anchor=tk.W)

        decrypt_button = tk.Radiobutton(frame, text="Decrypt", variable=self.state, value="decrypt", font=('Arial', 12))
        decrypt_button.pack(anchor=tk.W)

        self.state.trace('w', self.update_frame)  # Call update_frame when state changes

        # Frame below for different components based on state
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(padx=20, pady=20)

        self.bottom_frame.columnconfigure(0, minsize=450)
        self.bottom_frame.columnconfigure(1, minsize=150)
        self.bottom_frame.columnconfigure(2, minsize=450)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def update_frame(self, *_):
        # Clear the existing widgets in bottom_frame
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()

        # Add appropriate buttons based on state
        if self.state.get() == "encrypt":
            # Add widgets for encryption
            self.add_encryption_widgets()

        elif self.state.get() == "decrypt":
            self.add_decryption_widgets()
    
    def add_encryption_widgets(self):
        self.select_button_encryption = tk.Button(self.bottom_frame, text="Select Image", command=self.select_image)
        self.select_button_encryption.grid(column = 0, row=0, padx=10, pady=10)

        # Re-add image preview widget
        self.image_preview = tk.Label(self.bottom_frame)
        self.image_preview.grid(column=0, row=1, padx=20, pady=20)

        self.start_encrypt_button = tk.Button(self.bottom_frame, text="Encrypt", command=self.encrypt_image)
        self.start_encrypt_button.grid(column = 1, row=1, padx=10, pady=10)

        self.encryption_duration_label = tk.Label(self.bottom_frame, text="Encryption Duration: ")
        self.encryption_duration_label.grid(column=1, row=2, padx=10, pady=10)

        self.encrypt_result = tk.Label(self.bottom_frame, text="Encryption Image Result")
        self.encrypt_result.grid(column = 2, row=0, padx=10, pady=10)

        # In the column 2 row 1 show the result of encryption from GaussCircleCrypto
        # Re-add image preview widget
        self.encrypted_image_preview = tk.Label(self.bottom_frame)
        self.encrypted_image_preview.grid(column=2, row=1, padx=20, pady=20)

        self.save_encrypted_image_button = tk.Button(self.bottom_frame, text="Save Encrypted Image", command=self.save_encrypted_image)
        self.save_encrypted_image_button.grid(column=2, row=2, padx=10, pady=10)

        self.save_keyfile_button = tk.Button(self.bottom_frame, text="Save Key File", command=self.save_keyfile)
        self.save_keyfile_button.grid(column=2, row=3, padx=10, pady=10)
    
    def add_decryption_widgets(self):
        self.select_button_decryption = tk.Button(self.bottom_frame, text="Select Image", command=self.select_image)
        self.select_button_decryption.grid(column = 0, row=0, padx=10, pady=10)

        # Re-add image preview widget
        self.image_preview = tk.Label(self.bottom_frame)
        self.image_preview.grid(column=0, row=1, padx=20, pady=20)

        self.select_key = tk.Button(self.bottom_frame, text="Select Key File", command=self.select_key)
        self.select_key.grid(column = 0, row=2, padx=10, pady=10)
        
        self.start_decrypt_button = tk.Button(self.bottom_frame, text="Decrypt", command=self.decrypt_image)
        self.start_decrypt_button.grid(column = 1, row=1, padx=10, pady=10)
        
        self.decryption_duration_label = tk.Label(self.bottom_frame, text="Decryption Duration: ")
        self.decryption_duration_label.grid(column=1, row=2, padx=10, pady=10)

        self.decrypt_result = tk.Label(self.bottom_frame, text="Decryption Image Result")
        self.decrypt_result.grid(column = 2, row=0, padx=10, pady=10)

        # In the column 2 row 1 show the result of encryption from GaussCircleCrypto
        # Re-add image preview widget
        self.decrypted_image_preview = tk.Label(self.bottom_frame)
        self.decrypted_image_preview.grid(column=2, row=1, padx=20, pady=20)

        self.save_decrypted_image_button = tk.Button(self.bottom_frame, text="Save Decrypted Image", command=self.save_decrypted_image)
        self.save_decrypted_image_button.grid(column=2, row=2, padx=10, pady=10)

    def select_image(self):
        self.filepath_img = filedialog.askopenfilename(title="Select Image File", filetypes=(("Image files", "*.jpg *.png"), ("All files", "*.*")))
        if self.filepath_img:
            self.show_image_preview()

    def select_key(self):
        self.filepath_key = filedialog.askopenfilename(title="Select Key File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if self.filepath_key:
            folder, filename = os.path.split(self.filepath_key)
            short_path = os.path.join("..", filename)  # Assuming the last folder is displayed
            self.keyfile = tk.Label(self.bottom_frame, text=short_path)
            self.keyfile.grid(column=0, row=3, padx=10, pady=10)

    def show_image_preview(self):
        # Open the image file
        image = Image.open(self.filepath_img)
        # Resize the image to fit the label
        image = image.resize((300, 300))
        # Convert image for Tkinter
        tk_image = ImageTk.PhotoImage(image)
        # Update the label with the new image
        self.image_preview.configure(image=tk_image)
        self.image_preview.image = tk_image  # Keep a reference to avoid garbage collection

    def encrypt_image(self):
        # Check if an image and key file are selected
        if not hasattr(self, 'image_preview'):
            messagebox.showerror("Error", "Please select an image and a key file.")
            return
        
        start_time_encryption = time.time()
        crypto = GaussCircleCrypto()
        self.encryption_key = crypto.gauss_iterated_map()
        self.encrypted_image = crypto.encrypt(self.filepath_img, self.encryption_key)
        end_time_encryption = time.time()
        encryption_duration = end_time_encryption - start_time_encryption
        if self.encrypted_image:
            self.show_encrypted_image_preview()
            self.encryption_duration_label.config(text=f"Encryption Duration: {encryption_duration:.2f} seconds")
        else:
            messagebox.showerror("Error", "Encryption failed. Please try again.")

    def show_encrypted_image_preview(self):
        # Resize the image to fit the label
        encrypted_image_resized = self.encrypted_image.resize((300, 300))

        # Convert the resized image to a Tkinter PhotoImage
        tk_encrypted_image = ImageTk.PhotoImage(encrypted_image_resized)

        # Update the label with the new image
        self.encrypted_image_preview.configure(image=tk_encrypted_image)
        self.encrypted_image_preview.image = tk_encrypted_image  # Keep a reference to avoid garbage collection

    def save_encrypted_image(self):
        # Create a file dialog to select the folder and get the filename
        encrypted_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("Image files", "*.png"), ("All files", "*.*")))

        # If a file path is selected
        if encrypted_file:
            # Get the folder path and filename
            folder, filename_encrypted_image = os.path.split(encrypted_file)
            
        self.encrypted_image.save(filename_encrypted_image)
        
    def save_keyfile(self):
        # Create a file dialog to select the folder and get the filename
        folder_keyfile = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

        # If a file path is selected
        if folder_keyfile:
            # Get the folder path and filename
            folder, filename = os.path.split(folder_keyfile)
            
            # Call write_key_to_file with the folder path and filename
            crypto = GaussCircleCrypto()
            crypto.write_key_to_file(self.encryption_key, filename)

    def decrypt_image(self):
        # Check if an image and key file are selected
        if not hasattr(self, 'keyfile') or not hasattr(self, 'image_preview'):
            messagebox.showerror("Error", "Please select an image and a key file.")
            return
        
        start_time_decryption = time.time()
        crypto = GaussCircleCrypto()
        read_key = crypto.read_key_from_file(self.filepath_key)
        self.decrypted_image = crypto.decrypt(self.filepath_img, read_key)
        end_time_decryption = time.time()
        decryption_duration = end_time_decryption - start_time_decryption
        if self.decrypted_image:
            self.show_decrypted_image_preview()
            self.decryption_duration_label.config(text=f"Decryption Duration: {decryption_duration:.2f} seconds")
        else:
            messagebox.showerror("Error", "Decryption failed. The key and the image do not match.")
    
    def show_decrypted_image_preview(self):
        # Resize the image to fit the label
        decrypted_image_resized = self.decrypted_image.resize((300, 300))

        # Convert the resized image to a Tkinter PhotoImage
        tk_decrypted_image = ImageTk.PhotoImage(decrypted_image_resized)

        # Update the label with the new image
        self.decrypted_image_preview.configure(image=tk_decrypted_image)
        self.decrypted_image_preview.image = tk_decrypted_image  # Keep a reference to avoid garbage collection

    def save_decrypted_image(self):
        # Create a file dialog to select the folder and get the filename
        decrypted_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("Image files", "*.png"), ("All files", "*.*")))

        # If a file path is selected
        if decrypted_file:
            # Get the folder path and filename
            folder, decrypted_filename = os.path.split(decrypted_file)
            
        self.decrypted_image.save(decrypted_filename)

    def center_window(self, window, width, height):
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = (screen_width - width) // 2
        y = 1*(screen_height - height) // 8

        # Set the geometry string
        geometry_string = f"{width}x{height}+{x}+{y}"

        # Set the window geometry
        window.geometry(geometry_string)

    def on_closing(self):
        if messagebox.askyesno(title="Keluar Aplikasi", message="Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.root.destroy()

appGaussCircleIterated()