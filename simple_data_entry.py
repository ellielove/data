import PySimpleGUI as psg


def create_layout():
    return [
          [psg.Text('Dev Name'   , size=(15, 1)), psg.InputText(key='_DEVNAME_')]
        , [psg.Text('Public Name', size=(15, 1)), psg.InputText(key='_PUBNAME_')]
        , [psg.Text('Notes'      , size=(15, 1)), psg.InputText(key='_NOTES_')]
        , [psg.Text('Tags'       , size=(15, 1)), psg.InputText(key='_TAGS_')]
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
        window['_DEVNAME_'].update(entry['devname'], disabled=True, text_color='gray')
        window['_PUBNAME_'].update(entry['pubname'])
        window['_NOTES_'].update(entry['notes'])
        window['_TAGS_'].update(entry['tags'])

    while True:
        event, values = window.read(150)

        # quit without saving info
        if event == 'Cancel' or event == psg.WINDOW_CLOSED:
            window.close()
            return {'user_quit': True}

        if event == 'Save':
            result = {
                  'devname' : values['_DEVNAME_']
                , 'pubname' : values['_PUBNAME_']
                , 'notes'   : values['_NOTES_']
                , 'tags'    : values['_TAGS_']
            }
            window.close()
            return result
