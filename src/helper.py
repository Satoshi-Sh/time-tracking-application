from datetime import datetime


def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_minutes(seconds):
    minutes, remaining_seconds = divmod(seconds, 60)
    return minutes


def add_log(state, task, time_amount, status, message):
    temp = state.logs
    temp.task.append(task)
    temp.time.append(get_current_time())
    temp.time_amount.append(time_amount)
    temp.message.append(message)
    temp.status.append(status)
    state.logs = temp

# Find unique values in a list
def find_unique_keys(my_list):
    unique_values = [item for index, item in enumerate(my_list) if item not in my_list[:index]]
    return unique_values


def compute_times(state):
    unique_tasks = find_unique_keys(state.logs["task"])
    state.plot_data["Task"] = unique_tasks #plot data task list contains unique tasks
    total_times = [0 for _ in range(len(unique_tasks))] 
    state.plot_data["Work"] = total_times #plot data total_time list set to zero
    break_times = [0 for _ in range(len(unique_tasks))]
    state.plot_data["Break"] = break_times
    #Go through each task in unique list
    for i in range(len(state.plot_data["Task"])): 
        #Go through each task in logs list
        for j in range(len(state.logs["task"])):
            #if unique task is equal to logs task
            if state.plot_data["Task"][i] == state.logs["task"][j]:
                if state.logs["status"][j] == "Working":
                    state.plot_data["Work"][i]= state.plot_data["Work"][i] + state.logs["time_amount"][j]
                elif state.logs["status"][j] == "Break":
                  state.plot_data["Break"][i]= state.plot_data["Break"][i] + state.logs["time_amount"][j]
                    
