import json
import os

import PySimpleGUI as psg


class Node:
    def __init__(self, name, neighbors=None, data=None):
        self.name = name
        self.neighbors = neighbors
        self.data = data


class GraphDatabase:
    def __init__(self):
        self.nodes = {}
        self.save_file_path = ''

    @staticmethod
    def save_project_file(data, path=''):
        """Returns false on failure, true otherwise"""
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
        return os.path.isfile(path)

    @staticmethod
    def read_project_file(path):
        """returns empty project_data on failure, returns populated project_data on successful read"""
        if os.path.isfile(path):
            with open(path, 'r') as infile:
                return json.load(infile)
        return {}

    def add_node(self, name, node):
        if name not in self.nodes:
            self.nodes[name] = node


def create_layout():
    return [
        [psg.Text('Graph Test')]
        ,[psg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400,400), background_color='red', key='_GRAPH_', enable_events=True, drag_submits=True)]
        , [psg.Button('Save'), psg.Button('Exit')]
    ]


def graph_database_window_cycle():
    window = psg.Window(
        title='Graph database'
        , layout=create_layout()
        , size=(600,500)
        , return_keyboard_events=True
        , keep_on_top=True)

    window.read(timeout=45)

    graph = window['_GRAPH_']
    objects = {'circle': graph.DrawCircle((50, 50), 25, fill_color='white', line_color='black')}

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break

    window.close()


if __name__ == '__main__':
    graph_database_window_cycle()
