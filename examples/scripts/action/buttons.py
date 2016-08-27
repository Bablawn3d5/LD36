import entityx
from _entityx_components import Renderable, Body, Physics
from gamemath import vector2

Vector2 = vector2.Vector2
TILESIZE_X = 80
TILESIZE_Y = 60


class Button(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.physics.size.x = TILESIZE_X*3
        self.physics.size.y = TILESIZE_Y*1
        self.rend = self.Component(Renderable)
        self.rend.texture = "./images/button.png"
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
        self.updated = False

    def update(self, dt):
        # Do nothing.
        self.updated = True

class ButtonController(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
        self.init = False

    def update(self, dt):
        if (self.init == False):
            self.button1 = self.createButton(TILESIZE_X*0,TILESIZE_Y*2)
            self.button2 = self.createButton(TILESIZE_X*0,TILESIZE_Y*3)
            self.button3 = self.createButton(TILESIZE_X*0,TILESIZE_Y*4)
            self.button4 = self.createButton(TILESIZE_X*0,TILESIZE_Y*5)
            self.button5 = self.createButton(TILESIZE_X*0,TILESIZE_Y*6)
            self.button6 = self.createButton(TILESIZE_X*0,TILESIZE_Y*7)
            self.button7 = self.createButton(TILESIZE_X*0,TILESIZE_Y*8)
            self.button8 = self.createButton(TILESIZE_X*0,TILESIZE_Y*9)
            self.init = True

    def createButton(self, x, y):
        e = Button()
        e.body.position.x = x
        e.body.position.y = y
        return e

