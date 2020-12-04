import PySimpleGUI as psg


def create_layout(file_name):
    return [
          [psg.Text('Rename: {}'.format(file_name), key='_FILENAME_')]
        , [psg.InputText(key='_INPUT_')]
        , [psg.Button('Submit'), psg.Button('Cancel')]
    ]


def simple_rename_window_cycle(entry):
    """Instantiates, uses, and destorys a simple data entry window, and returns the new name"""
    layout = create_layout(entry['devname'])
    window = psg.Window('Rename Entry', layout)

    while True:
        event, values = window.read(150)

        if event in ('Cancel', psg.WINDOW_CLOSED):
            window.close()
            return {'user_quit': True}

        if event == 'Submit':
            new_name = values['_INPUT_']
            entry['devname'] = new_name
            window.close()
            return entry



