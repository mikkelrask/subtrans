SOURCE_LANG = "en"  # Source language code (e.g., 'en', 'ja', 'da')
TARGET_LANG = "da"  # Target language code
MODEL = f"Helsinki-NLP/opus-mt-{SOURCE_LANG}-{TARGET_LANG}"

SOURCE_SUFFIX = f".{SOURCE_LANG}"
TARGET_SUFFIX = f".{TARGET_LANG}"

SUBTITLE_FORMATS = [".srt", ".ass"]

def get_source_patterns():
    return [f"*{SOURCE_SUFFIX}{ext}" for ext in SUBTITLE_FORMATS]

def get_target_suffix():
    return TARGET_SUFFIX

def get_model_name():
    return MODEL 