from taipy.gui import Gui, State
import time
from helper import format_duration, add_log, get_minuts, get_current_time

task = ""
yourtask = "Enter Your Task"
init_dic = {
    "task": [],
    "time": [],
    "message": [],
    "activity": [],
    "time_amount": [],
}
logs = init_dic

time_amount = 0
displayed_time = format_duration(time_amount)

button = ""
status = "Not Working"

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

    while not state.stop_flag:
        state.time_amount += 1
        state.displayed_time = format_duration(state.time_amount)
        time.sleep(1)


def cancel(state):
    if state.activity == "Not Working":
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
    state.status = "Not Working"
    state.stop_flag = True


def take_break(state):
    if not (state.status == "Working"):
        return
    add_log(
        state,
        state.yourtask,
        state.time_amount,
        state.status,
        f"\nWorked for {get_minuts(state.time_amount)} mins\nTaking a break",
    )
    state.time_amount = 0
    state.displayed_time = format_duration(0)
    state.status = "Break"


def work(state):
    if not (state.status == "Break"):
        return
    add_log(
        state,
        state.yourtask,
        state.time_amount,
        state.status,
        f"\nTook a break for {get_minuts(state.time_amount)} mins\n Restart a task",
    )
    state.time_amount = 0
    state.displayed_time = format_duration(0)
    state.status = "Working"


page = """
#Task Time Tracker
<|layout|columns=1 1 1|
<|card|
##<|{yourtask}|> <br/>

## <|{task}|input|> <br />
<|Start|button|class_name=submit|on_action=submit|>
<|Finish|button|class_name=secondary|on_action=cancel|>
|>
<|card|
## <|Time Amount|> 
<|{displayed_time}|id=display|> 
|>
<|card|
##<|Status|> <br />
<|{status}|id=status|><br/>
<|board
<|Work|button|class_name=submit|on_action=work|>
<|Break|button|class_name=secondary|on_action=take_break|>
|>
|>
|>
<|container log-board|
##<|Log|>
<|{logs}|table|columns={["task","time","message","activity","time_amount"]}|show_all|>
|>


"""
Gui(page, css_file="main.css").run(
    title="Task Time Tracker", dark_mode=True, use_reloader=True, port=5001
)
