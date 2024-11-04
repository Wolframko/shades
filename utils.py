import json
from typing import List, Tuple, Dict
from rectangle import Rectangle
from bin import Bin

def rotate_rectangles(rectangles: List[Rectangle], bin_width: float) -> None:
    """
    Rotate rectangles based on their can_rotate value:
    - If can_rotate == 0: Do not rotate the rectangle.
    - If can_rotate == 1: Rotate the rectangle if its width > bin_width.
    - If can_rotate == 2: Must rotate the rectangle, regardless of its width.
    If after rotation, the rectangle's width > bin_width and can be split, split it.

    Args:
        rectangles (List[Rectangle]): The list of rectangles to process.
        bin_width (float): The width of the bin.
    """
    new_rectangles = []
    
    for rect in rectangles:
        if rect.can_rotate == 0:
            # Do not rotate
            if rect.width > bin_width:
                print(f"Rectangle {rect.name} is too wide for the bin and cannot be rotated.")
        elif rect.can_rotate == 1:
            # Rotate if width > bin_width
            if rect.width > bin_width:
                rect.rotate()
                if rect.width > bin_width:
                    print(f"Rectangle {rect.name} is too wide even after rotation. Splitting it.")
                    new_part = rect.split(bin_width)
                    if new_part:
                        new_part.is_rotated = rect.is_rotated
                        new_rectangles.append(new_part)
        elif rect.can_rotate == 2:
            # Must rotate without checking bin width
            rect.rotate()
            if rect.width > bin_width:
                print(f"Rectangle {rect.name} is too wide even after forced rotation. Splitting it.")
                new_part = rect.split(bin_width)
                if new_part:
                    new_part.is_rotated = rect.is_rotated
                    new_rectangles.append(new_part)
        else:
            print(f"Invalid can_rotate value {rect.can_rotate} for rectangle {rect.name}")
    
    rectangles.extend(new_rectangles)

def pack_rectangles(best_individual: List[int], rectangles: List[Rectangle], bin_width: float, bin_height: float) -> Tuple[Bin, List[Tuple[float, float, float, float]], float]:
    bin = Bin(bin_width, bin_height)
    cut_lines = []
    x, y = 0, 0
    max_height_in_row = 0
    force_new_line = False

    for idx in best_individual:
        rect = rectangles[idx]

        if force_new_line or x + rect.width > bin_width:
            # Start new row
            x = 0
            y += max_height_in_row
            max_height_in_row = 0
            force_new_line = False

        if y + rect.height > bin_height:
            print(f"Cannot fit rectangle {rect.name} in the bin.")
            continue  # Skip if the rectangle cannot fit in the bin

        bin.add_rectangle(rect, x, y)
        x += rect.width
        max_height_in_row = max(max_height_in_row, rect.height)

        if ':part1' in rect.name:
            force_new_line = True

    total_height = y + max_height_in_row
    return bin, cut_lines, total_height

def generate_html(bins: List[Bin], cut_lines: List[List[Tuple[float, float, float, float]]]) -> str:
    """
    Generate HTML to visualize the packed rectangles in multiple bins.

    Args:
        bins (List[Bin]): The list of bins containing packed rectangles.
        cut_lines (List[List[Tuple[float, float, float, float]]]): The list of cut lines for each bin.

    Returns:
        str: The generated HTML string for visualization.
    """
    data = {
        "bins": [bin.to_dict() for bin in bins],
        "cutLines": cut_lines
    }
    data_json = json.dumps(data)

    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rectangle Packing Visualization</title>
    <style>
        .container {{ position: relative; border: 2px solid black; margin-bottom: 20px; }}
        .rectangle {{ position: absolute; border: 1px solid black; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 12px; overflow: hidden; }}
        .arrow {{ font-size: 20px; line-height: 1; }}
        .bin-label {{ position: absolute; top: 5px; left: 5px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Rectangle Packing Visualization</h1>
    <div id="bins-container"></div>
    <script>
    (function() {{
        const data = {data_json};
        const binsContainer = document.getElementById('bins-container');
        const scale = 4;

        data.bins.forEach((bin, index) => {{
            const container = document.createElement('div');
            container.className = 'container';
            container.style.width = `${{bin.width * scale}}px`;
            container.style.height = `${{bin.used_height * scale}}px`;
            
            const binLabel = document.createElement('div');
            binLabel.className = 'bin-label';
            binLabel.textContent = `Bin ${{index + 1}} (${{bin.width}} x ${{bin.height}}) - Used Height: ${{bin.used_height}}`;
            container.appendChild(binLabel);

            bin.rectangles.forEach(({{"rectangle": rect, x, y}}) => {{
                const div = document.createElement('div');
                div.className = 'rectangle';
                Object.assign(div.style, {{
                    left: `${{x * scale}}px`,
                    top: `${{y * scale}}px`,
                    width: `${{rect.width * scale}}px`,
                    height: `${{rect.height * scale}}px`
                }});
                const arrow = rect.rotated ? '&#8594;' : '&#8595;'; // Right arrow for rotated, down arrow for not rotated
                div.innerHTML = `${{rect.name}}<br>${{rect.width}}x${{rect.height}}<br><span class="arrow">${{arrow}}</span>`;
                container.appendChild(div);
            }});

            binsContainer.appendChild(container);
        }});
    }})();
    </script>
</body>
</html>
'''
    return html

def save_bins_to_json(bins: List[Bin], filename: str) -> None:
    """
    Save the final data for multiple bins as JSON to a file.

    Args:
        bins (List[Bin]): The list of bins containing packed rectangles.
        filename (str): The name of the file to save the JSON data.
    """
    bins_data = {
        "bins": [
            {
                "width": bin.width,
                "height": bin.height,
                "used_height": bin.used_height,
                "rectangles": [
                    {
                        "rectangle": {
                            "name": rect.name,
                            "width": rect.width,
                            "height": rect.height,
                            "rotated": rect.is_rotated
                        },
                        "x": x,
                        "y": y
                    }
                    for rect, x, y in bin.rectangles
                ]
            }
            for bin in bins
        ]
    }

    with open(filename, 'w') as f:
        json.dump(bins_data, f, indent=2)
    print(f"Bins data saved to {filename}")

def load_input_data(filename: str) -> Tuple[List[Dict[str, float]], List[Rectangle]]:
    """
    Load input data from a JSON file containing multiple bins and rectangles.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        Tuple[List[Dict[str, float]], List[Rectangle]]: 
        A tuple containing a list of bin dictionaries and a list of Rectangle objects.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    
    bins = data['bins']
    rectangles = [Rectangle(**rect) for rect in data['rectangles']]
    
    return bins, rectangles

if __name__ == "__main__":
    bins, rectangles = load_input_data("testinput.json")
    print("Bins:")
    for bin in bins:
        print(f"  Width: {bin['width']}, Height: {bin['height']}")
    print("\nRectangles:")
    for rect in rectangles:
        print(f"  {rect.name}: {rect.width}x{rect.height}, Can rotate: {rect.can_rotate}")
