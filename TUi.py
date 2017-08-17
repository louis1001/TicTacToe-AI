from scene import *
import sound
import random
import math
import dialogs
from TicTacToe import TTT
A = Action

def map_r(val, og_a, og_b, tg_a, tg_b, as_int = True):
    og_range = og_b - og_a
    constraint_val = val - og_a
    
    percent = constraint_val/og_range
    
    tg_range = tg_b - tg_a
    
    constraint_tg_val = percent * tg_range
    
    mapped = constraint_tg_val + tg_a
    
    if as_int:
        mapped= int(mapped)
    
    return mapped
   
values = ['X', '0', '', 'Nadie']
textures = {
    'Grid': Texture('resources/grid.JPG'),
    'X':    Texture('resources/IMG_0415_1.JPG'),
    '0':    Texture('resources/IMG_0416_1.JPG')
    }

pvp = False

def touching(node, touch):
    f = node.frame
    
    return f.contains_point(touch)

class SwitchNode (SpriteNode):
    
    def __init__():
        pass

class ButtonNode(LabelNode):
    
    def __init__(self, text, callback):
        LabelNode.__init__(self, text)
        self.callback = callback

    def touched(self, touch):
        self.callback()

class CellNode(SpriteNode):
    
    def __init__(self, index, p):
        SpriteNode.__init__(self)
        self.index = index
        
        self.x = index % 3
        self.y = int((index - self.x) / 3)
        
        self.scale = 0.75
        
        p_bounds = p.frame
        p_center = p_bounds.size/2
        
        #self.set_value(random.choice(["X", "0"]))
        
        x_mapped = map_r(self.x, 0, 2, -1, 1)
        y_mapped = map_r(self.y, 0, 2, 1, -1)
        
        self.position = (Size(64, 64) * Size(x_mapped, y_mapped))
        self.size = (60, 60)
        
        self.alpha = 0.0

    def set_value(self, txtr):
        self.texture = textures[txtr]
    
    def touched(self, touch):
        print("touched:", self.index)

class TableNode(SpriteNode):
    
    def __init__(self, ttt):
        SpriteNode.__init__(self)
        self.ttt = ttt
        self.turn = ttt.turn
        self.winner = ttt.who_won()
        
        self.position = Point(*(get_screen_size()/2).as_tuple())
        
        self.texture = textures['Grid']
        self.scale = 1.8
        
        self.grid = []
        
        self.fill_grid()
    
    def fill_grid(self):
        self.grid = [CellNode(x, self) for x in range(9)]
        
        for x in self.grid: self.add_child(x)
        
    def touched(self, touch):
        # Touch is just a location
        if self.winner != -1: return 1
        
        for x in self.grid:
            if touching(x, touch):
                if self.ttt.grid[x.index] == 2:
                    self.ttt.move(x.index)
    
    def update(self):
        global agent
        for x in range(9):
            curr_c = self.ttt.grid[x]
            curr_n = self.grid[x]
            if curr_c != 2 and not curr_n.texture:
                curr_n.alpha = 1.0
                curr_n.set_value(values[curr_c])
                
        self.turn = self.ttt.turn
        
        who_wins = self.ttt.who_won()
        
        if who_wins != -1:
            self.winner = who_wins
        
        if not pvp and who_wins == -1 and self.turn:
            if not agent:
                while True:
                    pc_r_move = random.randint(0,8)
                    if self.ttt.grid[pc_r_move] == 2:
                        self.ttt.move(pc_r_move)
                        break
            else:
                next_move = agent.guess(self.ttt.grid)
                self.ttt.move(next_move)
class MyScene (Scene):
    
    def setup(self):
        self.background_color = "#fff"
        self.nodes = []
        
        # Creating a reset button, from the custom ButtonNode class
        self.reset_button = ButtonNode("Reset", self.reset)
        self.reset_button.position = (40, get_screen_size().y - 20)
        self.reset_button.color = '#0987e5'
        self.reset_button.font = ('Cousine', 20)
        self.add_child(self.reset_button)
        self.nodes.append(self.reset_button)
        
        # The label that shows all information to the user
        info_lbl = LabelNode('Juego Iniciado')
        info_lbl.position = (30, get_screen_size().y - 80)
        info_lbl.anchor_point = (0.0, 1.0)
        info_lbl.color = '#0707c3'
        
        self.info = info_lbl
        self.add_child(info_lbl)
        
        # The switch for pvp or random game
        
        # Initializing the resetable settings of the game
        self.reset()
    
    def reset(self):
        self.ttt = TTT()
        self.TNode = TableNode(self.ttt)
        self.nodes.append(self.TNode)
        self.add_child(self.TNode)
    
    def update(self):
        self.TNode.update()
        
        t = self.ttt.turn
        self.info.text = "Es turno de " + values[t]
        
        if self.TNode.winner != -1:
            self.info.text = values[self.TNode.winner] + ' ganó!'
    
    def touch_began(self, touch):
        for x in self.nodes:
            if touching(x, touch.location):
                
                rel_location = (touch.location - x.position)/1.8
                
                x.touched(rel_location)
    
    def did_change_size(self):
        self.reset_button.position = (40, get_screen_size().y - 30)
        
        self.TNode.position = Point(*(get_screen_size()/2).as_tuple())
        
        self.info.position = (30, get_screen_size().y - 80)

agent = None

def show(agent_ = None):
    the_scene = MyScene()
    run(the_scene, show_fps=0)
    if agent_:
        agent = agent_

if __name__ == '__main__':
    show()
