from typing import List, Tuple
from rectangle import Rectangle
from bin import Bin
from utils import rotate_rectangles, pack_rectangles, generate_html

def pack_multiple_bins(rectangles: List[Rectangle], bins: List[Bin]) -> List[Tuple[Bin, List[Tuple[float, float, float, float]], float]]:
    """
    Pack rectangles into multiple bins, starting from the smallest bin.

    Args:
        rectangles (List[Rectangle]): The list of rectangles to pack.
        bins (List[Bin]): The list of bins to pack rectangles into.

    Returns:
        List[Tuple[Bin, List[Tuple[float, float, float, float]], float]]:
        A list of tuples, each containing a packed bin, cut lines, and total height used for that bin.
    """
    # Sort bins by width in ascending order (since height is no longer a factor)
    sorted_bins = sorted(bins, key=lambda b: b.width)
    
    results = []
    remaining_rectangles = rectangles.copy()

    for bin in sorted_bins:
        if not remaining_rectangles:
            break

        # Run the greedy algorithm for the current bin
        bin_result = run_greedy_algorithm(remaining_rectangles, bin)
        packed_bin, cut_lines, total_height = bin_result

        # Update the bin's used height
        packed_bin.used_height = total_height
        
        # Add the results for this bin
        results.append((packed_bin, cut_lines, total_height))
        
        # Update remaining rectangles
        packed_names = {rect.name for rect, _, _ in packed_bin.rectangles}
        remaining_rectangles = [rect for rect in remaining_rectangles if rect.name not in packed_names]

    # If there are still remaining rectangles, you might want to handle this case
    if remaining_rectangles:
        print(f"Warning: {len(remaining_rectangles)} rectangles could not be packed.")

    return results

def run_greedy_algorithm(rectangles: List[Rectangle], bin: Bin) -> Tuple[Bin, List[Tuple[float, float, float, float]], float]:
    """
    Run the greedy algorithm for a single bin and return the packed bin, cut lines, and total height.

    Args:
        rectangles (List[Rectangle]): The list of rectangles to pack.
        bin (Bin): The bin to pack rectangles into.

    Returns:
        Tuple[Bin, List[Tuple[float, float, float, float]], float]:
        A tuple containing the packed bin, cut lines, and total height used.
    """
    # Rotate rectangles if necessary for the current bin
    rotate_rectangles(rectangles, bin.width)
    
    # Run the greedy algorithm for the current bin
    packed_indices, _ = greedy_algorithm(rectangles, bin)
    
    # Pack the rectangles into the current bin
    packed_bin, cut_lines, total_height = pack_rectangles(packed_indices, rectangles, bin)
    
    return packed_bin, cut_lines, total_height

def greedy_algorithm(rectangles: List[Rectangle], bin: Bin) -> Tuple[List[int], List[int]]:
    """
    Implement a greedy algorithm for rectangle packing, prioritizing larger parts
    and ensuring cut pieces are placed next to each other.

    Args:
        rectangles (List[Rectangle]): The list of rectangles to pack.
        bin (Bin): The bin to pack rectangles into.

    Returns:
        Tuple[List[int], List[int]]: A tuple containing two lists of indices:
            1. Indices of packed rectangles
            2. Indices of remaining (unpacked) rectangles
    """
    # Sort rectangles by area (width * height) in descending order
    sorted_indices = sorted(range(len(rectangles)), key=lambda i: rectangles[i].width * rectangles[i].height, reverse=True)
    
    packed_indices = []
    remaining_indices = set(sorted_indices)
    current_width = 0
    current_height = 0
    max_row_height = 0

    while remaining_indices:
        best_fit = None
        best_fit_area = 0

        # Try to find a rectangle that fits in current row
        for idx in remaining_indices:
            rect = rectangles[idx]
            if rect.width <= bin.width - current_width:
                area = rect.width * rect.height
                if area > best_fit_area:
                    best_fit = idx
                    best_fit_area = area

        if best_fit is None:
            # If we can't find any rectangle that fits in current row
            if current_width == 0:  # If we're at the start of a row and still can't fit anything
                # No more rectangles can fit in the remaining height
                break
            
            # Start a new row
            current_width = 0
            current_height += max_row_height
            max_row_height = 0
            continue

        rect = rectangles[best_fit]
        packed_indices.append(best_fit)
        remaining_indices.remove(best_fit)

        # Update current_width and max_row_height
        current_width += rect.width
        max_row_height = max(max_row_height, rect.height)

        # Handle split parts
        if ':part1' in rect.name:
            # Force new line after ':part1'
            current_width = 0
            current_height += max_row_height
            max_row_height = 0

            # Find and pack ':part2'
            part2_name = rect.name.replace(':part1', ':part2')
            part2_idx = next((i for i in remaining_indices if rectangles[i].name == part2_name), None)
            if part2_idx is not None:
                rect_part2 = rectangles[part2_idx]
                if rect_part2.width <= bin.width:
                    packed_indices.append(part2_idx)
                    remaining_indices.remove(part2_idx)
                    current_width += rect_part2.width
                    max_row_height = max(max_row_height, rect_part2.height)
                else:
                    print(f"Cannot fit {rect_part2.name} in the bin after splitting.")
            else:
                print(f"Corresponding part2 for {rect.name} not found.")

    return packed_indices, list(remaining_indices)
    

if __name__ == "__main__":
    # Example usage
    bins = [
        Bin(98, 0, "Bin_98"),
        Bin(120, 1, "Bin_120"),
        Bin(150, 2, "Bin_150")
    ]
    rectangles = [
        Rectangle("Item1", 46.0, 93.0, False),
        Rectangle("Item2", 71.875, 93.0, False),
        Rectangle("Item3", 81.125, 110.0, False),
    ]

    results = pack_multiple_bins(rectangles, bins)

    for i, (bin, cut_lines, total_height) in enumerate(results):
        print(f"Bin {i+1}:")
        print(f"  Width: {bin.width}")
        print(f"  Total used height: {total_height}")
        print("  Packed rectangles:")
        for rect, x, y in bin.rectangles:
            print(f"    {rect.name} ({rect.width}x{rect.height}) packed at ({x}, {y})")
        print()
