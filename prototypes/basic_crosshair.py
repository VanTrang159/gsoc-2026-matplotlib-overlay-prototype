class OverlayElement:
    def update(self, event):
        pass
    def draw(self, canvas):
        pass

class OverlayManager:
    def __init__(self):
        self.elements = []
    def add(self, element):
        self.elements.append(element)
    def on_mouse_move(self, event):
        for element in self.elements:
            element.update(event)
    def draw_all(self, canvas):
        for element in self.elements:
            element.draw(canvas)

class CrosshairOverlay(OverlayElement):
    def update(self, event):
        pass
