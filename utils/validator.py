# utils/validator.py

def validate_training_inputs(api_key, title, voices, visibility, cover_image=None):

    if not api_key:
        return False, "API Key is required."

    if not title:
        return False, "Model Title is required."

    if not voices or len(voices) == 0:
        return False, "At least one training voice file is required."

    # 核心逻辑：公开模型必须有封面图
    if visibility == "public" and not cover_image:
        return False, "A cover image is required for public models."

    return True, ""