# Fish-TTS Text-to-Speech Model Management Tool
这是一套基于 CustomTkinter 开发的桌面端工具，旨在通过 302.AI 提供的 Fish Audio 接口，让用户能够更便捷地通过上传自定义音频文件来训练独有的 TTS 模型。

## ✨ 核心特性

- **现代化的 GUI 界面**: 采用 CustomTkinter 构建，支持暗色模式，比传统的命令行工具更直观。

- **多文件批量上传**：支持一次性选择并上传多个 .wav, .mp3 或 .flac 文件，自动处理 multipart/form-data 请求。

- **多线程异步处理**：上传过程在独立线程运行，确保在处理大文件时界面不会卡死。

- **参数自定义**：支持设置模型名称（Title）、描述（Description）以及可见性（Visibility）。

- **针对 302.AI 优化**：自动配置 train_mode: fast 和 type: tts 等必填参数，简化用户操作。

## 🛠️ 安装与准备
1. 克隆仓库
    ```
    git clone https://github.com/your-username/ModelTrainingTool.git
    cd ModelTrainingTool
    ```
2. 安装依赖项

    本项目需要 requests 和 customtkinter 库：

    `` pip install requests customtkinter``

## 🚀 使用方法
1. 运行主程序：

    ```
    python ModelTrainingTool.py
    ```
2. 在界面中输入你的 302.AI API KEY。
3. 输入你想给模型起的名字（Model Title）。
4. 点击 Select Audio Files 选择用于训练的音频样本。
5. 点击 Start Training 开始上传并训练。训练成功后，你将获得一个 Model ID，你可以将其用于 moeru-ai/airi 或其他支持 IndexTTS 的项目。

## 📦 打包为独立程序 (.exe)
如果你想在没有 Python 环境的电脑上运行，可以使用 PyInstaller 将其打包：

```
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter ModelTrainingTool.py
```

打包完成后，可在 dist/ 文件夹中找到生成的执行文件。

## 📝 开发计划 (Roadmap)
[ ] 增加 Model List 标签页，用于查看和管理已创建的音色。

[ ] 增加音色更新（Update Voice）和删除（Delete Voice）功能。

[ ] 训练进度实时反馈增强。