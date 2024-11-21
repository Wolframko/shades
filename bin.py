from typing import List, Tuple
from rectangle import Rectangle

class Bin:
    def __init__(self, width: float, bin_id: int, name: str = ""):
        self.width = width
        self.id = bin_id
        self.name = name
        self.used_height: float = 0  # Track actual used height
        self.rectangles: List[Tuple[Rectangle, float, float]] = []

    def add_rectangle(self, rectangle: Rectangle, x: float, y: float):
        self.rectangles.append((rectangle, x, y))
        self.used_height = max(self.used_height, y + rectangle.height)

    def clear(self):
        self.rectangles.clear()
        self.used_height = 0

    def get_total_height(self) -> float:
        return self.used_height

    def to_dict(self):
        return {
            "width": self.width,
            "used_height": self.used_height,
            "rectangles": [
                {
                    "rectangle": rect.to_dict(),
                    "x": x,
                    "y": y
                } for rect, x, y in self.rectangles
            ]
        }
