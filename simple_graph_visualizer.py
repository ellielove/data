import PySimpleGUI as psg


def create_layout():
    return [
        [psg.Output(size=(60,20))]
    ]


def simple_graph_visualizer_window_cycle(file=None, title=None, layout=None):
    if not title:
        title = 'Simple Graph Visualizer'

    if not layout:
        layout = create_layout()

    window = psg.Window(title, layout, size=(600,500), return_keyboard_events=True)
    window.read(timeout=45)

    def shutdown_sequence():
        # save
        window.close()

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break


    shutdown_sequence()



