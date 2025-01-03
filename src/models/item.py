### Item model for the EETT extraction process ###
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(description="Name of the item")
    is_recommended: bool = Field(description="If the item is recommended")
    brand: str = Field(description="Brand of the item")
    specifications: str = Field(description="A brief description of the specifications of the item")
    location: str = Field(description="Location where the item should be located")
    length: float = Field(
        description="Length of the item in meters",
        default=0.0
    )
    width: float = Field(
        description="Width of the item in meters", 
        default=0.0
    )
    height: float = Field(
        description="Height of the item in meters",
        default=0.0
    )
    quantity: int = Field(description="Quantity of items", ge=0)