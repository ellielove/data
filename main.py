import json
import os

# tkinter
import PySimpleGUI as psg

import simple_data_entry as sde


class Application:

    @staticmethod
    def create_primary_window_layout() -> list:
        """this method holds the specification of the layout of the primary window"""
        return [
            [psg.Text('Browse:')]
            , [psg.Output(size=(50, 10), key='-OUTPUT-')]
            , [psg.Button('New Entry')]
        ]

    @staticmethod
    def read_project_file(path) -> dict:
        """returns empty dict on failure, returns populated dict on successful read"""
        if os.path.isfile(path):
            with open(path, 'r') as infile:
                return json.load(infile)
        return {}

    @staticmethod
    def save_project_file(data, path) -> bool:
        """Returns false on failure, true otherwise"""
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        return os.path.isfile(path)

    def __init__(self):
        """init application, but not open window"""
        self.dict = {}
        self.window_title = 'Thought Fragment Library'
        self.save_file_path = 'fragments.project.json'
        self.theme = 'Reddit'

        psg.theme(self.theme)
        self.layout = self.create_primary_window_layout()
        self.window = psg.Window(self.window_title, self.layout)

        self.dict = self.read_project_file(self.save_file_path)

    def modify_dictionary_entry(self, entry) -> None:
        """inserts a new entry, or modifies an existing entry, in the program dict """
        if entry['devname'] == '':
            return
        self.dict[entry['devname']] = entry

    def run(self) -> None:
        """runs a single cycle of the application"""

        def refresh_output():
            """convenience method, not to be used outside of Application().run()"""
            update_str = ''
            for key in self.dict.keys():
                update_str += key + ' : ' + self.dict[key]['tags'] + '\n'
            self.window['-OUTPUT-'].update(update_str)

        def shutdown_sequence():
            """performs the application shutdown sequence"""
            self.save_project_file(self.dict, self.save_file_path)
            self.window.close()

        # activate window with an initial read
        self.window.read(timeout=45)

        # use the data we've loaded in so far
        refresh_output()

        while True:
            event, values = self.window.read(timeout=150)

            # this one is going to happen the most
            if event == '__TIMEOUT__':
                continue
            # this one is the most important
            elif event in (psg.WIN_CLOSED, 'Quit'):
                psg.Print(self.dict, do_not_reroute_stdout=False)
                break
            elif event == 'New Entry':
                data = sde.simple_data_entry_window_cycle()
                self.modify_dictionary_entry(data)
                refresh_output()

        shutdown_sequence()


if __name__ == '__main__':
    Application().run()
