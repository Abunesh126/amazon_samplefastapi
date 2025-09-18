from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Product model
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    stock: int
    category: str

# Dummy database
products = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop with 16GB RAM",
        "price": 999.99,
        "stock": 10,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Smartphone",
        "description": "Latest model with 5G support",
        "price": 699.99,
        "stock": 15,
        "category": "Electronics"
    },
    {
        "id": 3,
        "name": "Coffee Maker",
        "description": "Automatic coffee maker with timer",
        "price": 79.99,
        "stock": 20,
        "category": "Home Appliances"
    }
]

# Get all products
@app.get("/products", response_model=List[Product])
async def get_products():
    return products

# Get product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# Add new product
@app.post("/products", response_model=Product)
async def create_product(product: Product):
    try:
        # Generate new ID
        new_id = max([p["id"] for p in products]) + 1
        new_product = product.dict()
        new_product["id"] = new_id
        products.append(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))