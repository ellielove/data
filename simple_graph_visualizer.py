from enum import Enum, auto
import json
import os

import PySimpleGUI as psg
import networkx as nx
import numpy as np

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


FILE_PATH = 'test.graph.json'


class EMouse(Enum):
    idle = auto()
    down = auto()
    dragging = auto()
    up = auto()


class ETool(Enum):
    add = auto()
    move = auto()
    rename = auto()
    delete = auto()


def get_test_nodes() -> dict:
    return {
          'A': (0,  0)
        , 'B': (200,  200)
        , 'C': (-200, -200)
        , 'D': (200, -200)
        , 'E': (-200,  200)
    }


def get_test_edges():
    return [
          ('A', 'B'), ('A', 'C')
        , ('B', 'C')
        , ('C', 'D')
        , ('D', 'E')
    ]


def create_menu_bar_layout():
    return [
        ['&File', ['New', '&Open', 'Save', '&SaveAs', '----', 'Settings', 'E&xit']]
    ]


def create_toolbar_layout():
    psg.set_options(auto_size_buttons=True, margins=(0, 0), button_color=psg.COLOR_SYSTEM_DEFAULT)
    return [[
          psg.Button('add', key='toolbar.add')
        , psg.Button('move', key='toolbar.move')
        , psg.Button('rename', key='toolbar.rename')
        , psg.Button('delete', key='toolbar.delete')
    ]]


def create_layout(size=(400, 400)):
    bg_color = 'gainsboro'
    ts = (size[0]-10, 1)
    gcs = (size[0], size[1]-90)
    gbl = (-size[0]/2, -size[1]/2)
    gbr = (size[0]/2, size[1]/2)
    return [
        # two things in one row
          [psg.Menu(create_menu_bar_layout(), tearoff=False)]
        , [psg.Frame('', create_toolbar_layout(), size=(size[0], 1))]
        , [psg.Graph(
              key='_GRAPH_'
            , canvas_size=gcs
            , graph_bottom_left=gbl
            , graph_top_right=gbr
            , background_color=bg_color
            , change_submits=True
            , drag_submits=True)]
        , [psg.Text(key='_INFO_', size=ts, background_color=bg_color)]
    ]


def simple_graph_visualizer_window_cycle(file=None, title=None, layout=None, size=(600, 500)):
    DATA = {}

    if not title:
        title = 'Simple Graph Visualizer'

    if not layout:
        layout = create_layout(size)

    if not file:
        file = FILE_PATH

    window = psg.Window(title, layout, size=size, return_keyboard_events=True)
    window.read(timeout=45)

    mouse_state = EMouse.idle
    tool_state = ETool.add

    def read_file(path) -> dict:
        """returns dict of json data, or returns dict with load_faliure:true as a key"""
        if path is not None:
            if os.path.isfile(path):
                with open(path, 'r') as infile:
                    result = json.load(infile)
                    # NOTE: right now, this handles a situation where a file is marked as failing
                    # to load, and accidentally gets saved that way.  We might need a better way to
                    # handle the problem though
                    if 'load_failure' in result:
                        del result['load_failure']
                    return result
        return {'load_failure': True}

    def write_file(path, data) -> bool:
        if path is not None:
            with open(path, 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
        return os.path.isfile(path)

    def shutdown_sequence():
        result = write_file(FILE_PATH, DATA)
        if result:
            print(f'saved data to file: {FILE_PATH}')
        else:
            print(f'Error! Could not save file; path={FILE_PATH}, data={DATA}')
        window.close()

    def draw_subgraph(nodes, edges):
        for edge in edges:
            a, b = edge
            pos_a = nodes[a]
            pos_b = nodes[b]
            draw_edge(pos_a, pos_b)

        for key in nodes.keys():
            draw_node(nodes[key], key)

    def draw_node(position, name):
        window['_GRAPH_'].draw_circle(position, 25, fill_color='white', line_color='black')
        window['_GRAPH_'].draw_text(name, position, color='black', text_location='center')

    def draw_edge(start, stop):
        window['_GRAPH_'].draw_line(start, stop)


    DATA = read_file(file)
    load_fail = f'Failed to load file: {file}'
    load_ok = f'File loaded: {file}'
    message = load_fail if 'load_failure' in DATA else load_ok
    window['_INFO_'].update(message)

    #if message == load_fail:
    #    DATA['nodes'] = get_test_nodes()
    #    DATA['edges'] = get_test_edges()

    if 'nodes' not in DATA:
        DATA['nodes'] = {}
    if 'edges' not in DATA:
        DATA['edges'] = []

    draw_subgraph(DATA['nodes'], DATA['edges'])

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break

        # mouse down event on the graph
        elif event == '_GRAPH_':
            x, y = values['_GRAPH_']
            if mouse_state == EMouse.idle:
                mouse_state = EMouse.down
                pos = (x, y)
                if tool_state == ETool.add:
                    DATA['nodes'][pos.__str__()] = pos
                    draw_node(pos, pos)
                # elif move
                # elif rename
                # elif delete

            elif mouse_state == EMouse.dragging:
                continue

        # mouse up event
        elif event.endswith('+UP'):
            mouse_state = EMouse.idle
            info = window['_INFO_']
            info.update(f'placed node at {pos}')

        # if it begins with toolbar
        elif event[::-1].endswith('toolbar'[::-1]):
            if event.endswith('add'):
                tool_state = ETool.add
            elif event.endswith('move'):
                tool_state = ETool.move
            elif event.endswith('rename'):
                tool_state = ETool.rename
            elif event.endswith('delete'):
                tool_state = ETool.delete
            window['_INFO_'].update(f'Tool State: {tool_state}')


    shutdown_sequence()
