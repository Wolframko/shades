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
        "can_rotate": "bool"
      }
    ],
    "bins": [
      {
        "width": "float",
        "height": "float"
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
        "height": "float",
        "used_height": "float",
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
    ]
  }
  ```

### 2. Pack Rectangles (HTML)
- **URL:** `/pack/html`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "rectangles": [
      {
        "name": "string",
        "width": "float",
        "height": "float",
        "can_rotate": "bool"
      }
    ],
    "bins": [
      {
        "width": "float",
        "height": "float"
      }
    ]
  }
  ```
- **Response:** HTML content visualizing the packed rectangles.


### 4. Root
- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "message": "Rectangle Packing API",
    "endpoints": ["/pack/json", "/pack/html"]
  }
  ```

## Project Structure

- `api.py`: Main FastAPI application file.
- `bin.py`: Contains the `Bin` class and related methods.
- `rectangle.py`: Contains the `Rectangle` class and related methods.
- `utils.py`: Utility functions for packing and visualizing rectangles.
- `greedy.py`: Greedy algorithm implementation for packing rectangles.
- `requirements.txt`: List of Python packages required for the project.