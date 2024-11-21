# Rectangle Packing API

This API allows you to pack rectangles into bins using a greedy algorithm. It provides endpoints to get the packing results in JSON and HTML formats.

## Endpoints

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
        "can_rotate": "int"
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
    "warnings": ["string"] // Names of rectangles that couldn't be packed
  }
  ```

### 2. Pack Rectangles (HTML)
- **URL:** `/pack/html`
- **Method:** `POST`
- **Request Body:** Same as `/pack/json`
- **Response:** HTML content visualizing the packed rectangles with cut lines.

### 3. Root
- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "message": "Rectangle Packing API",
    "endpoints": ["/pack/json", "/pack/html"]
  }
  ```

## Notes
- Each bin can have an optional name and ID. If not provided, bins are automatically assigned sequential IDs (0, 1, 2, ...) and names ("Bin_0", "Bin_1", etc.).
- The `can_rotate` parameter should be an integer value (0 or 1) indicating whether the rectangle can be rotated.
- The API returns warnings when some rectangles cannot be packed into any of the provided bins.
- The HTML response includes a visual representation of the packing solution with cut lines.