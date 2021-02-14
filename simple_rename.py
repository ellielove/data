import PySimpleGUI as psg


def create_layout(entry_name):
    return [
          [psg.Text('Rename: {}'.format(entry_name), key='_FILENAME_')]
        , [psg.InputText(default_text=entry_name, key='_INPUT_')]
        , [psg.Button('Submit'), psg.Button('Cancel')]
    ]


def simple_rename_window_cycle(entry):
    """Instantiates, uses, and destroys a simple data entry window, and returns the new name"""
    layout = create_layout(entry['devname'])
    window = psg.Window('Rename Entry', layout)

    while True:
        event, values = window.read(150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            window.close()
            return {'user_quit': True}

        if event == 'Submit':
            new_name = values['_INPUT_']
            entry['devname'] = new_name
            window.close()
            return entry



