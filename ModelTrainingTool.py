import customtkinter as ctk
from tkinter import filedialog, messagebox
import requests
import threading
import os

# --- Configuration ---
API_ENDPOINT = "https://api.302.ai/fish-audio/model"


class VoiceTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fish Audio Voice Trainer")
        self.geometry("600x650")
        ctk.set_appearance_mode("dark")

        # --- UI Elements ---
        self.label_title = ctk.CTkLabel(self, text="Fish Audio Model Trainer", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        # API Key
        self.entry_key = ctk.CTkEntry(self, placeholder_text="Enter 302.AI API Key", width=450, show="*")
        self.entry_key.pack(pady=10)

        # Model Title (Required)
        self.entry_name = ctk.CTkEntry(self, placeholder_text="Model Title (e.g., Columbina_V1)", width=450)
        self.entry_name.pack(pady=10)

        # Description (Optional)
        self.entry_desc = ctk.CTkTextbox(self, width=450, height=80)
        self.entry_desc.insert("0.0", "Model description...")
        self.entry_desc.pack(pady=10)

        # Visibility
        self.label_vis = ctk.CTkLabel(self, text="Visibility:")
        self.label_vis.pack()
        self.option_vis = ctk.CTkOptionMenu(self, values=["private", "public", "unlist"])
        self.option_vis.set("private")
        self.option_vis.pack(pady=5)

        # Audio File Selection
        self.btn_select = ctk.CTkButton(self, text="Select Audio Files", command=self.select_files, fg_color="#1f538d")
        self.btn_select.pack(pady=15)

        self.label_files = ctk.CTkLabel(self, text="No files selected", text_color="gray")
        self.label_files.pack()
        self.selected_files = []

        # Training Button
        self.btn_train = ctk.CTkButton(self, text="Start Training", command=self.start_training_thread,
                                       fg_color="#28a745", hover_color="#218838")
        self.btn_train.pack(pady=30)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=450)
        self.progress.set(0)
        self.progress.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
        if files:
            self.selected_files = list(files)
            self.label_files.configure(text=f"{len(files)} files selected", text_color="white")

    def start_training_thread(self):
        # Run API call in a thread so the UI doesn't freeze
        thread = threading.Thread(target=self.run_training)
        thread.start()

    def run_training(self):
        api_key = self.entry_key.get().strip()
        title = self.entry_name.get().strip()
        description = self.entry_desc.get("1.0", "end").strip()
        visibility = self.option_vis.get()

        if not api_key or not title or not self.selected_files:
            messagebox.showerror("Error", "API Key, Title, and Audio Files are required!")
            return

        self.btn_train.configure(state="disabled")
        self.progress.set(0.3)

        # Prepare Multipart Body
        headers = {"Authorization": f"Bearer {api_key}"}

        # Static params required by 302.AI [cite: 596, 611]
        data = {
            "type": "tts",  # Required [cite: 597]
            "title": title,  # Required [cite: 601]
            "train_mode": "fast",  # Required [cite: 611]
            "visibility": visibility,
            "description": description
        }

        # Handling multiple files for 'voices' [cite: 615]
        files = []
        try:
            for f_path in self.selected_files:
                files.append(("voices", (os.path.basename(f_path), open(f_path, "rb"))))

            response = requests.post(API_ENDPOINT, headers=headers, data=data, files=files)
            self.progress.set(1.0)

            if response.status_code == 200:
                result = response.json()
                model_id = result.get("id", "Unknown")
                messagebox.showinfo("Success", f"Model created successfully!\nModel ID: {model_id}")
            else:
                messagebox.showerror("API Error", f"Status: {response.status_code}\n{response.text}")

        except Exception as e:
            messagebox.showerror("System Error", str(e))
        finally:
            for _, f_tuple in files:
                f_tuple[1].close()  # Close file handles
            self.btn_train.configure(state="normal")
            self.progress.set(0)


if __name__ == "__main__":
    app = VoiceTrainerApp()
    app.mainloop()