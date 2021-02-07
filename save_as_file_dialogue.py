import PySimpleGUI as psg


class FileSaveAsWindow:

    @staticmethod
    def create_layout() -> list:
        return [
              [psg.Text('Save As - File Dialogue')]
            , [psg.Combo(
                psg.user_settings_get_entry('-filenames-', [])
                , default_value=psg.user_settings_get_entry('-last filename-', '')
                , size=(50, 1)
                , key='-FILENAME-'
                )
                , psg.FileSaveAs('File')
            ]
            , [psg.Button('Accept'), psg.Button('Clear'), psg.Button('Exit')]]

    def __init__(self, start_file, extensions, title='Save Project As'):
        self.window = psg.Window(title, self.create_layout())

    def pick_save_file(self) -> str:
        result = ''
        while True:

            #event, values = self.window.Read(timeout=150)
            event, values = self.window.Read(timeout=150)

            if event is None or event == 'Exit':
                break

            if event == 'Accept':
                psg.user_settings_set_entry('-filenames-', list(
                    set(psg.user_settings_get_entry('-filenames-', []) + [values['-FILENAME-'], ])))
                psg.user_settings_set_entry('-last filename-', values['-FILENAME-'])
                self.window['-FILENAME-'].update(values=list(set(psg.user_settings_get_entry('-filenames-', []))))
                result = psg.user_settings_get_entry('-filenames-')[0]
                break

            elif event == 'Clear':
                psg.user_settings_set_entry('-filenames-', [])
                psg.user_settings_set_entry('-last filename-', '')
                self.window['-FILENAME-'].update(values=[], value='')

        self.window.close()
        return result
