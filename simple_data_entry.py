import PySimpleGUI as psg


def create_layout():
    return [
          [psg.Text('New Entry: [Development Name, Public Name, Notes, Tags]')] # 0
        , [psg.Text('devname'   , size=(15, 1)), psg.InputText()]               # 1
        , [psg.Text('pubname'   , size=(15, 1)), psg.InputText()]               # 2
        , [psg.Text('notes'     , size=(15, 1)), psg.InputText()]               # 3
        , [psg.Text('tags'      , size=(15, 1)), psg.InputText()]               # 4
        , [psg.Button('Save'), psg.Button('Cancel')]
    ]


def simple_data_entry_window_cycle(entry=None, title=None, layout=None):
    """Instantiates, uses, and destroys a simple data entry window, and returns the input data """

    if not title:
        title = 'Simple Data Entry'
    if not layout:
        layout = create_layout()

    window = psg.Window(title, layout)

    if entry:
        window.read(timeout=45)
        layout[1][1].update(default_text=entry['devname'])
        layout[2][1].update(default_text=entry['pubname'])
        layout[3][1].update(default_text=entry['notes'])
        layout[4][1].update(default_text=entry['tags'])

    while True:
        event, values = window.read(150)

        # quit without saving info
        if event == 'Cancel' or event == psg.WINDOW_CLOSED:
            window.close()
            return {'user_quit': True}

        if event == 'Save':
            result = {
                  'devname' : values[0]
                , 'pubname' : values[1]
                , 'notes'   : values[2]
                , 'tags'    : values[3]
            }
            window.close()
            return result