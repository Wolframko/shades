import json
from typing import List, Tuple, Dict
from rectangle import Rectangle
from bin import Bin

def rotate_rectangles(rectangles: List[Rectangle], bin_width: float) -> None:
    """
    Rotate rectangles if their width is greater than bin_width and they can be rotated.
    If a rectangle is still too wide after rotation and can rotate, it is split.

    Args:
        rectangles (List[Rectangle]): The list of rectangles to process.
        bin_width (float): The width of the bin.
    """
    new_rectangles = []
    
    for rect in rectangles:
        if rect.width > bin_width:
            if rect.can_rotate:
                if rect.height <= bin_width:
                    rect.rotate()
                elif rect.width > bin_width and rect.height > bin_width:
                    print(f"Rectangle {rect.name} is too wide and tall for the bin. Splitting it.")
                    rect.rotate()
                    new_part = rect.split(bin_width)
                    new_part.is_rotated = True
                    if new_part:
                        if new_part.width < 10:
                            new_part.width = 10
                        new_rectangles.append(new_part)
            else:
                print(f"Rectangle {rect.name} is too wide for the bin and cannot be rotated or split.")
    
    rectangles.extend(new_rectangles)

def pack_rectangles(best_individual: List[int], rectangles: List[Rectangle], bin_width: float, bin_height: float) -> Tuple[Bin, List[Tuple[float, float, float, float]], float]:
    """
    Pack rectangles according to the best individual found by the algorithm.

    Args:
        best_individual (List[int]): The best individual (solution) found by the algorithm.
        rectangles (List[Rectangle]): The list of rectangles to pack.
        bin_width (float): The width of the bin.
        bin_height (float): The height of the bin.

    Returns:
        Tuple[Bin, List[Tuple[float, float, float, float]], float]: 
        A tuple containing the packed bin, the cut lines, and the total height used.
    """
    bin = Bin(bin_width, bin_height)
    cut_lines = []
    x, y, max_height = 0, 0, 0

    for gene in best_individual:
        rect = rectangles[gene]
        if x + rect.width > bin_width:
            cut_lines.append((0, y, bin_width, y))
            x, y = 0, y + max_height
            max_height = 0
        
        bin.add_rectangle(rect, x, y)
        cut_lines.append((x, y, x, y + rect.height))
        x += rect.width
        max_height = max(max_height, rect.height)

    cut_lines.append((0, y + max_height, bin_width, y + max_height))
    total_height = y + max_height
    
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
