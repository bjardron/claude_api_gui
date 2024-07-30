import threading
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from file_manager import FileManager
from claude_api import ClaudeAPI
from gui_layout import GUILayout
from allowed_extensions import allowed_extensions


class ClaudeGUI(GUILayout):
    def __init__(self):
        super().__init__()  # Call the parent class's __init__ method
        self.file_manager = FileManager()
        self.setup_main_window()
        self.claude_api = ClaudeAPI()
        self.create_chat_window()

    def start_send_message_thread(self):
        threading.Thread(target=self.send_message, daemon=True).start()

    def send_message(self):
        self.show_loading()
        
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message and not self.file_manager.staged_files:
            self.hide_loading()
            return

        # Process staged files if any
        if self.file_manager.staged_files:
            file_contents = self.process_files()
            message = f"{file_contents}\n\nUser message:\n{message}"

        model_mapping = {
            "Claude Sonnet 3.5": "claude-3-5-sonnet-20240620",
            "Claude Opus 3.0": "claude-3-opus-20240229",
            "Claude Haiku 3.0": "claude-3-haiku-20240307"
        }
        model = model_mapping.get(self.model_var.get(), "claude-3-5-sonnet-20240620")

        try:
            max_tokens = int(self.max_tokens_var.get())
        except ValueError:
            self.hide_loading()
            messagebox.showerror("Invalid Input", "Max Tokens must be an integer.")
            return

        system_prompt = self.system_prompt_entry.get()

        try:
            response = self.claude_api.send_message(
                model=model,
                temperature=float(self.temperature_var.get()),
                max_tokens=max_tokens,
                message=message,
                system_prompt=system_prompt
            )
            
            self.update_conversation(f"You: {message}\n")
            self.update_conversation(f"Claude: {response}\n", bold=True)
        except Exception as e:
            self.update_conversation(f"Error: {str(e)}\n")

        self.message_entry.delete("1.0", tk.END)
        self.clear_staged_files()
        self.hide_loading()

    def show_loading(self):
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.progress_bar.start()

    def hide_loading(self):
        self.progress_bar.stop()
        self.loading_frame.place_forget()

    def start_new_chat(self):
        self.conversation_text.delete("1.0", tk.END)
        self.system_prompt_entry.delete(0, tk.END)
        self.message_entry.delete("1.0", tk.END)
        self.update_staged_files_list()

    def update_conversation(self, text, bold=False):
        if bold:
            self.conversation_text.insert(tk.END, text, 'bold')
        else:
            self.conversation_text.insert(tk.END, text)
        self.conversation_text.see(tk.END)

    def save_conversation(self):
        conversation = self.conversation_text.get("1.0", tk.END).strip()
        if conversation:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(conversation)

    def start_review_file_thread(self):
        threading.Thread(target=self.review_file, daemon=True).start()

    def review_file(self):
        file_types = [
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Python Files", "*.py")
        ]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.file_manager.staged_files.append(file_path)
            self.update_staged_files_list()
            self.update_conversation(f"File staged: {file_path}\n")

    def start_code_review_thread(self):
        threading.Thread(target=self.code_review, daemon=True).start()

    def code_review(self):
        directory = filedialog.askdirectory()
        if directory:
            self.file_manager.staged_files = self.file_manager.filter_code_files(directory, allowed_extensions)
            self.update_staged_files_list()
            self.update_conversation(f"Code files staged from directory: {directory}\n")
            self.system_prompt_entry.delete(0, tk.END)
            self.system_prompt_entry.insert(0, "You are an AI that handles batch processing of code files. Process the provided code files in batches and maintain context. Respond to the user message based on the provided conversation context.")
            self.process_code_files_in_batches()

    def process_code_files_in_batches(self):
        batch_size = 5
        total_batches = (len(self.file_manager.staged_files) + batch_size - 1) // batch_size
        for i in range(total_batches):
            batch = self.file_manager.staged_files[i * batch_size:(i + 1) * batch_size]
            self.send_code_files_to_claude(batch)
        self.send_message_to_claude("Begin the comprehensive code review based on all provided files.")

    def send_code_files_to_claude(self, files):
        system_prompt = self.system_prompt_entry.get()
        message = "Code files for review:\n\n"
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    message += f"File: {file_path}\n"
                    message += file.read()
                    message += "\n\n"
            except Exception as e:
                self.update_conversation(f"Error reading file {file_path}: {e}\n")
        params = {
            "system_prompt": system_prompt,
            "model": self.model_var.get(),
            "temperature": float(self.temperature_var.get()),
            "max_tokens": int(self.max_tokens_var.get()),
            "message": message
        }
        try:
            response = self.claude_api.send_message(**params)
            self.update_conversation(f"Batch sent: {', '.join(files)}\n")
            self.update_conversation(f"Claude: {response}\n", bold=True)
        except Exception as e:
            self.update_conversation(f"Error sending code files to Claude: {e}\n")

    def send_message_to_claude(self, message):
        params = {
            "system_prompt": self.system_prompt_entry.get(),
            "model": self.model_var.get(),
            "temperature": float(self.temperature_var.get()),
            "max_tokens": int(self.max_tokens_var.get()),
            "message": message
        }
        try:
            response = self.claude_api.send_message(**params)
            self.update_conversation(f"Claude: {response}\n", bold=True)
        except Exception as e:
            self.update_conversation(f"Error sending message to Claude: {e}\n")

    def drop(self, event):
        file_path = event.data.strip('{}')
        self.file_manager.staged_files.append(file_path)
        self.update_staged_files_list()

    def update_staged_files_list(self):
        self.staged_files_list.delete(0, tk.END)
        for item in self.file_manager.staged_files:
            file_name = os.path.basename(item)
            self.staged_files_list.insert(tk.END, file_name)

    def run(self):
        self.root.mainloop()
