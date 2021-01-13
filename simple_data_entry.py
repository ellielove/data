import PySimpleGUI as psg


def create_layout():
    return [
          [psg.Text('Dev Name'   , size=(15, 1)), psg.InputText(key='_DEVNAME_', size=(300,1))]
        , [psg.Text('Public Name', size=(15, 1)), psg.InputText(key='_PUBNAME_', size=(300,1))]
        , [psg.Text('Notes'      , size=(15, 1)), psg.Multiline(key='_NOTES_', size=(300,10))]
        , [psg.Text('Tags'       , size=(15, 1)), psg.InputText(key='_TAGS_', size=(300,1))]
        , [psg.Button('Save'), psg.Button('Cancel')]
    ]


def simple_data_entry_window_cycle(entry=None, title=None, layout=None):
    """Instantiates, uses, and destroys a simple data entry window, and returns the input data """

    if not title:
        title = 'Simple Data Entry'
    if not layout:
        layout = create_layout()

    window = psg.Window(title, layout, size=(600, 300), return_keyboard_events=True, keep_on_top=True)

    if entry:
        window.read(timeout=45)
        window['_DEVNAME_'].update(entry['devname'], disabled=True, text_color='gray')
        window['_PUBNAME_'].update(entry['pubname'])
        window['_NOTES_'].update(entry['notes'])
        window['_TAGS_'].update(entry['tags'])

    while True:
        event, values = window.read(timeout=150)

        # quit without saving info
        if event == 'Cancel' or event == psg.WINDOW_CLOSED or event == 'Escape:27':
            window.close()
            return {'user_quit': True}

        if event == 'Save':
            result = {
                  'devname': values['_DEVNAME_']
                , 'pubname': values['_PUBNAME_']
                , 'notes'  : values['_NOTES_']
                , 'tags'   : values['_TAGS_']
            }
            window.close()
            return result
