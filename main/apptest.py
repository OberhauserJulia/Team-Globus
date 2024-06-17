from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Datenmodell für die Antwort
class ItemResponse(BaseModel):
    data: str

# Datenbank-Simulation (in-memory)
database = {
    "current_item": ""
}

@app.post("/api/placeitem", response_model=ItemResponse)
async def place_item():
    # Simuliere das Platzieren eines Artikels
    database["current_item"] = "SampleItem"
    
    return {"data": database["current_item"]}

@app.post("/api/itemanalyzed/{item}", response_model=ItemResponse)
async def item_analyzed(item: str):
    if item != database["current_item"]:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Simuliere das Analysieren des Artikels
    analyzed_data = f"{item} analyzed"
    database["current_item"] = analyzed_data
    
    return {"data": analyzed_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
