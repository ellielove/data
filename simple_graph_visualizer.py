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
    select = auto()
    rename = auto()
    delete = auto()


class Node:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.circle_id = None
        self.text_id = None


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
          psg.Button('add',    key='toolbar.add')
        , psg.Button('move',   key='toolbar.move')
        , psg.Button('select', key='toolbar.select')
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

    mouse_pos = (0, 0)
    mouse_pos_last = None

    button_default_color = ('black', 'light gray')
    button_highlight_color = ('black', 'orange')

# --------------------------------------------
    # this sections contains some fns we want encapsulated in our "object" (the graph visualizer)

    # File Access --------------------------------------
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
        if 'lookup' in nodes:
            del nodes['lookup']
        return True

    # --------------------------------------

    def shutdown_sequence():
        if not prepare_data_for_save():
            print('error preparing data for save!')
        result = write_file(FILE_PATH, DATA)
        if result:
            print(f'saved data to file: {FILE_PATH}')
        else:
            print(f'Error! Could not save file; path={FILE_PATH}, data={DATA}')
        window.close()

    # graphing --------------------------------------

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

    def add_node(pos, name=None):
        if not name:
            name = pos.__str__()
        else:
            # we make a point to use strings here, b/c that's
            # how we ensure we can serialize it to json later
            if type(name) is tuple:
                name = name.__str__()

        fig_ids = draw_node(pos, name)
        # add node to area which is saved out. this must be a string
        DATA['nodes'][name] = pos

        # add two way lookups for node, so we can find the node in question, when
        # given a single figure id, and so we can find both figure ids, when given
        # a node.  This allows us to make sure we can delete the whole node at once,
        # even if we just get a single figure id (such as, just the id for the text)
        DATA['nodes']['lookup'][fig_ids['circle_id']] = name
        DATA['nodes']['lookup'][fig_ids['text_id']] = name
        DATA['nodes']['lookup'][name] = fig_ids

    def select_node(figure_id, name=None):
        # lookup node based on figure id
        # set that node as selected node
        # this fn can be called multiple times and stack
        pass

    def delete_node(figure_id, name=None):
        nodes = DATA['nodes']

        # find the name of this node, so we can delete it from graph.nodes
        if not name:
            if nodes['lookup']:
                if figure_id in nodes['lookup']:
                    name = nodes['lookup'][figure_id]
                    if not name:
                        print(f'ERROR! Could not find node connected to id: {figure_id}')
                else:
                    print(f'ERROR! Could not lookup id: {figure_id}')
                    print(f'DATA: {DATA}')

        # find the other ids we need to remove
        ids = [figure_id]
        if name in nodes['lookup']:
            figures = nodes['lookup'][name]
            ids.append(figures['circle_id'])
            ids.append(figures['text_id'])

        # delete figure from screen
        for id in ids:
            window['_GRAPH_'].DeleteFigure(id)
            # delete lookup for each id
            if id in nodes['lookup']:
                del nodes['lookup'][id]
        # delete lookup for node name
        if name in nodes['lookup']:
            del nodes['lookup'][name]
        # delete node from dict
        if name in nodes:
            del nodes[name]

    # state management --------------------------------------

    def set_mouse_state(state):
        nonlocal mouse_state
        mouse_state = state

    def get_button_key_from_tool_state(state):
        if state == ETool.add:
            return 'toolbar.add'
        elif state == ETool.move:
            return 'toolbar.move'
        elif state == ETool.select:
            return 'toolbar.select'
        elif state == ETool.rename:
            return 'toolbar.rename'
        elif state == ETool.delete:
            return 'toolbar.delete'
        else:
            print(f'ERROR! Did not recognize ETool state! "{state}"')
            return 'unknown'

    def set_button_color(key, color):
        window[key].update(button_color=color)

    def set_tool_state(state):
        nonlocal tool_state
        last_state = tool_state
        tool_state = state

        # set new state button to active
        key = get_button_key_from_tool_state(state)
        set_button_color(key, button_highlight_color)

        # set last state button to inactive
        key = get_button_key_from_tool_state(last_state)
        set_button_color(key, button_default_color)

    # program event handling -------------------------------------

    def handle_window_event__timeout(event, values):
        set_mouse_state(EMouse.idle)

    def handle_window_event__generic(event, values):
        # window resize event
        size = window.get_screen_size()
        graph_size = (size[0], size[1] - get_graph_height_pad())
        window['_GRAPH_'].set_size(graph_size)

    def handle_graph_event__mouse_while_down(event, values):
        """These events are some kind of mouse down event on the graph itself.  Usually, this is
        a mouse button down event, but it can also be a mouse move event.
        Mouse up events ARE NOT ALLOWED in this fn"""
        nonlocal mouse_state
        nonlocal tool_state
        nonlocal mouse_pos
        nonlocal mouse_pos_last

        # current mouse position, and mouse delta
        mouse_pos = values['_GRAPH_']
        delta = (0, 0)
        if mouse_pos_last:
            delta = (mouse_pos_last[0] - mouse_pos[0], mouse_pos_last[1] - mouse_pos[1])

        # handling mouse state
        if mouse_state == EMouse.idle or mouse_state == EMouse.up:
            set_mouse_state(EMouse.down)
            # check to see if we clicked on anything, and if we did, set that thing
            # as currently selected
            figs = window['_GRAPH_'].get_figures_at_location(mouse_pos)
            for f in figs:
                select_node(f, None)

        # handling tool state
        if tool_state == ETool.add:
            add_node(mouse_pos)

        elif tool_state == ETool.delete:
            figs = window['_GRAPH_'].get_figures_at_location(mouse_pos)
            for f in figs:
                delete_node(f, None)

        elif tool_state == ETool.move:
            # select one node
            return

        elif tool_state == ETool.select:
            # draw a bounding rect to select multiple
            return

        elif tool_state == ETool.rename:
            # launch a one-shot window to handle rename
            # take new name, and put
            return

        # else:
        #     if mouse_state == EMouse.dragging:
        #         window['_INFO_'].update(f'mouse_state: {mouse_state}')
        #         # right now, this just shows that each "node" contains multiple figure ids
        #         #   1 - a circle
        #         #   2 - the title text
        #         # we're better off iterating these individually than trying to make it a tuple
        #         figs = window['_GRAPH_'].get_figures_at_location(mouse_pos)
        #         for f in figs:
        #             window['_GRAPH_'].MoveFigure(f, delta[0], delta[1])
        #     else:
        #         mouse_state = EMouse.dragging
        #         window['_INFO_'].update(f'mouse_state: {mouse_state}')

        # cache last mouse interaction
        mouse_pos_last = mouse_pos

    def handle_mouse_up_event(event, values):
        set_mouse_state(EMouse.idle)
        window['_INFO_'].update(f'mouse_state: {mouse_state}')

        # move any node that's been dragged

    def handle_toolbar_event(event, values):
        if event.endswith('add'):
            set_tool_state(ETool.add)
        elif event.endswith('move'):
            set_tool_state(ETool.move)
        elif event.endswith('select'):
            set_tool_state(ETool.select)
        elif event.endswith('rename'):
            set_tool_state(ETool.rename)
        elif event.endswith('delete'):
            set_tool_state(ETool.delete)
        window['_INFO_'].update(f'Tool State: {tool_state}')


# Program startup -------------------------------------------------------------
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

    set_tool_state(ETool.select)

# -------------------------------------------------------
    # this section is the application loop

    while True:
        event, values = window.read(timeout=150)

        if event in (psg.WINDOW_CLOSED, 'Cancel', 'Escape:27'):
            break

        elif event == '__TIMEOUT__':
            handle_window_event__timeout(event, values)

        # window resize event
        elif event == '_WINDOW_':
            handle_window_event__generic(event, values)

        # mouse down event on the graph
        elif event == '_GRAPH_':
            handle_graph_event__mouse_while_down(event, values)

        # mouse up event
        elif event.endswith('+UP'):
            handle_mouse_up_event(event, values)

        # toolbar events
        elif event.startswith('toolbar'):
            handle_toolbar_event(event, values)

    shutdown_sequence()
