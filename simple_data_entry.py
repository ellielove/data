import PySimpleGUI as psg


def create_layout():
    return [
          [psg.Text('New Entry: [Development Name, Public Name, Notes, Tags]')]
        , [psg.Text('devname'   , size=(15, 1)), psg.InputText()]
        , [psg.Text('pubname'   , size=(15, 1)), psg.InputText()]
        , [psg.Text('notes'     , size=(15, 1)), psg.InputText()]
        , [psg.Text('tags'      , size=(15, 1)), psg.InputText()]
        , [psg.Button('Submit'), psg.Button('Cancel')]
    ]


def simple_data_entry_window_cycle(title=None, layout=None):
    """Instantiates, uses, and destroys a simple data entry window, and returns the input data """

    # psg.Theme('')

    if not title:
        title = 'Simple Data Entry'
    if not layout:
        layout = create_layout()

    window = psg.Window(title, layout)
    while True:
        event, values = window.read(150)

        # quit without saving info
        if event == 'Cancel' or event == psg.WINDOW_CLOSED:
            window.close()
            return {'user-quit': True}

        if event == 'Submit':
            window.close()
            return {
                  'devname' : values[0]
                , 'pubname' : values[1]
                , 'notes'   : values[2]
                , 'tags'    : values[3]
            }
