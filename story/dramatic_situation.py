import json
import os

import PySimpleGUI as psg


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
        , [psg.Graph(
            key='_GRAPH_'
            , canvas_size=(600, 400)
            , graph_bottom_left=(0, 0)
            , graph_top_right=(600, 400)
            , background_color='light gray'
            , enable_events=True
            , drag_submits=True
            , right_click_menu=['&Right', ['IsA', 'HasA']]
        )]
        , [psg.Button('Save'), psg.Button('Exit')]
    ]


class DragManager:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.object = None
        self.is_active = False


class SpawnManager:
    def __init__(self):
        self.is_allowed = True


def graph_database_window_cycle():
    window = psg.Window(
        title='Graph database'
        , layout=create_layout()
        , size=(600,500)
        , return_keyboard_events=True
        , keep_on_top=True)

    window.read(timeout=45)

    graph = window['_GRAPH_']
    drag = DragManager()
    spawn = SpawnManager()

    def zero_mouse_positions():
        graph.ClickPosition = (None, None)
        drag.start_pos = None
        drag.end_pos = None
        drag.is_active = False
        drag.object = None
        spawn.is_allowed = True

    def draw_circle_at_location(x, y, r=10, fc='white', lc='black', lw=1) -> int:
        if not spawn.is_allowed:
            return -1
        circle = graph.draw_circle(center_location=(x, y), radius=r, fill_color=fc, line_color=lc, line_width=lw)
        drag.object = circle
        spawn.is_allowed = False
        return circle

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break

        if '__TIMEOUT__' in event:
            continue

        if None not in graph.ClickPosition:
            print(f'click_position={graph.ClickPosition}')

        if event.startswith('_GRAPH_'):
            x, y = values['_GRAPH_']

            if event.endswith('+UP'):
                zero_mouse_positions()
                continue

            # current mouse movement, including an unmarked mouse down
            figures = graph.get_figures_at_location(location=(x, y))
            if len(figures) > 0:
                drag.object = figures[0]

            if drag.object:
                graph.relocate_figure(drag.object, x, y)
            else:
                draw_circle_at_location(x, y, 10)

        else:
            print('unhandled event: ', event, values)

    window.close()


if __name__ == '__main__':
    graph_database_window_cycle()
