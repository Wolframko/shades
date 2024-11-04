# Rectangle Packing API

This API allows you to pack rectangles into bins using a greedy algorithm. It provides endpoints to get the packing results in JSON, HTML, and PDF formats.

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

### 3. Pack Rectangles (PDF)
- **URL:** `/pack/pdf`
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
- **Response:** PDF file visualizing the packed rectangles.

### 4. Root
- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "message": "Rectangle Packing API",
    "endpoints": ["/pack/json", "/pack/html", "/pack/pdf"]
  }
  ```