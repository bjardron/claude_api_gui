import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES

class GUILayout:
    def setup_main_window(self):
        self.root = TkinterDnD.Tk()  # Use TkinterDnD.Tk for drag and drop support
        self.root.title("Claude API")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

    def create_chat_window(self):
        self.chat_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.chat_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.configure_styles()
        self.create_input_fields()
        self.create_conversation_display()
        self.create_message_entry()
        self.create_buttons()
        self.configure_grid()
        self.create_loading_indicator()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF", foreground="#000000")
        style.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')])
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF", font=("Arial", 10))
        style.configure("TButton", background="#4CAF50", foreground="#FFFFFF", font=("Arial", 10), padding=5)

    def create_input_fields(self):
        self.max_tokens_var = tk.StringVar(value="4096")

        fields = [
            ("System Prompt:", "system_prompt_entry", tk.Entry, {"width": 50}),
            ("Model:", "model_var", ttk.Combobox, {"values": ["Claude Sonnet 3.5", "Claude Opus 3.0", "Claude Haiku 3.0"], "state": "readonly"}),
            ("Temperature:", "temperature_var", ttk.Combobox, {"values": [round(x * 0.1, 1) for x in range(1, 11)], "state": "readonly"}),
            ("Max Tokens:", "max_tokens_entry", tk.Entry, {"width": 10, "textvariable": self.max_tokens_var})
        ]

        for i, (label_text, attr_name, widget_class, widget_kwargs) in enumerate(fields):
            ttk.Label(self.chat_frame, text=label_text).grid(row=i, column=0, padx=(10, 5), pady=(5, 5), sticky=tk.E)
            widget = widget_class(self.chat_frame, **widget_kwargs)
            widget.grid(row=i, column=1, padx=(5, 10), pady=(5, 5), sticky=tk.W, columnspan=2)
            setattr(self, attr_name, widget)

        self.model_var.set("Claude Sonnet 3.5")
        self.temperature_var.set(0.7)

    def create_conversation_display(self):
        self.conversation_text = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, bg="#404040", fg="#FFFFFF", font=("Arial", 10), insertbackground="#FFFFFF")
        self.conversation_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def create_message_entry(self):
        self.message_entry = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=3, width=50, bg="#404040", fg="#FFFFFF", font=("Arial", 10), insertbackground="#FFFFFF")
        self.message_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        send_frame = tk.Frame(self.chat_frame, bg="#2E2E2E")
        send_frame.grid(row=5, column=2, padx=10, pady=5, sticky="nsew")
        tk.Button(send_frame, text="Send", command=self.start_send_message_thread, bg="#3A3A3A", fg="#FFFFFF", font=("Arial", 10), padx=10, pady=5).pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        tk.Button(send_frame, text="Start New Chat", command=self.start_new_chat, bg="#3A3A3A", fg="#FFFFFF", font=("Arial", 10), padx=10, pady=5).pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))
        tk.Label(send_frame, text="Staged Files:", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10)).pack(side=tk.TOP, anchor=tk.W, pady=(10, 0))
        self.create_file_staging_area(send_frame)

    def create_buttons(self):
        button_frame = tk.Frame(self.chat_frame, bg="#2E2E2E")
        button_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        buttons = [
            ("Save Conversation", self.save_conversation),
            ("Review File", self.start_review_file_thread),
            ("Code Review", self.start_code_review_thread)
        ]
        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command, bg="#3A3A3A", fg="#FFFFFF", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=(0, 10))

    def create_file_staging_area(self, parent_frame):
        self.staged_files_list = tk.Listbox(parent_frame, bg="#404040", fg="#FFFFFF", font=("Arial", 10), height=6, width=20)
        self.staged_files_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        clear_button = tk.Button(parent_frame, text="Clear", command=self.clear_staged_files, bg="#3A3A3A", fg="#FFFFFF", font=("Arial", 8))
        clear_button.pack(side=tk.TOP, anchor=tk.W, pady=(5, 0))

    def configure_grid(self):
        self.chat_frame.grid_rowconfigure(4, weight=3)
        self.chat_frame.grid_rowconfigure(5, weight=1)
        for i in range(3):
            self.chat_frame.grid_columnconfigure(i, weight=1)

    def create_loading_indicator(self):
        self.loading_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_label = tk.Label(self.loading_frame, text="Processing...", bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 12))
        self.loading_label.pack(pady=10)
        self.progress_bar = ttk.Progressbar(self.loading_frame, mode="indeterminate", length=200)
        self.progress_bar.pack()
        self.loading_frame.place_forget()

    def clear_staged_files(self):
        self.file_manager.clear_staged_files()
        self.update_staged_files_list()

    
