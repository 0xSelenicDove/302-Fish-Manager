import requests
import os


class FishAudioClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.302.ai/fish-audio/model"

    def train_model(self, title, visibility, voices, description="", cover_image=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "type": "tts",
            "title": title,
            "train_mode": "fast",
            "visibility": visibility,
            "description": description
        }

        files = []
        try:
            if cover_image:
                files.append(("cover_image", (os.path.basename(cover_image), open(cover_image, "rb"))))
            for v in voices:
                files.append(("voices", (os.path.basename(v), open(v, "rb"))))

            return requests.post(self.endpoint, headers=headers, data=data, files=files)
        finally:
            for _, f_tuple in files:
                f_tuple[1].close()