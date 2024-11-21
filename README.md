# Rectangle Packing API

This API allows you to pack rectangles into bins using a greedy algorithm. It provides endpoints to get the packing results in JSON and HTML.

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Installation

1. **Unpack server**

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the API

1. **Start the FastAPI server:**
    ```sh
    python ./api.py
    ```

## API Endpoints

### 1. Pack Rectangles (JSON)
- **URL:** `/pack/json`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "rectangles": [
      {
        "name": "string",
        "width": "float",
        "height": "float",
        "can_rotate": "int"  // 0, 1, 2
      }
    ],
    "bins": [
      {
        "width": "float",
        "name": "string (optional)",
        "id": "int (optional)"
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "packed_bins": [
      {
        "width": "float",
        "used_height": "float",
        "name": "string",
        "id": "int",
        "rectangles": [
          {
            "name": "string",
            "width": "float",
            "height": "float",
            "x": "float",
            "y": "float",
            "rotated": "bool"
          }
        ]
      }
    ],
    "warnings": ["string"]  // Names of rectangles that couldn't be packed
  }
  ```

### 2. Pack Rectangles (HTML)
- **URL:** `/pack/html`
- **Method:** `POST`
- **Request Body:** Same as `/pack/json`
- **Response:** HTML visualization of the packing solution with cut lines

## Bin Features

### Bin Identification
Each bin can be assigned:
- **ID**: An optional integer identifier. If not provided, bins are automatically assigned IDs based on their order (0, 1, 2, ...).
- **Name**: An optional string name. If not provided, bins are automatically named as "Bin_[ID]".

Example request with custom bin identification:
```json
{
  "rectangles": [
    {
      "name": "rect1",
      "width": 100,
      "height": 50,
      "can_rotate": 1
    }
  ],
  "bins": [
    {
      "width": 200,
      "name": "Custom Bin",
      "id": 42
    }
  ]
}
```

## Project Structure

- `api.py`: Main FastAPI application file.
- `bin.py`: Contains the `Bin` class and related methods.
- `rectangle.py`: Contains the `Rectangle` class and related methods.
- `utils.py`: Utility functions for packing and visualizing rectangles.
- `greedy.py`: Greedy algorithm implementation for packing rectangles.
- `requirements.txt`: List of Python packages required for the project.