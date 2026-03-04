from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import  get_scalar_api_reference
from typing import Any
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import save_shipments, shipments_db

app = FastAPI()
    
# shipments_db = {
#     12345: {
#         "id": 12345,
#         "shipment_title": "Wooden Table",
#         "shipment_weight": 20.5,
#         "shipment_description": "A sturdy wooden table perfect for dining rooms.",
#         "shipment_status": "In Transit"
#     },
#     12346: {
#         "id": 12346,
#         "shipment_title": "Office Chair",
#         "shipment_weight": 15.0,
#         "shipment_description": "An ergonomic office chair with adjustable height.",
#         "shipment_status": "Delivered"
#     },
#     12347: {
#         "id": 12347,
#         "shipment_title": "Laptop",
#         "shipment_weight": 2.5,
#         "shipment_description": "A high-performance laptop suitable for gaming and work.",
#         "shipment_status": "Shipped"
#     },
#     12348: {
#         "id": 12348,
#         "shipment_title": "Bookshelf",
#         "shipment_weight": 30.0,
#         "shipment_description": "A spacious bookshelf made of solid wood.",
#         "shipment_status": "Processing"
#     },
#     12349: {
#         "id": 12349,
#         "shipment_title": "Desk Lamp",
#         "shipment_weight": 1.0,
#         "shipment_description": "A modern LED desk lamp with adjustable brightness.",
#         "shipment_status": "Out for Delivery"
#     },
#     12351: { 
#         "id": 12351,
#         "shipment_title": "Smartphone",
#         "shipment_weight": 0.2,
#         "shipment_description": "A latest model smartphone with advanced features.",
#         "shipment_status": "Delivered"
#     },
#     12352: {
#         "id": 12352,
#         "shipment_title": "Headphones",
#         "shipment_weight": 0.5,
#         "shipment_description": "Noise-cancelling over-ear headphones with high-fidelity sound.",
#         "shipment_status": "In Transit"
#     },
#     12353: {
#         "id": 12353,
#         "shipment_title": "Coffee Maker",
#         "shipment_weight": 2.0,
#         "shipment_description": "A programmable coffee maker with a built-in grinder.",
#         "shipment_status": "Shipped"
#     },
#     12354: {
#         "id": 12354,
#         "shipment_title": "Fitness Tracker",
#         "shipment_weight": 0.3,
#         "shipment_description": "A waterproof fitness tracker with heart rate monitoring.",
#         "shipment_status": "Processing"
#     },
#     12355: {
#         "id": 12355,
#         "shipment_title": "Gaming Console",
#         "shipment_weight": 5.0,
#         "shipment_description": "A next-gen gaming console with immersive graphics.",
#         "shipment_status": "Out for Delivery"
#     }
        
# }

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )

@app.get("/shipment/latest")
def get_latest_shipments():
    id = max(shipments_db.keys())  # Get the maximum tracking ID
    return shipments_db[id]  

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    if id not in shipments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment ID {id} not found")
    #shipment_data = shipments_db[id]
    return shipments_db[id]
  
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    # Create and assign shipment a new id
    new_id = max(shipments_db.keys()) + 1
    # Add to shipments dict
    shipments_db[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "shipment_status": "Placed"
    }
    save_shipments()
    # Return id for later use
    return {"id": new_id}

@app.get("/shipments/{field}")
def get_shipments_by_field(field: str, id: int = None) -> dict [str, Any]:
    if field not in ["shipment_title", "shipment_weight", "shipment_description", "shipment_status"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid field: {field}. Valid fields are 'shipment_title', 'shipment_weight', 'shipment_description', 'shipment_status'."
        )
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shipment ID is required"
        )
    if id not in shipments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment ID {id} not found"
        )
    return {
        field: shipments_db[id][field]
    }

@app.put("/shipment/")
def update_shipment(id: int, shipment_title: str = None, shipment_weight: float = None, shipment_description: str = None, shipment_status: str = None) -> dict[str, Any]:
    shipments_db[id] = {
        "shipment_title": shipment_title,
        "shipment_weight": shipment_weight,
        "shipment_description": shipment_description,
        "shipment_status": shipment_status
    }
    return shipments_db[id]

# 1 Way of updating a shipment is to use the PUT method, which replaces the entire shipment record with the new data provided in the request. This means that if any field is not included in the request, it will be set to null or default value in the database. This method is useful when you want to update all fields of a shipment at once.
# 2 Way of updating a shipment is to use the PATCH method, which allows you to update only specific fields of a shipment without affecting the other fields. This means that if you only want to update the shipment status, you can send a PATCH request with just the shipment_status field, and the other fields will remain unchanged in the database. This method is useful when you want to make partial updates to a shipment record.
# In summary, the PUT method is used for full updates of a shipment record, while the PATCH method is used for partial updates of specific fields in a shipment record.
# Patch method can be used by updating the body of the request with the fields that you want to update, and the server will only update those fields in the database, leaving the other fields unchanged. This allows for more flexibility and efficiency when updating shipment records, as you can update only the necessary fields without having to send the entire shipment data in the request.
# @app.patch("/shipment")
# def patch_shipment(id: int, shipment_title: str | None = None, shipment_weight: float | None = None, shipment_description: str | None = None, shipment_status: str | None = None) -> dict[str, Any]:
#     if id not in shipments_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Shipment ID {id} not found"
#         )
#     if shipment_weight is not None and shipment_weight >= 26.0:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail="Shipment weight must be less than 26 kg"
#         )
#     if shipment_title is not None:
#         shipments_db[id]["shipment_title"] = shipment_title
#     if shipment_weight is not None:
#         shipments_db[id]["shipment_weight"] = shipment_weight
#     if shipment_description is not None:
#         shipments_db[id]["shipment_description"] = shipment_description
#     if shipment_status is not None:
#         shipments_db[id]["shipment_status"] = shipment_status
#     return shipments_db[id]

@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, body: ShipmentUpdate):
    if id not in shipments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment ID {id} not found"
        )
    # shipment_to_update = shipments_db[id]
    # shipment_to_update.update(body)
    # shipments_db[id] = shipment_to_update
    shipments_db[id].update(body.model_dump(exclude_none=True))
    save_shipments()
    return shipments_db[id]

@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    if id not in shipments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment ID {id} not found"
        )
    del shipments_db[id]
    return {"message": f"Shipment with ID {id} deleted successfully"}