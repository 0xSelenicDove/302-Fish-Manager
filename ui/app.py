import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

# 导入自定义模块
from api.client import FishAudioClient
from utils.validator import validate_training_inputs


class VoiceTrainerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 窗口基础设置
        self.title("302-Fish-Manager")
        self.geometry("600x750")
        ctk.set_appearance_mode("dark")

        # 内部状态变量
        self.selected_cover = None
        self.selected_voices = []

        self._setup_ui()

    def _setup_ui(self):
        """初始化 UI 组件"""
        self.label_title = ctk.CTkLabel(self, text="Fish Audio Model Trainer", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        # API Key 输入框
        self.entry_key = ctk.CTkEntry(self, placeholder_text="Enter 302.AI API Key", width=450, show="*")
        self.entry_key.pack(pady=10)

        # 模型标题输入框
        self.entry_name = ctk.CTkEntry(self, placeholder_text="Model Title (e.g., Columbina_V1)", width=450)
        self.entry_name.pack(pady=10)

        # 模型描述文本域
        self.label_desc = ctk.CTkLabel(self, text="Model Description:")
        self.label_desc.pack()
        self.entry_desc = ctk.CTkTextbox(self, width=450, height=80)
        self.entry_desc.pack(pady=5)

        # 可见性下拉菜单
        self.label_vis = ctk.CTkLabel(self, text="Visibility:")
        self.label_vis.pack()
        self.option_vis = ctk.CTkOptionMenu(self, values=["private", "public", "unlist"])
        self.option_vis.set("private")
        self.option_vis.pack(pady=5)

        # 封面图选择区域
        self.btn_cover = ctk.CTkButton(self, text="Select Cover Image (Required for Public)",
                                       command=self._select_cover, fg_color="#6c757d")
        self.btn_cover.pack(pady=15)
        self.label_cover_path = ctk.CTkLabel(self, text="No cover selected", text_color="gray")
        self.label_cover_path.pack()

        # 音频样本选择区域
        self.btn_select = ctk.CTkButton(self, text="Select Training Voices",
                                        command=self._select_voices, fg_color="#1f538d")
        self.btn_select.pack(pady=10)
        self.label_files = ctk.CTkLabel(self, text="No voices selected", text_color="gray")
        self.label_files.pack()

        # 训练触发按钮
        self.btn_train = ctk.CTkButton(self, text="Start Training", command=self._start_training_thread,
                                       fg_color="#28a745", hover_color="#218838")
        self.btn_train.pack(pady=30)

        # 进度条
        self.progress = ctk.CTkProgressBar(self, width=450)
        self.progress.set(0)
        self.progress.pack(pady=10)

    # --- 交互逻辑 ---

    def _select_cover(self):
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp")])
        if file:
            self.selected_cover = file
            self.label_cover_path.configure(text=f"Cover: {os.path.basename(file)}", text_color="#3b82f6")

    def _select_voices(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
        if files:
            self.selected_voices = list(files)
            self.label_files.configure(text=f"{len(files)} voices selected", text_color="white")

    def _start_training_thread(self):
        """开启新线程运行任务，防止 GUI 假死"""
        task_thread = threading.Thread(target=self._run_training_process)
        task_thread.start()

    def _run_training_process(self):
        # 1. 收集数据
        api_key = self.entry_key.get().strip()
        title = self.entry_name.get().strip()
        description = self.entry_desc.get("1.0", "end").strip()
        visibility = self.option_vis.get()

        # 2. 验证输入 (使用外部 Validator)
        is_valid, error_msg = validate_training_inputs(
            api_key, title, self.selected_voices, visibility, self.selected_cover
        )

        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return

        # 3. 准备 UI 状态
        self.btn_train.configure(state="disabled")
        self