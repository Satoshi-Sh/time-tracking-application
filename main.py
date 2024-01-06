from taipy.gui import Gui

task = "Your Task"
yourtask = 'Your Task'


def submit(state):
    state.yourtask = state.task
    state.task = "Your Task"


def cancel(state):
    state.task = "Your Task"
    state.yourtask = "Your Task"


page = """
#Ur Ma Universal

<|container task-card|
##<|{yourtask}|> <br/>

## <|{task}|input|> <br />
<|Submit|button|class_name=submit|on_action=submit|>
<|Cancel|button|class_name=secondary|on_action=cancel|>
|>

"""

Gui(page, css_file="main.css").run(use_reloader=True, port=5001)
