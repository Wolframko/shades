class Rectangle:
    """
    Represents a rectangle with properties such as name, width, height, and rotation capabilities.
    """
    __slots__ = ['name', 'width', 'height', 'can_rotate', 'is_rotated']
    def __init__(self, name: str, width: float, height: float, can_rotate: int):
        """
        Initialize a Rectangle object.

        Args:
            name (str): The name of the rectangle.
            width (float): The width of the rectangle.
            height (float): The height of the rectangle.
            can_rotate (int): Rotation behavior (0: cannot rotate, 1: can rotate if needed, 2: must rotate).
        """
        self.name = name
        self.width = width
        self.height = height
        self.can_rotate = can_rotate
        self.is_rotated = False

    def rotate(self):
        """
        Rotate the rectangle.
        """
        self.width, self.height = self.height, self.width
        self.is_rotated = not self.is_rotated

    def split(self, max_width: float):
        """
        Split the rectangle if its width exceeds the maximum width.

        Args:
            max_width (float): The maximum allowed width.

        Returns:
            Rectangle or None: A new Rectangle object representing the excess part if split, None otherwise.
        """
        if self.width <= max_width:
            return None
        excess_width = self.width - max_width
        if excess_width < 10:
            excess_width = 10
        # Rename the original rectangle to include ':part1'
        self.name = f"{self.name}:part1"
        new_part = Rectangle(f"{self.name.replace(':part1', ':part2')}", excess_width, self.height, self.can_rotate)
        self.width = max_width
        return new_part

    def to_dict(self):
        """
        Convert the Rectangle object to a dictionary.

        Returns:
            dict: A dictionary representation of the Rectangle.
        """
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "rotated": self.is_rotated,
            "can_rotate": self.can_rotate  # Ensure can_rotate is included when saving
        }
