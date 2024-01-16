from taipy.gui import Gui, State
import time
from helper import (
    format_duration,
    add_log,
    get_minutes,
    get_current_time,
    compute_times,
)

task = ""
yourtask = "Enter Your Task"
init_dic = {
    "task": [],
    "time": [],
    "message": [],
    "status": [],
    "time_amount": [],
}
logs = init_dic
plot_data = {"Task": [], "Work": [], "Break": []}

time_amount = 0
displayed_time = format_duration(time_amount)

button = ""
status = "Not Started"
status_btn_label = "----"

start_stop_btn_label = "START"

stop_flag = False


def submit(state):
    if state.task == "":
        return
    state.yourtask = state.task
    state.logs = init_dic
    add_log(state, state.yourtask, 0, "Start", f"Started Task:{state.task}")
    state.task = ""
    state.stop_flag = False
    state.status = "Working"
    state.status_btn_label = "BREAK"
    state.start_stop_btn_label = "FINISH"

    while not state.stop_flag:
        state.time_amount += 1
        state.displayed_time = format_duration(state.time_amount)
        time.sleep(1)


def finish(state):
    if state.status == "Not Working":
        return
    add_log(
        state,
        state.yourtask,
        state.time_amount,
        state.status,
        f"Completed {state.yourtask}",
    )
    state.task = ""
    state.yourtask = "Enter Your Task"
    state.time_amount = 0
    state.displayed_time = format_duration(0)
    state.status = "Not Started"
    state.stop_flag = True
    state.start_stop_btn_label = "START"
    state.status_btn_label = "----"
    compute_times(state)


def start_stop_btn_action(state):
    if state.status == "Working":
        finish(state)
    else:
        submit(state)


def take_break(state):
    if not (state.status == "Working"):
        return
    add_log(
        state,
        state.yourtask,
        state.time_amount,
        state.status,
        f"\nWorked for {get_minutes(state.time_amount)} mins\nTaking a break",
    )
    state.time_amount = 0
    state.displayed_time = format_duration(0)
    state.status = "Break"
    state.status_btn_label = "WORK"
    compute_times(state)


def work(state):
    if not (state.status == "Break"):
        return
    add_log(
        state,
        state.yourtask,
        state.time_amount,
        state.status,
        f"\nTook a break for {get_minutes(state.time_amount)} mins\n Restart a task",
    )
    state.time_amount = 0
    state.displayed_time = format_duration(0)
    state.status = "Working"
    state.status_btn_label = "BREAK"
    compute_times(state)


def status_btn_action(state):
    if state.status == "Working":
        take_break(state)

    elif state.status == "Break":
        work(state)


plot_properties = {
    "y[1]": "Break",
    "color[1]": "#dc2626",
    "y[2]": "Work",
    "color[2]": "#16a34a",
    "x": "Task",
}


page = """
#Task Time Tracker
<|layout|columns=1 1 1|
<|card|
##<|{yourtask}|> <br/>

## <|{task}|input|> <br />
<|{start_stop_btn_label}|button|on_action=start_stop_btn_action|>
|>
<|card|
## <|Time Amount|> 
<|{displayed_time}|id=display|> 
|>
<|card|
##<|Status|> <br />
<|{status}|id=status|><br/>
<|board
<|{status_btn_label}|button|on_action=status_btn_action|active={status!="Not Started"}|>

|>
|>
|>
<|container log-board|
##<|Log|>
<|{logs}|table|columns={["task","time","message","status","time_amount"]}|show_all|>
|>

<|{plot_data}|chart|type=bar|properties={plot_properties}|>


"""
Gui(page, css_file="main.css").run(
    title="Task Time Tracker", dark_mode=True, use_reloader=True, port=5001
)
