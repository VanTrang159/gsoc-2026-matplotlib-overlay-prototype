class OverlayElement:
    def update(self, event):
        pass
    def draw(self, renderer):
        pass

class OverlayManager:
    def __init__(self):
        self.elements = []
    def add(self, element):
        self.elements.append(element)
    def remove(self, element):
        self.elements.remove(element)
    def update_all(self, event):
        for element in self.elements:
            element.update(event)
    def draw_all(self, renderer):
        for element in self.elements:
            element.draw(renderer)

class CrosshairOverlay(OverlayElement):
    pass

class CoordinateOverlay(OverlayElement):
    pass
