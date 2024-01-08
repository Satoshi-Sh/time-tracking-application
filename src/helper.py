from datetime import datetime


def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_minuts(seconds):
    minutes, remaining_seconds = divmod(seconds, 60)
    return minutes


def add_log(
    state, task, time_amount=59, activity="break", message="hello this is a test"
):
    temp = state.logs
    temp.task.append(task)
    temp.time.append(get_current_time())
    temp.time_amount.append(time_amount)
    temp.message.append(message)
    temp.activity.append(activity)
    state.logs = temp
