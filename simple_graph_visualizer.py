from enum import Enum, auto
import json
import os

import PySimpleGUI as psg
import networkx as nx
import numpy as np


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


def get_graph_height_pad():
    return 150


def create_layout(size=(400, 400)):
    bg_color = 'gainsboro'

    one_line_window_width = (size[0], 1)
    graph_size = (size[0], size[1] - get_graph_height_pad())

    gbl = (-size[0]/2, -size[1]/2)
    gbr = (size[0]/2, size[1]/2)
    return [
        # two things in one row
          [psg.Menu(create_menu_bar_layout(), tearoff=False)]
        , [psg.Frame('', create_toolbar_layout(), size=one_line_window_width)]
        , [psg.Text(key='_INFO_', size=one_line_window_width, background_color=bg_color)]
        , [psg.Text('Name'), psg.InputText(key='name.text', size=one_line_window_width)]
        , [psg.Text('Notes'), psg.InputText(key='notes.text', size=one_line_window_width)]
        , [psg.Graph(
              key='_GRAPH_'
            , canvas_size=graph_size
            , graph_bottom_left=gbl
            , graph_top_right=gbr
            , background_color=bg_color
            , change_submits=True
            , drag_submits=True)
        ]
    ]


def simple_graph_visualizer_window_cycle(file=None, title=None, layout=None, size=(600, 500)):
# ------------------------------------------------
    # this section contains program state
    DATA = {}

    if not title:
        title = 'Simple Graph Visualizer'

    if not layout:
        layout = create_layout(size)

    if not file:
        file = FILE_PATH

    window = psg.Window(title, layout, size=size, return_keyboard_events=True, resizable=True)
    window.read(timeout=45)
    window.bind('<Configure>', '_WINDOW_')

    mouse_state = EMouse.idle
    tool_state = ETool.add

# --------------------------------------------
    # this sections contains some fns we want encapsulated in our "object" (the graph visualizer)

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

    def prepare_data_for_save():
        nodes = DATA['nodes']
        for key in nodes.keys():
            if len(nodes[key]) >= 2 and nodes[key][2]:
                del nodes[key][2]
        if 'lookup' in nodes:
            del nodes['lookup']
        return True

    def shutdown_sequence():
        if not prepare_data_for_save():
            print('error preparing data for save!')
        result = write_file(FILE_PATH, DATA)
        if result:
            print(f'saved data to file: {FILE_PATH}')
        else:
            print(f'Error! Could not save file; path={FILE_PATH}, data={DATA}')
        window.close()

    def set_selected_node(name, note):
        window['name.text'].update(value=name)
        window['note.text'].update(value=note)

    def draw_subgraph(nodes, edges):
        for edge in edges:
            a, b = edge
            pos_a = nodes[a]
            pos_b = nodes[b]
            draw_edge(pos_a, pos_b)

        lookup = {}
        for key in nodes.keys():
            # this node needs to hold the circle_id, and the text_id
            ids = draw_node(nodes[key], key)
            nodes[key].append(ids)
            lookup[ids['circle_id']] = key
            lookup[ids['text_id']] = key

        nodes['lookup'] = lookup

    def draw_node(position, name):
        """returns a tuple of the circle id and then the text id.  These ideas will be reassigned each runtime
        so we have to retain and use them in memory, but we shouldn't write them to disk"""
        cid = window['_GRAPH_'].draw_circle(position, 25, fill_color='white', line_color='black')
        tid = window['_GRAPH_'].draw_text(name, position, color='black', text_location='center')
        return {'circle_id': cid, 'text_id': tid}

    def draw_edge(start, stop):
        window['_GRAPH_'].draw_line(start, stop)

# -------------------------------------------------------------
    # this is the section where we load data and test data integrity
    DATA = read_file(file)
    load_fail = f'Failed to load file: {file}'
    load_ok = f'File loaded: {file}'
    message = load_fail if 'load_failure' in DATA else load_ok
    window['_INFO_'].update(message)

    if 'nodes' not in DATA:
        DATA['nodes'] = {}
    if 'edges' not in DATA:
        DATA['edges'] = []
    # we delete this for a couple of reasons:
    # 1. the id's in this lookup are assigned each time the program is run,
    #       and possibly more often than that, so we can't rely on the ids in
    #       the last run to work for this run
    # 2. all the other keys in the 'nodes' section are meant to be actual nodes
    #       and unless that remains true, it complicates the process of iterating
    #       over them
    if 'lookup' in DATA['nodes']:
        del DATA['nodes']['lookup']

# -------------------------------------------------------
    # this section pre-loads the data from the last file
    draw_subgraph(DATA['nodes'], DATA['edges'])

# -------------------------------------------------------
    # this section is the application loop

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break

        if event == '__TIMEOUT__':
            mouse_state = EMouse.idle

        # window resize event
        if event == '_WINDOW_':
            size = window.get_screen_size()
            graph_size = (size[0], size[1] - get_graph_height_pad())
            window['_GRAPH_'].set_size(graph_size)

        # mouse down event on the graph
        elif event == '_GRAPH_':
            pos = values['_GRAPH_']
            if mouse_state == EMouse.idle:
                mouse_state = EMouse.down
                if tool_state == ETool.add:
                    DATA['nodes'][pos.__str__()] = pos
                    draw_node(pos, pos)
                else:
                    # right now, this just shows that each "node" contains multiple figure ids
                    #   1 - a cirlce
                    #   2 - the title text
                    # we're better off iterating these individually than trying to make it a tuple
                    figs = window['_GRAPH_'].get_figures_at_location(pos)
                    for f in figs:
                        node_name = DATA['nodes']['lookup'][f]
                        print(f'node looked up: {node_name}')

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

        # if it begins with 'toolbar'
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
