import tkinter as tk

from graph import Graph


OVAL_RADIUS = 15
DEFAULT_NODE_MODE = 'd'
START_NODE_MODE = 's'
END_NODE_MODE = 'e'
MODE_LIST = {
    DEFAULT_NODE_MODE: 'Add default node',
    START_NODE_MODE: 'Add starting node',
    END_NODE_MODE: 'Add end node'
}

def get_instruction_text():
    instruction_text = ''
    for key, value in MODE_LIST.items():
        instruction_text += f'Press "{key}" to {value}\n'
    return instruction_text

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title('Path Calculator')
        self.master.geometry('800x600')

        self.add_node_mode = DEFAULT_NODE_MODE

        self.create_widgets()

        self.prev_node = None

        self.nodes = []
        self.start_nodes = []
        self.end_nodes = []
        self.node_stack = []

    def create_widgets(self):
        self.calculate = tk.Button(self)
        self.calculate['text'] = 'Calculate total paths'
        self.calculate['command'] = self.calculate_n_paths
        self.calculate.pack(side='top')

        self.lbl_result = tk.Label(self, text='None')
        self.lbl_result.pack(side='top')
        
        instruction_text = get_instruction_text()
        self.lbl_instruction = tk.Label(self, text=instruction_text)
        self.lbl_instruction.pack(side='top')
        
        self.lbl_information = tk.Label(self, text=f'Mode: {MODE_LIST[self.add_node_mode]}')
        self.lbl_information.pack(side='top')

        self.canvas = tk.Canvas(width=800, height=400)
        self.canvas.create_text(200, 50, fill="darkblue",font="Times 12 bold",
                        text="Left click to create node, right click to connect nodes.")
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.set_mode)
        self.canvas.bind('<Button-1>', self.add_node)
        self.canvas.bind('<Button-3>', self.connect_node)
        self.canvas.pack(expand=True)

        self.quit = tk.Button(self, text='QUIT', fg='red',
                              command=self.master.destroy)
        self.quit.pack(side='bottom')

    def set_mode(self, event):
        event_char = event.char.lower()
        self.add_node_mode = event_char
        if event_char not in MODE_LIST.keys():
            self.add_node_mode = DEFAULT_NODE_MODE
        self.lbl_information.configure(text=f'Mode: {MODE_LIST[self.add_node_mode]}')
        

    def add_node(self, event):
        x = event.x
        y = event.y
        if self.add_node_mode == DEFAULT_NODE_MODE:
            fill_color = 'yellow'
        elif self.add_node_mode == START_NODE_MODE:
            fill_color = 'green'
        elif self.add_node_mode == END_NODE_MODE:
            fill_color = 'red'
        Graph.id = self.canvas.create_oval(x-(OVAL_RADIUS/2), y-(OVAL_RADIUS/2), x+(OVAL_RADIUS/2), y+(OVAL_RADIUS/2), fill=fill_color)
        g = Graph()
        self.nodes.append(g)
        if self.add_node_mode == START_NODE_MODE:
            self.start_nodes.append(g)
        elif self.add_node_mode == END_NODE_MODE:
            self.end_nodes.append(g)
        print(f'Create new node {Graph.id} at position {x}, {y}')
        print(f'Current nodes are: {self.nodes}')
        print(f'Current start nodes are: {self.start_nodes}')
        print(f'Current end nodes are: {self.end_nodes}')

    def connect_node(self, event):
        x = event.x
        y = event.y
        object_ids = event.widget.find_overlapping(x, y, x+1, y+1)
        node_id = []
        for id in object_ids:
            if self.canvas.type(id) == 'oval':
                node_id = (id,)
            else:
                node_id = None
        node = self.nodes[self.nodes.index(f'G-{node_id[0]:03d}')] if node_id else None

        if node:
            if self.prev_node:
                if self.prev_node != node:
                    prev_node_pos = self.canvas.coords(self.prev_node.id)
                    curr_node_pos = self.canvas.coords(node_id)
                    print(f'Connecting nodes {self.prev_node} ({prev_node_pos}) and {node} ({curr_node_pos})')
                    self.canvas.create_line(
                        prev_node_pos[0]+(OVAL_RADIUS/2), prev_node_pos[1]+(OVAL_RADIUS/2),
                        curr_node_pos[0]+(OVAL_RADIUS/2), curr_node_pos[1]+(OVAL_RADIUS/2)
                        )
                    self.prev_node.add_child(node)
                else:
                    print('Please select another node!')
                self.prev_node = None
            else:
                self.prev_node = node
                print(f'Selecting node {node} at position {x}, {y}')
        else:
            self.prev_node = None

    def calculate_n_paths(self):
        count = 0
        self.node_stack = self.start_nodes.copy()

        print('Start:', self.start_nodes)
        print('End:', self.end_nodes)
        print('Stack:', self.node_stack)

        while len(self.node_stack) > 0:
            node = self.node_stack.pop()
            if node in self.end_nodes:
                count += 1
            else:
                self.node_stack.extend(node.children)
            # print('Stack:', self.node_stack)

        self.lbl_result.configure(text=count)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
