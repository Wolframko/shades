import unittest
import json
from rectangle import Rectangle
from bin import Bin
from greedy import pack_multiple_bins

class TestRectanglePacking(unittest.TestCase):
    def setUp(self):
        # Load test input data
        with open('testinput.json', 'r') as f:
            self.test_input = json.load(f)
        
        # Load expected output data
        with open('test_bin_data.json', 'r') as f:
            self.expected_output = json.load(f)

        # Create Rectangle objects from input data
        self.rectangles = [Rectangle(**rect) for rect in self.test_input['rectangles']]
        
        # Create Bin objects from input data
        self.bins = [Bin(bin_data['width'], bin_data['height']) for bin_data in self.test_input['bins']]

    def test_multiple_bins_packing(self):
        # Run the packing algorithm for multiple bins
        results = pack_multiple_bins(self.rectangles, self.bins)
        
        # Check if the number of packed bins is less than or equal to the expected output
        self.assertLessEqual(len(results), len(self.expected_output['bins']))
        
        for i, (packed_bin, cut_lines, total_height) in enumerate(results):
            expected_bin = self.expected_output['bins'][i]
            
            # Check bin dimensions
            self.assertEqual(packed_bin.width, expected_bin['width'])
            self.assertLessEqual(total_height, expected_bin['height'])
            
            # Check each packed rectangle
            for rect, x, y in packed_bin.rectangles:
                # Find the corresponding expected rectangle
                expected_rect = next((r['rectangle'] for r in expected_bin['rectangles'] if r['rectangle']['name'] == rect.name), None)
                if expected_rect:
                    self.assertEqual(rect.width, expected_rect['width'])
                    self.assertEqual(rect.height, expected_rect['height'])
                    self.assertEqual(rect.is_rotated, expected_rect.get('rotated', False))

    def test_bin_order(self):
        # Verify that bins are packed from smallest to largest
        results = pack_multiple_bins(self.rectangles, self.bins)
        bin_areas = [bin.width * bin.height for bin, _, _ in results]
        self.assertEqual(bin_areas, sorted(bin_areas))

    def test_rectangle_rotation(self):
        results = pack_multiple_bins(self.rectangles, self.bins)
        for packed_bin, _, _ in results:
            for rect, _, _ in packed_bin.rectangles:
                if not rect.can_rotate:
                    self.assertFalse(rect.is_rotated)

    def test_rectangle_splitting(self):
        results = pack_multiple_bins(self.rectangles, self.bins)
        all_packed_names = set()
        for packed_bin, _, _ in results:
            for rect, _, _ in packed_bin.rectangles:
                all_packed_names.add(rect.name.split(':')[0])  # Remove ':part1' or ':part2' if present
        
        # Check if all original rectangles are packed
        original_names = set(rect.name for rect in self.rectangles)
        self.assertEqual(all_packed_names, original_names)
        
        # Check if any rectangles were split
        split_rectangles = [name for name in all_packed_names if ':part' in name]
        if split_rectangles:
            for split_name in split_rectangles:
                base_name = split_name.split(':')[0]
                self.assertTrue(any(name.startswith(f"{base_name}:part") for name in all_packed_names))

    def test_bin_capacity(self):
        results = pack_multiple_bins(self.rectangles, self.bins)
        for packed_bin, _, total_height in results:
            self.assertLessEqual(total_height, packed_bin.height)
            for rect, x, y in packed_bin.rectangles:
                self.assertLessEqual(x + rect.width, packed_bin.width)
                self.assertLessEqual(y + rect.height, total_height)

    def test_all_rectangles_packed(self):
        results = pack_multiple_bins(self.rectangles, self.bins)
        packed_names = set()
        for packed_bin, _, _ in results:
            for rect, _, _ in packed_bin.rectangles:
                packed_names.add(rect.name.split(':')[0])  # Remove ':part1' or ':part2' if present
        original_names = set(rect.name for rect in self.rectangles)
        self.assertEqual(packed_names, original_names)

if __name__ == '__main__':
    unittest.main()