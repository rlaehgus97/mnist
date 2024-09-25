from datetime import datetime

def get_now_time():
    current_time = datetime.now()

    return current_time.strftime("%Y-%m-%d %H:%M:%S")
