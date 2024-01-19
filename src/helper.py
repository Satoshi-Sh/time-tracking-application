from datetime import datetime
import random
from kintone.controller import post_record, get_todays_data

snakes = [
    "cobra",
    "viper",
    "habu",
    "keelback",
    "krait",
    "lancehead",
    "lora",
    "mamba",
    "mamushi",
    "moccasin",
    "python",
    "racer",
    "rat_snake",
    "sea_snake",
    "taipan",
    "titanoboa",
    "urutu",
    "viper",
    "cat",
    "dog",
    "lion",
    "panda",
    "racoon",
    "bear",
    "cow",
    "sheep",
    "rabbit",
    "tiger",
    "spider",
]


def get_random_name():
    return f"{random.choice(snakes)}_{random.randint(1,99)}"


def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_current_date():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return current_date


def get_minutes(seconds):
    minutes, remaining_seconds = divmod(seconds, 60)
    return minutes


def add_log(state, task, time_amount, status, message):
    current_time = get_current_time()
    ## Backend post
    data = {
        "username": {"value": state.username},
        "time": {"value": current_time},
        "task": {"value": task},
        "date": {"value": get_current_date()},
        "status": {"value": status},
        "time_amount": {"value": time_amount},
    }
    post_record(data)
    ## UI part
    temp = state.logs
    temp.task.append(task)
    temp.time.append(current_time)
    temp.time_amount.append(time_amount)
    temp.message.append(message)
    temp.status.append(status)
    state.logs = temp
    ## Get New Data
    state.todays_df = get_todays_data()


# Find unique values in a list
def find_unique_keys(my_list):
    unique_values = [
        item for index, item in enumerate(my_list) if item not in my_list[:index]
    ]
    return unique_values


def compute_times(state):
    unique_tasks = find_unique_keys(state.logs["task"])

    # Create a copy of plot_data to avoid modifying state in-place
    new_plot_data = {key: state.plot_data[key].copy() for key in state.plot_data}

    new_plot_data["Task"] = unique_tasks

    total_times = [0 for _ in range(len(unique_tasks))]
    new_plot_data["Work"] = total_times

    break_times = [0 for _ in range(len(unique_tasks))]
    new_plot_data["Break"] = break_times

    # Go through each task in unique list
    for i in range(len(unique_tasks)):
        # Go through each task in logs list
        for j in range(len(state.logs["task"])):
            # if unique task is equal to logs task
            if unique_tasks[i] == state.logs["task"][j]:
                if state.logs["status"][j] == "Working":
                    new_plot_data["Work"][i] += state.logs["time_amount"][j]
                elif state.logs["status"][j] == "Break":
                    new_plot_data["Break"][i] += state.logs["time_amount"][j]

    # Update the state with the new plot data
    state.plot_data = new_plot_data


prop = {
    # Shared y values
    "y": "users",
    "x[1]": "Break",
    "color[1]": "#c26391",
    "x[2]": "Working",
    "color[2]": "#5c91de",
    "orientation": "h",
    #
    "layout": {
        "barmode": "overlay",
        # Set a relevant title for the x axis
        "xaxis": {"title": "Users"},
        # Hide the legend
        "showlegend": False,
    },
}
