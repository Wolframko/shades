import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QGroupBox, QFileDialog, QTextEdit, QScrollArea, QListWidget, QMessageBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json
import pandas as pd
from utils import rotate_rectangles, pack_rectangles, generate_html, save_bins_to_json

# Assuming the Rectangle class is defined in a separate file
from rectangle import Rectangle
from greedy import pack_multiple_bins
from bin import Bin

class RectanglePackingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectangle Packing GUI")
        self.setGeometry(100, 100, 1200, 800)

        self.rectangles = []
        self.bins = []
        self.create_widgets()

    def create_widgets(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Bin management frame
        bin_group = QGroupBox("Bin Management")
        bin_layout = QVBoxLayout(bin_group)

        bin_width_layout = QHBoxLayout()
        bin_width_layout.addWidget(QLabel("Bin Width:"))
        self.bin_width_entry = QLineEdit()
        bin_width_layout.addWidget(self.bin_width_entry)
        bin_layout.addLayout(bin_width_layout)

        bin_height_layout = QHBoxLayout()
        bin_height_layout.addWidget(QLabel("Bin Height:"))
        self.bin_height_entry = QLineEdit()
        bin_height_layout.addWidget(self.bin_height_entry)
        bin_layout.addLayout(bin_height_layout)

        add_bin_button = QPushButton("Add Bin")
        add_bin_button.clicked.connect(self.add_bin)
        bin_layout.addWidget(add_bin_button)

        self.bin_list = QListWidget()
        bin_layout.addWidget(self.bin_list)

        remove_bin_button = QPushButton("Remove Selected Bin")
        remove_bin_button.clicked.connect(self.remove_bin)
        bin_layout.addWidget(remove_bin_button)

        left_layout.addWidget(bin_group)

        # Rectangle management frame
        rect_group = QGroupBox("Rectangle Management")
        rect_layout = QVBoxLayout(rect_group)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_entry = QLineEdit()
        name_layout.addWidget(self.name_entry)
        rect_layout.addLayout(name_layout)

        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_entry = QLineEdit()
        width_layout.addWidget(self.width_entry)
        rect_layout.addLayout(width_layout)

        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_entry = QLineEdit()
        height_layout.addWidget(self.height_entry)
        rect_layout.addLayout(height_layout)

        self.can_rotate_var = QCheckBox("Can Rotate")
        rect_layout.addWidget(self.can_rotate_var)

        add_button = QPushButton("Add Rectangle")
        add_button.clicked.connect(self.add_rectangle)
        rect_layout.addWidget(add_button)

        self.rect_table = QTableWidget()
        self.rect_table.setColumnCount(4)
        self.rect_table.setHorizontalHeaderLabels(["Name", "Width", "Height", "Can Rotate"])
        self.rect_table.itemSelectionChanged.connect(self.on_select_rectangle)
        self.rect_table.cellChanged.connect(self.on_cell_changed)
        rect_layout.addWidget(self.rect_table)

        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_rectangle)
        rect_layout.addWidget(remove_button)

        left_layout.addWidget(rect_group)

        # File operations
        file_layout = QHBoxLayout()
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        file_layout.addWidget(save_button)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        file_layout.addWidget(load_button)

        left_layout.addLayout(file_layout)

        # Run algorithm button
        run_greedy_button = QPushButton("Run Greedy Algorithm")
        run_greedy_button.clicked.connect(self.run_greedy_algorithm)
        left_layout.addWidget(run_greedy_button)

        # Results frame
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)

        right_layout.addWidget(results_group)

        # Add WebView
        self.webview = QWebEngineView()
        self.webview.setMinimumSize(600, 700)
        right_layout.addWidget(self.webview)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def add_bin(self):
        try:
            width = float(self.bin_width_entry.text())
            height = float(self.bin_height_entry.text())
        except ValueError:
            print("Invalid input for bin dimensions")
            return

        bin = Bin(width, height)
        self.bins.append(bin)
        self.update_bin_list()
        self.clear_bin_inputs()

    def update_bin_list(self):
        self.bin_list.clear()
        for bin in self.bins:
            self.bin_list.addItem(f"Bin: {bin.width} x {bin.height}")

    def clear_bin_inputs(self):
        self.bin_width_entry.clear()
        self.bin_height_entry.clear()

    def remove_bin(self):
        current_row = self.bin_list.currentRow()
        if current_row >= 0:
            del self.bins[current_row]
            self.update_bin_list()

    def save_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if filename:
            data = {
                "bins": [{"width": b.width, "height": b.height} for b in self.bins],
                "rectangles": [{"name": r.name, "width": r.width, "height": r.height, "can_rotate": r.can_rotate} for r in self.rectangles]
            }
            with open(filename, "w") as f:
                json.dump(data, f)

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json);;Excel Files (*.xlsx *.xls)")
        if filename:
            if filename.endswith(('.json')):
                with open(filename, "r") as f:
                    data = json.load(f)
                self.bins = [Bin(b["width"], b["height"]) for b in data["bins"]]
                self.rectangles = [Rectangle(**r) for r in data["rectangles"]]
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filename, header=None)
                if df.shape[1] < 2:
                    print("Excel file must have at least two columns: width and height")
                    return
                self.rectangles = [Rectangle(f"Rect_{i+1}", row[0], row[1], False) for i, row in df.iterrows()]
            else:
                print("Unsupported file format")
                return
            
            self.update_bin_list()
            self.update_rectangle_list()

    def run_greedy_algorithm(self):
        if not self.bins:
            print("No bins added")
            return

        # Reload rectangles from the GUI table
        self.rectangles = []
        for row in range(self.rect_table.rowCount()):
            name = self.rect_table.item(row, 0).text()
            width = float(self.rect_table.item(row, 1).text())
            height = float(self.rect_table.item(row, 2).text())
            can_rotate = self.rect_table.cellWidget(row, 3).isChecked()
            rectangle = Rectangle(name, width, height, can_rotate)
            self.rectangles.append(rectangle)

        if not self.rectangles:
            print("No rectangles added")
            return

        results = pack_multiple_bins(self.rectangles, self.bins)
        
        # Check if all rectangles were packed
        all_packed_rectangles = [rect for bin, _, _ in results for rect, _, _ in bin.rectangles]
        unpacked_rectangles = [rect for rect in self.rectangles if rect not in all_packed_rectangles]
        
        if unpacked_rectangles:
            warning_message = "The following rectangles could not be packed:\n"
            for rect in unpacked_rectangles:
                warning_message += f"- {rect.name} ({rect.width}x{rect.height})\n"
            
            QMessageBox.warning(self, "Packing Warning", warning_message)

        self.display_results(results)

    def display_results(self, results):
        self.results_text.clear()
        for i, (bin, cut_lines, total_height) in enumerate(results):
            self.results_text.append(f"Bin {i+1}:")
            self.results_text.append(f"  Width: {bin.width}, Height: {bin.height}")
            self.results_text.append(f"  Total used height: {total_height}")
            self.results_text.append("  Packed rectangles:")
            for rect, x, y in bin.rectangles:
                rotation_status = "rotated" if rect.is_rotated else "not rotated"
                self.results_text.append(f"    {rect.name} ({rect.width}x{rect.height}) packed at ({x}, {y}) - {rotation_status}")
            self.results_text.append("")

        # Generate HTML and display in WebView
        html_content = generate_html([bin for bin, _, _ in results], [cut_lines for _, cut_lines, _ in results])
        with open('output.html', 'w') as f:
            f.write(html_content)
        print("HTML content saved to 'output.html'")
        self.webview.setHtml(html_content, QUrl.fromLocalFile(QGuiApplication.applicationDirPath()))
        self.webview.show()
        print("HTML content set to webview")

        # Save the final bin data as JSON
        save_bins_to_json([bin for bin, _, _ in results], "final_bin_data.json")

    def add_rectangle(self):
        name = self.name_entry.text()
        try:
            width = float(self.width_entry.text())
            height = float(self.height_entry.text())
        except ValueError:
            print("Invalid input for width or height")
            return

        can_rotate = self.can_rotate_var.isChecked()

        rectangle = Rectangle(name, width, height, can_rotate)
        self.rectangles.append(rectangle)
        self.update_rectangle_list()
        self.clear_rectangle_inputs()

    def update_rectangle_list(self):
        self.rect_table.setRowCount(len(self.rectangles))
        for i, rect in enumerate(self.rectangles):
            self.rect_table.setItem(i, 0, QTableWidgetItem(rect.name))
            self.rect_table.setItem(i, 1, QTableWidgetItem(str(rect.width)))
            self.rect_table.setItem(i, 2, QTableWidgetItem(str(rect.height)))
            
            # Create a QCheckBox for the "Can Rotate" column
            can_rotate_checkbox = QCheckBox()
            can_rotate_checkbox.setChecked(rect.can_rotate)
            can_rotate_checkbox.stateChanged.connect(lambda state, row=i: self.on_can_rotate_changed(row, state))
            self.rect_table.setCellWidget(i, 3, can_rotate_checkbox)

    def on_can_rotate_changed(self, row, state):
        self.rectangles[row].can_rotate = bool(state)

    def clear_rectangle_inputs(self):
        self.name_entry.clear()
        self.width_entry.clear()
        self.height_entry.clear()
        self.can_rotate_var.setChecked(False)

    def on_select_rectangle(self):
        selected_items = self.rect_table.selectedItems()
        if selected_items:
            row = self.rect_table.row(selected_items[0])
            self.name_entry.setText(self.rect_table.item(row, 0).text())
            self.width_entry.setText(self.rect_table.item(row, 1).text())
            self.height_entry.setText(self.rect_table.item(row, 2).text())
            self.can_rotate_var.setChecked(self.rect_table.cellWidget(row, 3).isChecked())

    def on_cell_changed(self, row, column):
        item = self.rect_table.item(row, column)
        if item is not None:
            rect = self.rectangles[row]
            if column == 0:  # Name
                rect.name = item.text()
            elif column == 1:  # Width
                rect.width = float(item.text())
            elif column == 2:  # Height
                rect.height = float(item.text())

    def remove_rectangle(self):
        selected_items = self.rect_table.selectedItems()
        if selected_items:
            row = self.rect_table.row(selected_items[0])
            del self.rectangles[row]
            self.update_rectangle_list()
            self.clear_rectangle_inputs()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RectanglePackingGUI()
    window.show()
    sys.exit(app.exec())