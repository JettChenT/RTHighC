import pygame

class Label:
    def __init__(self, x, y, bg, fSize, fClr, fntName=None, autoSize=True, w=0, h=0, align="left",
                 txt='text'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = pygame.font.Font(fntName, fSize)
        self.bg = bg
        self.rect = (self.x, self.y, self.w, self.h)
        self.fClr = fClr
        self.autoSize = autoSize
        self.txt = txt
        self.align = align
        self.pic = None
        self.fx = self.fy = 0
        self.alignD = {
            'left': lambda: (self.x + 10, self.y + 10),
            'middle': lambda: (self.x + self.w // 2 - self.pic.get_width() // 2, self.y + 10),
            'right': lambda: (self.x + self.w - self.pic.get_width() - 10, self.y + 10)
        }
        self.focused = False
        self.render()

    def inside(self, tx, ty) -> bool:
        return (0 <= (tx - self.x) <= self.rect[2]) and (0 <= (ty - self.y) <= self.rect[3])

    def render(self):
        self.pic = self.font.render(self.txt, True, self.fClr)
        if self.autoSize:
            self.w = self.pic.get_width() + 20
            self.h = self.pic.get_height() + 20
            self.rect = (self.x, self.y, self.w, self.h)
        self.fx, self.fy = self.alignD[self.align]()

    def draw(self, scr):
        if self.bg:
            pygame.draw.rect(scr, self.bg, self.rect)
        scr.blit(self.pic, (self.fx, self.fy))

    def recv_key(self,key):
        pass

    def recv_mouse(self,tx,ty):
        pass

    def tick(self):
        pass

    def focus(self):
        self.focused = True

    def deFocus(self):
        self.focused = False

    def update(self, txt):
        self.txt = txt
        self.render()

    def __str__(self):
        return str(self.txt)

    def __len__(self):
        return len(self.txt)


class TextBox(Label):
    def __init__(self, x, y, fntName=None, autoSize=True, w=0, h=0, align="left", bg='white', fClr='black', fSize=32,
                 pad=5):
        super().__init__(x, y, bg, fSize, fClr, fntName, autoSize, w, h, align, txt="")
        self.pointer = 0
        self.enterFunc = lambda: None
        self.pad = pad
        self.cnt = 0

    def drawCurser(self, scr):
        if self.cnt>=50 or (not self.focused):
            return
        t = self.font.render(self.txt[:self.pointer], True, self.fClr)
        w, h = t.get_width() + 10, t.get_height()
        pygame.draw.line(scr, self.fClr, (self.rect[0] + w, self.rect[1] + 10),
                         (self.rect[0] + w, self.rect[1] + h + 10))

    def drawSide(self, scr):
        p = self.pad
        a = self.rect[0] - p
        b = self.rect[1] - p
        c = a + self.rect[2] + 2 * p
        d = b + self.rect[3] + 2 * p
        tl = (a, b)
        tld = (a + p, b + p)
        tr = (c, b)
        trd = (c - p, b + p)
        bl = (a, d)
        bld = (a + p, d - p)
        br = (c, d)
        brd = (c - p, d - p)
        pygame.draw.polygon(scr, (128, 128, 128), (tl, tld, trd, tr))
        pygame.draw.polygon(scr, (128, 128, 128), (tr, trd, brd, br))
        pygame.draw.polygon(scr, (192, 192, 192), (bl, bld, brd, br))
        pygame.draw.polygon(scr, (192, 192, 192), (tl, tld, bld, bl))

    def draw(self, scr):
        self.drawSide(scr)
        super().draw(scr)
        self.drawCurser(scr)

    def recv_key(self, key):
        if key == pygame.K_RIGHT:
            self.pointer += 1
            if self.pointer == len(self.txt) + 1:
                self.pointer -= 1
        elif key == pygame.K_LEFT:
            self.pointer -= 1
            if self.pointer == -1:
                self.pointer += 1
        elif key == pygame.K_BACKSPACE:
            self.update(self.txt[:self.pointer - 1] + self.txt[self.pointer:])
            self.pointer -= 1
            if self.pointer == -1:
                self.pointer += 1
        elif key == pygame.K_KP_ENTER:
            self.enterFunc()
        elif chr(key).isalnum() or key == pygame.K_SPACE:
            self.update(self.txt[:self.pointer] + chr(key) + self.txt[self.pointer:])
            self.pointer += 1

    def link_enter(self, func):
        self.enterFunc = func

        def inn(*args, **kwargs):
            func(*args, **kwargs)

        return inn

    def tick(self):
        self.cnt = (self.cnt+1)%100

    def recv_mouse(self,tx,ty):
        if not self.inside(tx,ty):
            return False
        self.cnt = 0
        # dx = tx-self.x
        # minx = float("inf")
        # minN = -1
        # for n in range(-1,len(self.txt)):
        #     curW = self.font.render(self.txt[:n+1], True, self.fClr).get_width()
        #     if abs((curW - self.x)-dx)<minx:
        #         minx = abs((curW - self.x)-dx)
        #         minN = n
        # self.pointer = minN-1

class Window:
    def __init__(self):
        self.components = []
        self.focus = -1
        self.map = dict()

    def __len__(self):
        return len(self.components)

    def render(self):
        for component in self.components:
            component.render()

    def draw(self,scr):
        for component in self.components:
            component.draw(scr)

    def recv_key(self,key):
        self.components[self.focus].recv_key(key)

    def tick(self):
        for component in self.components:
            component.tick()

    def recv_mouse(self,tx,ty):
        for i in range(len(self.components)):
            component = self.components[i]
            if component.inside(tx,ty):
                component.focus()
                self.focus = i
                component.recv_mouse(tx,ty)
            else:
                component.deFocus()

    def add_component(self,component,id=''):
        self.components.append(component)
        if id != '':
            self.map[id] = len(self.components)-1

    def __getitem__(self, item):
        if type(item) == int:
            return self.components[item]
        elif type(item) == str:
            return self.components[self.map[item]]