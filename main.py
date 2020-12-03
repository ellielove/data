
# tkinter
import PySimpleGUI as psg

import simple_data_entry as sde


class Application:

    @staticmethod
    def create_primary_window_layout():
        # window layout
        return [
              [psg.Text('Browse:')]
            , [psg.Output(size=(50, 10), key='-OUTPUT-')]
            , [psg.Button('New Entry')]
        ]

    def __init__(self):
        """init application, but not open window"""
        self.dict = {}
        self.window_title = 'Thought Fragment Library'
        psg.theme('DarkAmber')
        self.layout = self.create_primary_window_layout()
        self.window = psg.Window(self.window_title, self.layout)

    def modify_dictionary_entry(self, entry):
        """inserts a new entry, or modifies an existing entry, in the program dict """
        if entry['devname'] == '':
            return
        self.dict[entry['devname']] = entry

    def run(self):
        """runs a single cycle of the application"""

        def refresh_output():
            """convenience method, not to be used outside of Application().run()"""
            update_str = ''
            for key in self.dict.keys():
                update_str += key + ' : ' + self.dict[key]['tags'] + '\n'
            self.window['-OUTPUT-'].update(update_str)

        while True:
            event, values = self.window.read(timeout=150)
            if event == psg.WINDOW_CLOSED:
                break
            if event == 'New Entry':
                data = sde.simple_data_entry_window_cycle()
                self.modify_dictionary_entry(data)
                refresh_output()

            if event and event != '__TIMEOUT__':
                continue

        print('loop exit')
        self.window.close()
        print('window close')


if __name__ == '__main__':
    Application().run()
