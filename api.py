from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List
from rectangle import Rectangle
from bin import Bin
from greedy import pack_multiple_bins
from utils import generate_html, save_bins_to_json
import json

app = FastAPI()

class RectangleInput(BaseModel):
    name: str
    width: float
    height: float
    can_rotate: int

class BinInput(BaseModel):
    width: float
    height: float

class PackingInput(BaseModel):
    rectangles: List[RectangleInput]
    bins: List[BinInput]

def pack_rectangles_helper(input_data: PackingInput):
    rectangles = [Rectangle(**rect.dict()) for rect in input_data.rectangles]
    bins = [Bin(**bin.dict()) for bin in input_data.bins]
    results = pack_multiple_bins(rectangles, bins)
    
    # Track packed rectangles
    packed_names = set()
    for bin, _, _ in results:
        for rect, _, _ in bin.rectangles:
            packed_names.add(rect.name)
    
    # Identify unpacked rectangles
    warnings = [rect.name for rect in rectangles if rect.name not in packed_names]
    
    return results, warnings

@app.post("/pack/json")
async def pack_rectangles_json(input_data: PackingInput):
    results, warnings = pack_rectangles_helper(input_data)
    
    response_data = {
        "packed_bins": [
            {
                "width": bin.width,
                "height": bin.height,
                "used_height": bin.used_height,
                "rectangles": [
                    {
                        "name": rect.name,
                        "width": rect.width,
                        "height": rect.height,
                        "x": x,
                        "y": y,
                        "rotated": rect.is_rotated
                    } for rect, x, y in bin.rectangles
                ]
            } for bin, _, _ in results
        ],
        "warnings": warnings
    }
    
    return response_data

@app.post("/pack/html")
async def pack_rectangles_html(input_data: PackingInput):
    results, warnings = pack_rectangles_helper(input_data)
    
    html_content = generate_html([bin for bin, _, _ in results], [cut_lines for _, cut_lines, _ in results])
    
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/")
async def root():
    return {"message": "Rectangle Packing API", "endpoints": ["/pack/json", "/pack/html"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
