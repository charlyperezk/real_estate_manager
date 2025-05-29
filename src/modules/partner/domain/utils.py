from datetime import datetime

def current_period() -> str:
    return datetime.now().strftime("%Y-%m")