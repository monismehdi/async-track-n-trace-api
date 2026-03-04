from pydantic import BaseModel, Field
from enum import Enum

class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"


class BaseShipment(BaseModel):
    shipment_title: str = Field(..., description="The title of the shipment")
    shipment_weight: float = Field(..., description="The weight of the shipment in kg")
    shipment_description: str = Field(..., description="The description of the shipment")
    
class ShipmentRead(BaseShipment):
    shipment_status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    shipment_status: ShipmentStatus

