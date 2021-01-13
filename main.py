import json
import os

# tkinter
import PySimpleGUI as psg

import simple_data_entry as sde
import simple_rename as sr
import save_as_file_dialogue as saveAs


class Application:

    @staticmethod
    def create_menu_bar_layout() -> list:
        return [
            ['&File', ['&Open', 'Save', '&SaveAs', '----', 'Settings', 'E&xit']]
        ]

    @staticmethod
    def create_right_click_menu() -> list:
        return [
            ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]
        ]

    @staticmethod
    def create_primary_window_layout() -> list:
        """this method holds the specification of the layout of the primary window"""
        return [
              [psg.Menu(Application.create_menu_bar_layout(), tearoff=False, pad=(400, 1))]
            , [psg.Text('Search'), psg.Input(size=(50, 1), enable_events=True, key='_SEARCH_')]
            , [psg.Listbox([], size=(50, 30), enable_events=True, key='_LIST_')]
            , [
                  psg.Button('New')
                , psg.Button('Edit')
                , psg.Button('Rename', button_color=(psg.theme_background_color(), 'orange'))
                , psg.Button('Delete', button_color=(psg.theme_background_color(), 'red'))
            ]
        ]

    @staticmethod
    def read_project_file(path) -> dict:
        """returns empty project_data on failure, returns populated project_data on successful read"""
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
        self.project_data = {}
        self.window_title = 'Thought Fragment Library'
        self.save_file_path = 'fragments.project.json'
        self.theme = 'Reddit'
        self.selected_entry = ''
        self.window_size = (400, 600)
        self.save_every_n_ms = 180000  # 3 minutes in ms
        self.time_since_last_save = 0
        self.double_clicks = 0

        psg.theme(self.theme)
        self.layout = self.create_primary_window_layout()
        self.window = psg.Window(
              self.window_title
            , self.layout
            , size=self.window_size
        )

        self.project_data = self.read_project_file(self.save_file_path)

    def modify_dictionary_entry(self, entry) -> None:
        """inserts a new entry, or modifies an existing entry, in the program project_data """
        if 'user_quit' in entry and entry['user_quit']:
            return
        self.project_data[entry['devname']] = entry

    def run(self) -> None:
        """runs a single cycle of the application"""

        def refresh_output():
            """convenience method, not to be used outside of Application().run()"""
            self.window['_LIST_'].update(list(self.project_data.keys()))

        def shutdown_sequence():
            """performs the application shutdown sequence"""
            self.save_project_file(self.project_data, self.save_file_path)
            self.window.close()

        def run_simple_data_entry_window(_entry):
            """invokes one life cycle of the data entry window"""
            _selection = self.project_data[_entry] if _entry in self.project_data else ''
            _modification = sde.simple_data_entry_window_cycle(_selection)
            # this saves changes after edits AND reads
            self.modify_dictionary_entry(_modification)
            self.save_project_file(self.project_data, self.save_file_path)
            refresh_output()

        # activate window with an initial read
        self.window.read(timeout=45)

        # use the data we've loaded in so far
        refresh_output()

        while True:
            event, values = self.window.read(timeout=150)
            self.time_since_last_save += 250

            # this one is going to happen the most
            if event == '__TIMEOUT__':
                if self.time_since_last_save > self.save_every_n_ms:
                    self.save_project_file(self.project_data, self.save_file_path)
                    self.time_since_last_save = 0
                continue

            # this one is the most important
            elif event in (psg.WIN_CLOSED, 'Quit', 'Exit'):
                break

            elif event == 'Save':
                self.save_project_file(self.project_data, self.save_file_path)
                print('Save')

            elif event == 'SaveAs':
                # SaveAs file dialogue
                save = saveAs.FileSaveAsWindow(start_file=self.save_file_path, extensions=('JSON', '.json'))
                self.save_file_path = save.pick_save_file()
                self.save_project_file(self.project_data, self.save_file_path)
                continue

            elif event == 'Open':
                psg.FileBrowse()
                print('Open')
                continue

            elif event == 'Settings':
                print('Settings')
                continue

            # search bar interactions
            elif event == '_SEARCH_':
                if values['_SEARCH_'] != '':
                    search = values['_SEARCH_']
                    new_items = [x for x in self.project_data.keys() if search in x]
                    self.window['_LIST_'].update(new_items)
                else:
                    self.window['_LIST_'].update(list(self.project_data.keys()))

            # NEW
            elif event == 'New':
                run_simple_data_entry_window('')

            # EDIT
            elif event == 'Edit':
                if '_LIST_' in values and values['_LIST_'] != []:
                    selection = values['_LIST_'][0]
                    if selection in self.project_data.keys():
                        run_simple_data_entry_window(selection)

            # RENAME
            elif event == 'Rename':
                if '_LIST_' in values and values['_LIST_'] != []:
                    selection = values['_LIST_'][0]
                    if selection in self.project_data.keys():
                        entry = self.project_data[selection]
                        data = sr.simple_rename_window_cycle(entry)
                        if 'devname' in data and len(data['devname']) > 0:
                            self.project_data[data['devname']] = data
                            del self.project_data[selection]
                            refresh_output()

            # DELETE
            elif event == 'Delete':
                if '_LIST_' in values and values['_LIST_'] != []:
                    selection = values['_LIST_'][0]
                    choice = psg.popup_yes_no('delete: {}'.format(selection))
                    if choice and choice == 'Yes':
                        del self.project_data[selection]
                        self.save_project_file(self.project_data, self.save_file_path)
                        refresh_output()

            # click on list of items, open editor
            elif event == '_LIST_':
                if values['_LIST_'] is None or len(values['_LIST_']) == 0:
                    continue
                run_simple_data_entry_window(values['_LIST_'][0])

        shutdown_sequence()


if __name__ == '__main__':
    Application().run()
